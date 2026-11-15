"""Retire exactly the new-format Specifications approved for one delivery."""

from pathlib import Path
import re
import subprocess

from .batches import fiche_entries
from .files import header_value
from .specifications import SPECIFICATION_NAMES

FULL_REVISION = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")


def git(root, *args):
    result = subprocess.run(["git", *args], cwd=root, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip() or "Could not read Git approval.")
    return result.stdout


def retirement_paths(source, workspace):
    for entry in fiche_entries(source):
        if len(entry) not in (3, 4):
            raise ValueError("Expected a Specification ID, approval path and valid legacy fields.")
        identifier, revision, pinned = entry[:3]
        if revision is not None:
            continue
        if not isinstance(identifier, str) or not re.fullmatch(r"SPEC-[0-9]{3,}", identifier):
            raise ValueError("Retirement requires a valid Specification ID.")
        if not isinstance(pinned, str):
            raise ValueError("Retirement requires a pinned Specification path.")
        original = Path(pinned)
        if pinned not in {
            (workspace / name / "approved" / f"{identifier.lower()}.md").as_posix()
            for name in SPECIFICATION_NAMES
        }:
            raise ValueError(f"Expected the approved Specification path for {identifier}.")
        yield original, original.parent.parent / "retired" / original.name


def approval_paths(root, workspace, description, source, approval):
    current = list(retirement_paths(source, workspace))
    if not current and approval is None:
        return []
    if not isinstance(approval, str) or not FULL_REVISION.fullmatch(approval):
        raise ValueError("Retirement requires the full trusted Batch approval commit.")
    if git(root, "cat-file", "-t", approval).strip() != b"commit":
        raise ValueError("The trusted Batch approval commit is unavailable.")
    approved = git(root, "show", f"{approval}:{description.as_posix()}").decode("utf-8")
    if (header_value(approved, "status") != "ready"
            or header_value(approved, "id") != header_value(source, "id")
            or list(fiche_entries(approved)) != list(fiche_entries(source))):
        raise ValueError("Closing Specification pins must match the trusted Batch approval.")
    if len({old for old, _ in current}) != len(current):
        raise ValueError("A Batch must select each Specification at most once.")
    return current


def tree_entry(root, revision, file):
    return git(root, "ls-tree", revision, "--", file.as_posix()).split(None, 3)[:3]


def approved_specification(root, approval, original):
    entry = tree_entry(root, approval, original)
    if len(entry) != 3 or entry[0] != b"100644" or entry[1] != b"blob":
        raise ValueError(f"Missing regular Specification in approval: {original}.")
    return entry


def verify_retirement(root, workspace, description, source, approval, closing):
    for original, retired in approval_paths(root, workspace, description, source, approval):
        for parent in retired.parents:
            if parent == Path("."):
                break
            entry = tree_entry(root, closing, parent)
            if entry and entry[:2] != [b"040000", b"tree"]:
                raise ValueError(f"Expected a local retirement directory: {parent}.")
        if (tree_entry(root, closing, original)
                or tree_entry(root, closing, retired) != approved_specification(root, approval, original)):
            raise ValueError(f"Close the Batch with its exact approved Specification retired: {retired}.")


def retire_batch_specifications(root, workspace, description, approval):
    source = (root / description).read_text(encoding="utf-8")
    if header_value(source, "status") not in {"validated", "rejected"}:
        raise ValueError("Retire Specifications when closing a decided Batch.")
    moves = []
    paths = approval_paths(root, workspace, description, source, approval)
    for original, retired in paths:
        src, dest = root / original, root / retired
        if src.resolve() != src or dest.resolve() != dest:
            raise ValueError(f"Specification retirement paths cannot contain symbolic links: {original}.")
        entry = approved_specification(root, approval, original)
        approved = git(root, "cat-file", "blob", entry[2].decode("ascii"))
        if not src.exists() and dest.is_file() and dest.read_bytes() == approved:
            continue
        if not src.is_file() or src.read_bytes() != approved or dest.exists():
            raise ValueError(f"Expected the exact approved Specification and an unused archive path: {original}.")
        if dest.parent.exists() and not dest.parent.is_dir():
            raise ValueError(f"Expected a directory for retired Specifications: {dest.parent}.")
        moves.append((src, dest))
    for src, dest in moves:
        dest.parent.mkdir(exist_ok=True)
        src.rename(dest)
    return [retired.as_posix() for _, retired in paths]
