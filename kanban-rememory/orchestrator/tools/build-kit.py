"""Build the installation kit as a ZIP archive from the committed files of HEAD.

Everything sits under kanban-rememory/, the one folder the install replaces, so unpacking the kit in a repository
cannot overwrite a user file. kanban-rememory.json is this repository's own configuration and stays out; VERSION
carries the kit version and the GUARDRAILS.md template is the file of HEAD. START.md, the instructions to give the
agent, is written next to the archive and is not part of it."""

import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[3]


def build(root, output=None):
    """Write dist/kanban-rememory-kit-<version>.zip, or output, and return its path."""
    config = subprocess.check_output(["git", "show", "HEAD:kanban-rememory.json"], cwd=root)
    version = json.loads(config)["version"]
    folder = f"kanban-rememory-kit-{version}"
    target = Path(output) if output else root / "dist" / f"{folder}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "archive", "--format=zip", f"--prefix={folder}/", "-o", str(target),
                           "HEAD", "--", "kanban-rememory"], cwd=root)
    with zipfile.ZipFile(target, "a") as kit:
        kit.writestr(f"{folder}/kanban-rememory/VERSION", f"{version}\n")
        kit.writestr(f"{folder}/kanban-rememory/orchestrator/templates/GUARDRAILS.md",
                     subprocess.check_output(["git", "show", "HEAD:GUARDRAILS.md"], cwd=root))
    start = subprocess.check_output(["git", "show", "HEAD:kanban-rememory/orchestrator/templates/start.md"], cwd=root, text=True)
    (target.parent / "START.md").write_text(start.format(version=version, zip=target.name, folder=folder))
    return target


def main(argv=None, root=ROOT):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) > 1:
        raise SystemExit("usage: build-kit.py [output.zip]")
    try:
        print(build(root, argv[0] if argv else None))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Cannot build the kit: {error}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
