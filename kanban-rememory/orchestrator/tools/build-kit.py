"""Build the installation kit as a ZIP archive from the committed files of HEAD."""

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
KIT_FILES = ("kanban-rememory", "kanban-rememory.json", "AGENTS.md", "CLAUDE.md", "GUARDRAILS.md")


def build(root, output=None):
    """Write dist/kanban-rememory-kit-<version>.zip, or output, and return its path."""
    config = subprocess.check_output(["git", "show", "HEAD:kanban-rememory.json"], cwd=root)
    version = json.loads(config)["version"]
    folder = f"kanban-rememory-kit-{version}"
    target = Path(output) if output else root / "dist" / f"{folder}.zip"
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "archive", "--format=zip", f"--prefix={folder}/", "-o", str(target),
                           "HEAD", "--", *KIT_FILES], cwd=root)
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
