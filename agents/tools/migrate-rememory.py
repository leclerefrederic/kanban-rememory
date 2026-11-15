"""Preview or apply the centralized Rememory migration in this checkout."""

import argparse
import subprocess

from kanban.files import ROOT
from kanban.memory_migration import migrate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        migrate(ROOT, args.apply)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
