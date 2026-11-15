"""Check scope, acceptance artifact integrity, and publication evidence."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def revision(ref):
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], text=True
    ).strip()


def artifact_digest(path):
    digest = hashlib.sha256()
    entries = sorted(path.rglob("*")) if path.is_dir() else [path]
    for entry in entries:
        if entry.is_symlink():
            raise ValueError("Acceptance artifacts must not contain symbolic links.")
        if entry.is_file():
            digest.update(str(entry.relative_to(path.parent)).encode() + b"\0")
            digest.update(b"x" if entry.stat().st_mode & 0o111 else b"-")
            with entry.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def record_scope(record, module):
    from kanban.files import ROOT, check_module_records
    from kanban.project import coordination_root, invocation_module, load_project, primary_worktree

    project = load_project(primary_worktree(ROOT))
    selected = project.select_module(invocation_module(module))
    workspace = project.workspace(selected)
    if selected is None:
        return project.board, None, None
    check_module_records(workspace)
    check_module_records(project.board)
    prefix = coordination_root(ROOT).resolve() / "projects" / project.id / "modules" / selected
    path = record.absolute()
    if (not path.is_relative_to(prefix) or len(path.relative_to(prefix).parts) != 2
            or path.name != "guard.json" or path != path.resolve()
            or not re.fullmatch(r"batch-[0-9]+", path.parent.name)):
        raise ValueError(f"Expected a local guard at {prefix}/<batch>/guard.json.")
    return project.board, f"Batch-{path.parent.name[6:]}", selected


def active_card(card, workspace, batch=None, scope=None):
    from kanban.files import header_value

    board = workspace / "kanban"
    path = board / "workflow.json"
    if not path.exists():
        raise ValueError("kanban/workflow.json is required.")
    if batch is not None:
        from kanban.workflow import load_workflow

        stages = load_workflow(workspace)["active"]
    else:
        stages = json.loads(path.read_text()).get("active")
    if not stages:
        raise ValueError("workflow.json must list its active stages.")
    for stage in stages:
        for path in (board / stage).glob(card.lower() + "-*.md"):
            if path.is_symlink() or not path.is_file():
                continue
            source = path.read_text(encoding="utf-8")
            if batch is None or (header_value(source, "batch") == batch and header_value(source, "scope") == scope):
                return True
    return False


def verify_artifact(candidate):
    if not candidate or not Path(candidate["path"]).exists():
        raise ValueError("The acceptance artifact is missing.")
    if artifact_digest(Path(candidate["path"])) != candidate["sha256"]:
        raise ValueError("The acceptance artifact changed.")


def verify_module_product(record, accepted, published):
    from kanban.accepted_content import verify_accepted_content
    from kanban.project import coordination_root

    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()
    relative = record.resolve()
    common = coordination_root(root).resolve()
    if relative.is_relative_to(common):
        parts = relative.relative_to(common).parts
        if len(parts) == 6 and parts[0] == "projects" and parts[2] == "modules" and parts[-1] == "guard.json":
            verify_accepted_content(root, accepted, published)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["change", "correct", "freeze", "verify", "publish"])
    parser.add_argument("record", type=Path)
    parser.add_argument("--card")
    parser.add_argument("--module", help="Module ID from project.json")
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--blocking-test")
    parser.add_argument("--restart", action="store_true")
    parser.add_argument("--revision", help="commit being published; defaults to HEAD")
    args = parser.parse_args()
    try:
        # Pre-push already selects and verifies the record against the pushed commit.
        if args.operation != "publish" or args.module is not None:
            workspace, batch, scope = record_scope(args.record, args.module)
        record = json.loads(args.record.read_text())
        current = revision("HEAD")
        frozen = record.get("acceptance")
        if args.operation in {"change", "correct"}:
            if not re.fullmatch(r"[A-Z][A-Z0-9]*-[0-9]{8}", args.card or ""):
                raise ValueError("An active Card ID is required.")
            if args.card not in record["authorized_cards"] or not active_card(args.card, workspace, batch, scope):
                raise ValueError("Record out-of-scope work in Backlog and defer it.")
            if args.operation == "correct":
                if not frozen or not args.blocking_test or record.get("correction"):
                    raise ValueError("Record a blocking test for the current acceptance candidate.")
                verify_artifact(frozen)
                record["correction"] = {"card": args.card, "test": args.blocking_test}
                record.pop("decision", None)
                record.pop("verification", None)
            elif frozen:
                if record.get("correction", {}).get("card") != args.card:
                    raise ValueError("Acceptance is active. Preserve the recorded build.")
                verify_artifact(frozen)
        elif args.operation == "freeze":
            if frozen and not args.restart:
                raise ValueError("Explicitly restart affected tests before replacing the acceptance baseline.")
            path = args.artifact
            if path is None or not path.exists():
                raise ValueError("An existing acceptance artifact is required.")
            if frozen:
                verify_artifact(frozen)
                if current == frozen["revision"] or any(
                    candidate == path.resolve() or candidate in path.resolve().parents
                    or path.resolve() in candidate.parents
                    for candidate in [Path(frozen["path"]), *(
                        Path(item["path"]) for item in record.get("previous_candidates", [])
                    )]
                ):
                    raise ValueError("Use a new commit and a separate artifact path.")
                record.setdefault("previous_candidates", []).append({
                    **frozen, "correction": record.pop("correction", None),
                })
            record.pop("verification", None)
            record["acceptance"] = {"revision": current, "path": str(path.resolve()),
                                    "sha256": artifact_digest(path.resolve())}
            record.pop("decision", None)
        else:
            verify_artifact(frozen)
            if args.operation == "publish":
                published = revision(args.revision) if args.revision else current
                decision = record.get("decision") or {}
                if decision.get("result") == "rejected":
                    if decision.get("revision") != frozen["revision"]:
                        raise ValueError("Record the User's rejection of the exact revision.")
                    if subprocess.run(["git", "merge-base", "--is-ancestor", frozen["revision"], published]
                                      ).returncode != 1:
                        raise ValueError("A rejected revision must stay out of the published history.")
                else:
                    if record.get("correction"):
                        raise ValueError("Complete correction and restart acceptance before publication.")
                    checks = record.get("verification", {})
                    if checks.get("revision") != frozen["revision"] or checks.get("technical_checks") != "passed":
                        raise ValueError("Record passing technical checks for the acceptance revision.")
                    changed = subprocess.check_output(
                        ["git", "diff", "--name-only", revision(record["base_revision"]), frozen["revision"]],
                        text=True,
                    ).splitlines()
                    strict = set(record.get("full_build_files", []))
                    if any(Path(path).name in strict for path in changed) and checks.get("full_build") != "passed":
                        raise ValueError("Changes to " + ", ".join(sorted(strict)) + " require a successful full build.")
                    if decision != {"revision": frozen["revision"], "result": "accepted"}:
                        raise ValueError("Record the User's acceptance of the exact revision.")
                    subprocess.run(["git", "merge-base", "--is-ancestor", frozen["revision"], published], check=True)
                    verify_module_product(args.record, frozen["revision"], published)
        if args.operation in {"correct", "freeze"}:
            args.record.write_text(json.dumps(record, indent=2) + "\n")
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    print("Batch guard passed.")


if __name__ == "__main__":
    main()
