"""Build the installation kit as a ZIP archive from the committed files of HEAD.

The kit sits under kanban-rememory/, the one folder the install replaces; installer/init.py, the installation script,
is the only other file. Both stay inside the archive's own folder. kanban-rememory.json is this repository's own configuration and stays out; VERSION
carries the kit version and the GUARDRAILS.md template is the file of HEAD."""

import json
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]


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
        kit.writestr(f"{folder}/installer/init.py",
                     subprocess.check_output(["git", "show", "HEAD:dist/installer/init.py"], cwd=root))
        kit.writestr(f"{folder}/kanban-rememory/VERSION", f"{version}\n")
        kit.writestr(f"{folder}/kanban-rememory/orchestrator/templates/GUARDRAILS.md",
                     subprocess.check_output(["git", "show", "HEAD:GUARDRAILS.md"], cwd=root))
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
