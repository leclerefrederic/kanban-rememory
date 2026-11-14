"""Copy the kit skills from agents/skills/ into the discovery folders of Claude Code and Codex."""

import argparse
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"claude": ".claude/skills", "codex": ".agents/skills"}


def files(folder):
    return {path.relative_to(folder): path.read_bytes() for path in folder.rglob("*") if path.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--check", action="store_true", help="Report differences without writing.")
    args = parser.parse_args()
    sources = sorted(path for path in (ROOT / "agents/skills").iterdir() if (path / "SKILL.md").is_file())
    if not sources:
        sys.exit("No skill found in agents/skills/.")
    differences = []
    for key, relative in TARGETS.items():
        if args.target not in (key, "both"):
            continue
        for source in sources:
            destination = ROOT / relative / source.name
            if not destination.is_dir() or files(source) != files(destination):
                differences.append(f"{relative}/{source.name}")
                if not args.check:
                    shutil.rmtree(destination, ignore_errors=True)
                    shutil.copytree(source, destination)
    version = (ROOT / "agents/VERSION").read_text().strip()
    if args.check:
        if differences:
            sys.exit("Out of date (kit " + version + "): " + ", ".join(differences))
        print(f"Skills match kit {version}.")
    else:
        print(f"Kit {version}: updated {len(differences)} skill folder(s)" + (": " + ", ".join(differences) if differences else "."))


if __name__ == "__main__":
    main()
