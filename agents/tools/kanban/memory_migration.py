"""Plan and resume the move to centralized Rememory journals."""

from base64 import b64decode, b64encode
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Optional
from urllib.parse import quote, unquote, urlsplit

from .coordination import exclusive
from .files import HEADING, LINK, markdown_files, prose_lines
from .project import coordination_root, load_project
from .specifications import SPECIFICATION_NAMES


FORWARD = "<!-- kr-rememory-forward -->"


@dataclass(frozen=True)
class Change:
    path: Path
    before: Optional[bytes]
    after: Optional[bytes]
    mode: int = 0o644


def local_path(root, path):
    """Validate each ancestor before reading, writing or unlinking a path."""
    if not path.is_relative_to(root) or path.resolve() != path:
        raise ValueError(f"Expected a local Rememory migration path: {path}.")
    return path


def read(path):
    if not path.exists():
        return None
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Expected a regular file: {path}.")
    return path.read_bytes()


def journal_moves(project):
    directories = [(project.memory, project.memory / "project")]
    directories.extend((workspace / "rememory", project.memory / "modules" / name)
                       for name, workspace in project.modules.items())
    moved = {}
    clear_placeholders = set()
    for source, target in directories:
        for directory in (source, target):
            local_path(project.root, directory)
            if directory.exists() and not directory.is_dir():
                raise ValueError(f"Expected a journal directory: {directory}.")
        for path in sorted(source.glob("*.md")):
            local_path(project.root, path)
            content = read(path)
            if content.startswith(FORWARD.encode()):
                continue
            destination = local_path(project.root, target / path.name)
            if destination.exists():
                raise ValueError(f"Journal collision: {destination.relative_to(project.root)}.")
            moved[path] = destination
        if source != project.memory and (source / ".gitkeep").exists():
            path = local_path(project.root, source / ".gitkeep")
            if read(path) == b"":
                clear_placeholders.add(path)
    return directories, moved, clear_placeholders


def protected_document(document, project):
    for workspace in (project.board, *project.modules.values()):
        for name in SPECIFICATION_NAMES:
            if document.is_relative_to(workspace / name):
                return True
        for name in ("batches", "lots", "Lots"):
            if document.is_relative_to(workspace / name):
                return True
        if document.is_relative_to(workspace / "kanban"):
            # Only an uncompleted Card may have its link rewritten by migration.
            archived = project.archived_stages(workspace)
            return document.parent.name in archived
    return False


def forbidden_document(document, project):
    return any(document.is_relative_to(workspace / name / stage)
               for workspace in (project.board, *project.modules.values())
               for name in SPECIFICATION_NAMES for stage in ("draft", "ready"))


def rewrite_links(source, document, destination, moved, frozen, forwards):
    lines = source.splitlines(keepends=True)
    for index, line in prose_lines(lines):
        code = [match.span() for match in re.finditer(r"`+[^`]*`+", line)]

        def rewrite(match):
            if any(a <= match.start() < b for a, b in code):
                return match[0]
            href = match[1] or match[2]
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
                return match[0]
            old = (document.parent / unquote(url.path)).resolve()
            if old in moved and frozen:
                forwards.setdefault(old, set()).add(unquote(url.fragment))
                return match[0]
            target = moved.get(old, old)
            if (destination.parent / unquote(url.path)).resolve() == target:
                return match[0]
            relative = quote(os.path.relpath(target, destination.parent), safe="/")
            if url.path.endswith("/"):
                relative += "/"
            group = 1 if match[1] is not None else 2
            start = match.start(group) - match.start()
            return match[0][:start] + relative + match[0][start + len(url.path):]

        lines[index] = LINK.sub(rewrite, line)
    return "".join(lines)


def plan(project):
    root = project.root
    directories, moved, placeholders = journal_moves(project)
    edits = {}
    forwards = {}
    for _, target in directories:
        path = local_path(root, target / ".gitkeep")
        if not target.exists() and not any(destination.parent == target for destination in moved.values()):
            edits[path] = Change(path, None, b"")
    docs = set(markdown_files(root=root)) | set(moved)
    for path in sorted(docs):
        if path.is_relative_to(root / "Archives") or forbidden_document(path, project):
            continue
        frozen = protected_document(path, project)
        original = read(path)
        target = moved.get(path, path)
        rewritten = rewrite_links(original.decode("utf-8"), path, target,
                                  moved, frozen, forwards).encode("utf-8")
        if target != path or rewritten != original:
            local_path(root, target)
            edits[target] = Change(target, original if target == path else None,
                                   rewritten, stat.S_IMODE(path.stat().st_mode))
    for path in sorted(placeholders | set(moved)):
        content = read(path)
        pointer = None
        if path in forwards:
            relative = quote(os.path.relpath(moved[path], path.parent), safe="/")
            body = f"{FORWARD}\n\n[Read this journal at its current location]({relative}).\n"
            if any(forwards[path]):
                seen = set()
                for _, line in prose_lines(content.decode("utf-8").splitlines()):
                    heading = HEADING.match(line)
                    if not heading:
                        continue
                    slug = re.sub(r"[^\w -]", "", heading[2].lower()).replace(" ", "-")
                    anchor, suffix = slug, 1
                    while anchor in seen:
                        anchor = f"{slug}-{suffix}"
                        suffix += 1
                    seen.add(anchor)
                    body += f"\n{line}\n\n[Read this entry]({relative}#{quote(anchor)}).\n"
            pointer = body.encode("utf-8")
        edits[path] = Change(path, content, pointer, stat.S_IMODE(path.stat().st_mode))
    return list(edits.values())


def replace(path, content, mode):
    if content is None:
        path.unlink()
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".rememory-", delete=False) as handle:
        staged = Path(handle.name)
        handle.write(content)
    try:
        staged.chmod(mode)
        staged.replace(path)
    finally:
        staged.unlink(missing_ok=True)


def save(root, checkpoint, changes):
    def encode(content):
        return None if content is None else b64encode(content).decode("ascii")

    records = [[item.path.relative_to(root).as_posix(), encode(item.before),
                encode(item.after), item.mode] for item in changes]
    replace(checkpoint, json.dumps(records).encode("utf-8"), 0o600)


def resume(root, checkpoint):
    def decode(content):
        return None if content is None else b64decode(content, validate=True)

    return [Change(local_path(root, root / path), decode(before), decode(after), mode)
            for path, before, after, mode in json.loads(read(checkpoint))]


def apply_changes(root, changes):
    for item in changes:
        local_path(root, item.path)
        if read(item.path) not in (item.before, item.after):
            raise ValueError(f"Journal migration found an intervening edit: {item.path}.")
    for item in changes:
        if read(item.path) != item.after:
            replace(item.path, item.after, item.mode)
    for parent in {item.path.parent for item in changes if item.after is None}:
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()


def checkpoint_path(root, project_id):
    """Name the migration state for this checkout, even when Git is shared."""
    root = Path(root).resolve()
    directory = coordination_root(root) / "projects" / project_id
    checkout = hashlib.sha256(os.fsencode(root)).hexdigest()
    return directory / f"rememory-migration-{checkout}.json"


def migrate(root, apply=False):
    project = load_project(root)
    if project.flat_board:
        raise ValueError("Project settings already use one flat Rememory journal directory.")
    root = project.root
    checkpoint = checkpoint_path(root, project.id)

    def run():
        pending = checkpoint.exists() or checkpoint.is_symlink()
        changes = resume(root, checkpoint) if pending else plan(project)
        for item in changes:
            action = "Remove" if item.after is None else ("Create" if item.before is None else "Update")
            print(f"{action} {item.path.relative_to(root).as_posix()}")
        if not changes:
            print("Rememory journals already use the centralized layout.")
        elif not apply:
            print("Preview only. Run again with --apply after approval.")
        else:
            if not pending:
                save(root, checkpoint, changes)
            apply_changes(root, changes)
            checkpoint.unlink()
            print("Rememory journals migrated.")

    if not apply:
        run()
    else:
        with exclusive(checkpoint.parent, "journal-update"):
            run()
