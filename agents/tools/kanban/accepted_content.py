"""Keep acceptance tied to the product content that will be published."""

import os
from pathlib import PurePosixPath
import subprocess

from .project import parse_manifest


class StaleAcceptance(ValueError):
    pass


def git(root, *args):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Could not compare Git trees.")
    return result.stdout


def verify_accepted_content(root, accepted, closing):
    """Compare committed paths, including changes in mode, type, and presence."""
    manifest = git(root, "ls-tree", closing, "--", "project.json").split()
    if len(manifest) != 4 or manifest[0] not in (b"100644", b"100755") or manifest[1] != b"blob":
        raise ValueError("The closing revision must contain a regular project.json.")
    project = parse_manifest(root, git(root, "cat-file", "blob", manifest[2].decode("ascii")), resolve_paths=False)

    def relative(path):
        return PurePosixPath(path.relative_to(root).as_posix())

    sources = tuple(map(relative, project.sources))
    memory = relative(project.memory)
    modules = tuple(map(relative, project.modules.values()))
    changed = git(root, "diff", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none",
                  "--no-renames", "--name-only", "-z", accepted, closing, "--")
    for name in changed.split(b"\0"):
        if not name:
            continue
        path = PurePosixPath(os.fsdecode(name))
        if not tracking_record(path, memory, modules, sources):
            raise StaleAcceptance(
                f"The combined product differs from the accepted candidate at {path.as_posix()!r}. "
                "Repeat affected acceptance checks and record a decision for the new candidate."
            )


def tracking_record(path, memory, modules, sources):
    if any(path.is_relative_to(source) for source in sources):
        return False
    if path != memory and path.is_relative_to(memory):
        return path.suffix == ".md"
    for module in modules:
        if path == module or not path.is_relative_to(module):
            continue
        directory, *parts = path.relative_to(module).parts
        if directory in {"batches", "lots", "Lots"}:
            return path.suffix == ".md" or (len(parts) >= 3 and parts[1] == "evidence")
        if directory in {"kanban", "rememory"}:
            return path.suffix == ".md"
        return directory == "specs" and path.suffix == ".md" and parts[:1] != ["resources"]
    return False
