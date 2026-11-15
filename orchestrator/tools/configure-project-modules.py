"""Preview or apply approved project settings and module boards in the current repository."""

import argparse
import os
from pathlib import Path
import subprocess
import tempfile

from kanban.coordination import exclusive
from kanban.files import ROOT
from kanban.project import SETTINGS, coordination_root, parse_settings, primary_worktree
from kanban.workflow import check_new_workflow


def plan(project):
    paths = [project.memory]
    for workspace in project.modules.values():
        paths.extend(workspace / stage for stage in (*project.workflow["stages"], "resources"))
    for path in paths:
        if path.resolve() != path or (path.exists() and not path.is_dir()):
            raise ValueError(f"Not a local directory: {path.relative_to(ROOT)}.")
    return paths


def configure(proposal, apply):
    if primary_worktree(ROOT) != ROOT:
        raise ValueError("Configure the project from the primary worktree.")
    settings = ROOT / SETTINGS
    if settings.exists() or settings.is_symlink():
        raise ValueError("Project settings already exist. Agree an explicit migration to change them.")
    # Validate and publish the same bytes, even if the proposal changes later.
    source = proposal.read_bytes()
    project = parse_settings(ROOT, source)
    check_new_workflow(project.workflow)
    paths = plan(project)
    print(f"{project.name}: {', '.join(project.modules)}")
    for path in paths:
        print(path.relative_to(ROOT))
    if not apply:
        print("Preview only. Run again with --apply after approval.")
        return
    with exclusive(coordination_root(ROOT), "setup"):
        if settings.exists() or settings.is_symlink():
            raise ValueError("Project settings appeared after preview.")
        if plan(project) != paths:
            raise ValueError("The installation paths changed. Review the setup preview again.")
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
            if not any(path.iterdir()):
                (path / ".gitkeep").touch(exist_ok=True)
        settings.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=settings.parent, prefix=".settings-", delete=False) as pending:
            staged = Path(pending.name)
            pending.write(source)
        try:
            os.link(staged, settings)  # Refuses to replace a file created concurrently.
        finally:
            staged.unlink()
    print("Project modules are ready.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("settings", type=Path, help="Proposed project/settings.json content")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        configure(args.settings, args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
