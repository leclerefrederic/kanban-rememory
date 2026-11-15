"""Pre-push check for Batch closures being published on main."""

import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

from kanban.accepted_content import verify_accepted_content
from kanban.files import header_value
from kanban.project import parse_manifest


BATCH_DIR = re.compile(r"batch-[0-9]+")
OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
STATUSES = {"draft", "ready", "in-progress", "delivered", "validated", "rejected", "closed"}


def git(*args, check=True):
    result = subprocess.run(["git", *args], capture_output=True)
    if check and result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "git failed")
    return result.stdout if result.returncode == 0 else None


def snapshot(sha):
    """Read paths and object modes from the pushed tree, independent of checkout."""
    entries = {}
    for entry in git("ls-tree", "-r", "-t", "-z", "--full-tree", sha).split(b"\0"):
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, _, object_id = metadata.decode("ascii").split()
            entries[PurePosixPath(path.decode("utf-8", errors="surrogateescape"))] = (mode, object_id)
    return entries


def regular_object(tree, path):
    mode, object_id = tree[path]
    if mode not in {"100644", "100755"}:
        raise ValueError(f"Expected a regular file: {path}.")
    return git("cat-file", "blob", object_id)


def committed_project(root, tree):
    path = PurePosixPath("project.json")
    if path not in tree:
        return None
    project = parse_manifest(root, regular_object(tree, path), resolve_paths=False)
    workspaces = {
        module: PurePosixPath(workspace.relative_to(root).as_posix())
        for module, workspace in project.modules.items()
    }
    directories = [*workspaces.values(), PurePosixPath(project.memory.relative_to(root).as_posix())]
    for source in project.sources:
        path = PurePosixPath(source.relative_to(root).as_posix())
        if path in tree and tree[path][0] == "120000":
            raise ValueError(f"Manifest source is a symbolic link: {path}.")
        directories.extend(path.parents)
    for path in directories:
        for folder in (path, *path.parents):
            if folder in tree and tree[folder][0] != "040000":
                raise ValueError(f"Manifest directory is not a local tree: {folder}.")
    return project.id, workspaces


def statuses(tree, project):
    """Track legacy history and each module by its qualified Batch identity."""
    found = {}
    batch_roots = {PurePosixPath("project/batches"): (None, None)}
    if project:
        project_id, workspaces = project
        for module, workspace in workspaces.items():
            batch_roots[workspace / "batches"] = (project_id, module)

    for path in tree:
        if path.name != "description.md" or path.parent.parent not in batch_roots:
            continue
        project_id, module = batch_roots[path.parent.parent]
        batch = path.parent.name
        try:
            source = regular_object(tree, path).decode("utf-8")
            status = header_value(source, "status")
        except ValueError:
            if module:
                raise
            status = None
        if module:
            if not BATCH_DIR.fullmatch(batch) or header_value(source, "id") != f"Batch-{batch[6:]}":
                raise ValueError(f"Batch ID does not match its module record: {path}.")
            if not isinstance(status, str) or status not in STATUSES:
                raise ValueError(f"Invalid Batch status: {path}.")
        found[(project_id, module, batch)] = status
    return found


def coordination_record(path):
    if not path.is_file() or path.resolve() != path:
        raise ValueError(f"Missing or linked publication evidence: {path.name}.")
    record = json.loads(path.read_bytes())
    if not isinstance(record, dict):
        raise ValueError(f"Invalid publication evidence: {path.name}.")
    return record


def verify_module_closure(root, common, local_sha, remote_sha, identity):
    project_id, module, batch = identity
    delivery = f"Batch-{batch[6:]}"
    directory = common / "kanban-rememory" / "projects" / project_id
    evidence = coordination_record(directory / f"closure-{module}-{batch}.json")
    integration = coordination_record(directory / "integration.json")
    if (evidence.get("project") != project_id or evidence.get("delivery") != f"{module}/{delivery}"
            or evidence.get("closing") != local_sha or evidence.get("main_revision") != remote_sha
            or evidence.get("result") not in ("accepted", "rejected") or not evidence.get("owner")):
        raise ValueError(f"Closing evidence does not match {module}/{delivery} or the pushed revisions.")
    if (integration.get("module") != module or integration.get("owner") != evidence["owner"]
            or integration.get("delivery") != delivery or integration.get("main_revision") != remote_sha
            or integration.get("verified_revision") != local_sha or not integration.get("worktree")):
        raise ValueError(f"Integration ownership does not match {module}/{delivery}.")
    trailer = git("show", "-s", "--format=%(trailers:key=Batch-Closure,valueonly)", local_sha)
    if trailer.decode().strip() != f"{module}/{delivery}":
        raise ValueError(f"Closing commit requires Batch-Closure: {module}/{delivery}.")
    candidate = evidence.get("candidate")
    if not isinstance(candidate, str) or not OBJECT_ID.fullmatch(candidate):
        raise ValueError(f"Missing exact candidate for {module}/{delivery}.")
    if git("merge-base", "--is-ancestor", remote_sha, local_sha, check=False) is None:
        raise ValueError("The closing commit does not preserve the remote main revision.")
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", candidate, local_sha], capture_output=True)
    expected = 0 if evidence["result"] == "accepted" else 1
    if ancestry.returncode != expected:
        raise ValueError(f"Candidate ancestry does not match the decision for {module}/{delivery}.")
    if evidence["result"] == "accepted":
        verify_accepted_content(root, candidate, local_sha)


def guard_path(common, project_id, module, batch):
    directory = common / "kanban-rememory"
    if module:
        directory /= Path("projects") / project_id / "modules" / module
    return directory / batch / "guard.json"


def verify_artifact_guard(common, root, guard, local_sha, identity):
    project_id, module, batch = identity
    record = guard_path(common, project_id, module, batch)
    if not record.exists() and not record.is_symlink():
        return
    if record.is_symlink() or not record.is_file() or record.resolve() != record:
        raise ValueError(f"Batch guard must be a regular local file: {record}.")
    result = subprocess.run(
        [sys.executable, str(guard), "publish", "--revision", local_sha, str(record)],
        cwd=root, capture_output=True, text=True,
    )
    if result.returncode:
        label = f"{module}/{batch}" if module else batch
        raise ValueError(f"{label} cannot be closed. {result.stderr.strip()}")


def main():
    root = Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve()
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip()).resolve()
    guard = Path(__file__).with_name("guard-batch-work.py")
    for line in sys.stdin:
        fields = line.split()
        if len(fields) != 4:
            raise ValueError("Malformed Git pre-push input.")
        _, local_sha, remote_ref, remote_sha = fields
        if remote_ref != "refs/heads/main":
            continue
        if not OBJECT_ID.fullmatch(local_sha) or not OBJECT_ID.fullmatch(remote_sha):
            raise ValueError("Expected full Git object IDs.")
        if not local_sha.strip("0"):
            continue
        local_tree = snapshot(local_sha)
        local_project = committed_project(root, local_tree)
        if not remote_sha.strip("0"):
            # Preserve the initial-publication behavior when there is no remote main.
            continue
        if git("cat-file", "-e", remote_sha, check=False) is None:
            if local_project:
                raise ValueError("Fetch the remote main revision before module publication.")
            continue  # Preserve legacy behavior for an unavailable remote revision.
        remote_tree = snapshot(remote_sha)
        remote_project = committed_project(root, remote_tree)
        if remote_project and not local_project:
            raise ValueError("The update removes the active project manifest.")
        before = statuses(remote_tree, remote_project)
        for identity, status in statuses(local_tree, local_project).items():
            if status == "closed" and before.get(identity) != "closed":
                if identity[1] is not None:
                    verify_module_closure(root, common, local_sha, remote_sha, identity)
                verify_artifact_guard(common, root, guard, local_sha, identity)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError) as error:
        sys.exit(f"Push refused: {error}")
