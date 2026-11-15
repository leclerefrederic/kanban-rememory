"""Preview or apply approved multi-module setup to the current repository."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import tempfile

from kanban.batches import batch_descriptions
from kanban.files import ROOT, cards, header_value
from kanban.project import primary_worktree, read_manifest
from kanban.specifications import specification_directories, specification_root
from kanban.workflow import check_workflow


@contextmanager
def activation_lock():
    common = subprocess.check_output(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
        cwd=ROOT, text=True,
    ).strip()
    directory = Path(common) / "kanban-rememory"
    directory.mkdir(exist_ok=True)
    lock = directory / "batch-pickup.lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError("Repository coordination is occupied. Retry after the owner releases it.") from None
    try:
        yield
    finally:
        lock.rmdir()


def check_legacy_work():
    workflow_file = ROOT / "project/kanban/workflow.json"
    if workflow_file.is_file():
        workflow = check_workflow(json.loads(workflow_file.read_text(encoding="utf-8")))
        for stage in workflow["active"]:
            if cards(stage):
                raise ValueError("Close existing active Cards before activating modules.")
        intake = workflow.get("intake", workflow["stages"][0])
        if cards(intake):
            raise ValueError("Account for existing backlog Cards in an approved migration plan.")
    for description in batch_descriptions():
        status = header_value(description.read_text(encoding="utf-8"), "status")
        if status not in {"draft", "ready", "closed"}:
            raise ValueError("Close existing active Batches before activating modules.")


def plan(manifest, workflow, with_batches=False):
    manifest.check_legacy_boards()
    board = manifest.board / "kanban"
    paths = [*manifest.setup_memory(), board, *(board / stage for stage in workflow["stages"])]
    for workspace in manifest.modules.values():
        if with_batches:
            paths.extend(specification_directories(workspace))
        else:
            specification_root(workspace)
    for path in paths:
        if path.resolve() != path or (path.exists() and not path.is_dir()):
            raise ValueError(f"Not a local directory: {path.relative_to(ROOT)}.")
    config = board / "workflow.json"
    if config.is_symlink():
        raise ValueError(f"Not a local workflow: {config.relative_to(ROOT)}.")
    if config.exists() and check_workflow(json.loads(config.read_text(encoding="utf-8"))) != workflow:
        raise ValueError(f"Different workflow already exists: {config.relative_to(ROOT)}.")
    if board.exists():
        outside = [p for p in board.iterdir()
                   if p.is_dir() and p.name not in workflow["stages"] and any(p.glob("*.md"))]
        if outside:
            raise ValueError("The project contains Cards outside the approved stages.")
    return paths


def configure(args):
    if primary_worktree(ROOT) != ROOT:
        raise ValueError("Activate modules from the primary worktree.")
    target = ROOT / "project.json"
    if target.exists() or target.is_symlink():
        raise ValueError("A manifest already exists. Use an explicit migration to change it.")
    with tempfile.TemporaryDirectory() as temporary:
        # Validate and publish the same bytes, even if the proposal changes later.
        snapshot = Path(temporary) / "project.json"
        snapshot.write_bytes(args.manifest.read_bytes())
        manifest = read_manifest(ROOT, snapshot)
        workflow = check_workflow(json.loads(args.workflow.read_text(encoding="utf-8")))
        check_legacy_work()
        paths = plan(manifest, workflow, args.with_batches)
        print(f"{manifest.name}: {', '.join(manifest.modules)}")
        print(json.dumps(workflow, indent=2))
        for path in paths:
            print(path.relative_to(ROOT))
        if not args.apply:
            print("Preview only. Run again with --apply after approval.")
            return
        with activation_lock():
            if target.exists() or target.is_symlink():
                raise ValueError("A project manifest appeared after preview.")
            check_legacy_work()
            if plan(manifest, workflow, args.with_batches) != paths:
                raise ValueError("The installation paths changed. Review the setup preview again.")
            for path in paths:
                path.mkdir(parents=True, exist_ok=True)
                if not any(path.iterdir()):
                    (path / ".gitkeep").touch(exist_ok=True)
            config = manifest.board / "kanban/workflow.json"
            if not config.exists():
                with config.open("x", encoding="utf-8") as stream:
                    json.dump(workflow, stream, indent=2)
                    stream.write("\n")
            with tempfile.NamedTemporaryFile(dir=ROOT, prefix=".project-", delete=False) as pending:
                staged = Path(pending.name)
                pending.write(snapshot.read_bytes())
            try:
                os.link(staged, target)
            finally:
                staged.unlink()
        print("Project modules are ready.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Proposed manifest")
    parser.add_argument("--workflow", type=Path, required=True, help="Approved workflow JSON")
    parser.add_argument("--with-batches", action="store_true", help="Set up Specifications and Batches in each module")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        configure(args)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
