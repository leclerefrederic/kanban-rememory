"""Keep acceptance tied to the product content that will be published."""

import json
import os
from pathlib import PurePosixPath
import subprocess

from .files import CARD_ID, header_value
from .project import PROJECT_SCOPE, parse_manifest
from .specifications import SPECIFICATION_NAMES
from .workflow import check_workflow


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
    board = PurePosixPath("project/kanban")
    changed = git(root, "diff", "--no-ext-diff", "--no-textconv", "--ignore-submodules=none",
                  "--no-renames", "--name-only", "-z", accepted, closing, "--")
    for name in changed.split(b"\0"):
        if not name:
            continue
        path = PurePosixPath(os.fsdecode(name))
        if path.is_relative_to(board) and not any(path.is_relative_to(source) for source in sources):
            tracking = committed_card_change(root, accepted, closing, board, path, project.modules)
        else:
            tracking = tracking_record(path, memory, modules, sources)
        if not tracking:
            raise StaleAcceptance(
                f"The combined product differs from the accepted candidate at {path.as_posix()!r}. "
                "Repeat affected acceptance checks and record a decision for the new candidate."
            )


def committed_card_change(root, accepted, closing, board, path, modules):
    name = CARD_ID.match(path.stem)
    if len(path.relative_to(board).parts) != 2 or path.suffix != ".md" or name is None:
        return False
    try:
        workflow = check_workflow(json.loads(git(root, "show", f"{closing}:{board}/workflow.json")))
        if path.parent.name not in workflow["stages"]:
            return False
        for revision in (accepted, closing):
            entry = git(root, "ls-tree", revision, "--", path.as_posix()).split()
            if not entry:
                continue
            if entry[:2] != [b"100644", b"blob"]:
                return False
            source = git(root, "cat-file", "blob", entry[2].decode("ascii")).decode("utf-8")
            if (header_value(source, "type") != "card" or header_value(source, "id") != name[1]
                    or header_value(source, "scope") not in (PROJECT_SCOPE, *modules)):
                return False
    except (ValueError, KeyError):
        return False
    return True


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
        return directory in SPECIFICATION_NAMES and path.suffix == ".md" and parts[:1] != ["resources"]
    return False
