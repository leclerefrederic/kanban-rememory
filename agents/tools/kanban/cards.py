"""Card creation, display, and guarded moves."""

from contextlib import contextmanager
from collections import Counter
from datetime import date, datetime
import json
import os
import re
from unicodedata import normalize
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo

from .batches import is_closed_lot_report, relationship, validate_lot_mapping
from .coordination import replace_text
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, cards, field,
                    header_value, markdown_files, markdown_lines, prose_lines)
from .project import PROJECT_SCOPE
from .validation import FROZEN_CARD_MOVE_LINKS


def scoped_cards(stage, project, context=None, scope=None):
    """Read current Cards on the shared board, or all Cards in a simple project."""
    for path in cards(stage, project):
        if context is None:
            yield path
            continue
        found = context.card_scope(path, allow_legacy=True)
        if found is not None and (scope is None or found == scope):
            yield path


def find_card(workflow, task_id, project=PROJECT, context=None):
    matches = [(stage, path) for stage in workflow["stages"]
               for path in cards(stage, project)
               if CARD_ID.match(path.stem)[1].upper() == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one current card for {task_id}, found {len(matches)}.")
    stage, path = matches[0]
    if context and context.card_scope(path, allow_legacy=True) is None:
        raise ValueError(f"{task_id} is an unscoped historical record. Use history or an approved migration.")
    return stage, path


def show_board(workflow, limit, today, project=PROJECT, root=ROOT, *, context=None, scope=None):
    wip = Counter()
    for stage in workflow["stages"]:
        print(stage)
        for path in scoped_cards(stage, project, context, scope):
            source = path.read_text(encoding="utf-8")
            card_scope = context.card_scope(path) if context else None
            heading = next((line[2:] for line in markdown_lines(source)
                            if line.startswith("# ")), path.stem)
            task_id = CARD_ID.match(path.stem)[1].upper()
            title = heading.removeprefix(task_id).lstrip(" —-")
            scope_column = f"{card_scope} | " if context else ""
            print(f"  {task_id} | {scope_column}{title} | {path.relative_to(root)}")
            if stage in workflow["active"]:
                wip[card_scope] += 1
                try:
                    age = f"{(today - date.fromisoformat(field(source, 'Actual start'))).days} days"
                except ValueError:
                    age = "unknown"
                print(f"    Age: {age}")
                state = field(source, "State")
                if state:
                    print(f"    State: {state}")
                blocker = field(source, "Blocker")
                if blocker:
                    print(f"    Blocker: {blocker}")
    if context and scope is None:
        for item in (PROJECT_SCOPE, *context.modules):
            print(f"{item} WIP: {wip[item]}/{limit} | Available slots: {max(0, limit - wip[item])}")
    else:
        print(f"WIP: {wip[scope]}/{limit} | Available slots: {max(0, limit - wip[scope])}")
    return 0


def rewrite_card_links(source, document, card, target, root=ROOT):
    new_document = target if document == card else document
    lines = source.splitlines(keepends=True)
    for index, line in prose_lines(lines):
        code_spans = [match.span() for match in re.finditer(r"`+[^`]*`+", line)]

        def rewrite(match):
            if any(start <= match.start() < end for start, end in code_spans):
                return match[0]
            href = match[1] or match[2]
            url = urlsplit(href)
            if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
                return match[0]
            old_destination = (document.parent / unquote(url.path)).resolve()
            if old_destination == card:
                if (document.relative_to(root).as_posix(), href) in FROZEN_CARD_MOVE_LINKS:
                    return match[0]
                destination = target
            elif document == card:
                destination = old_destination
                if (target.parent / unquote(url.path)).resolve() == destination:
                    return match[0]
            else:
                return match[0]
            relative = quote(os.path.relpath(destination, new_document.parent), safe="/")
            if url.path.endswith("/"):
                relative += "/"
            group = 1 if match[1] is not None else 2
            start = match.start(group) - match.start()
            return match[0][:start] + relative + match[0][start + len(url.path):]

        lines[index] = LINK.sub(rewrite, line)
    return "".join(lines)


def relocate_card(card, target, completed, transition, project=PROJECT, root=ROOT, *, context=None, scope=None):
    updates = {}
    documents = markdown_files(None if project == root / "project" else project, root)
    for document in set(documents) | {card}:
        original = document.read_bytes()
        source = original.decode("utf-8")
        updated = rewrite_card_links(source, document, card, target, root)
        if document == card and header_value(source, "type") == "card":
            updated = updated.rstrip()
            if not re.search(r"^## History$", updated, re.MULTILINE):
                updated += "\n\n## History"
            updated += f"\n\n- {transition}\n"
        if source != updated:
            if context and document != card:
                same_scope_card = (document.is_relative_to(project / "kanban")
                                   and CARD_ID.match(document.stem)
                                   and context.card_scope(document, allow_legacy=True) == scope)
                local_journal = document.is_relative_to(context.scope_memory(scope))
                if not (same_scope_card or local_journal):
                    raise ValueError(f"Move would rewrite a protected record: {document.relative_to(root)}. Use a stable Card ID.")
            if project != root / "project" and not any(
                document.is_relative_to(project / directory) for directory in ("kanban", "rememory")
            ):
                raise ValueError(f"Move would rewrite a protected record: {document.relative_to(root)}. Use a qualified Card reference.")
            if (document.parent == completed and CARD_ID.match(document.stem)) or is_closed_lot_report(document, project):
                raise ValueError(f"Move would rewrite immutable history: {document.relative_to(root)}")
            updates[target if document == card else document] = (original, updated.encode("utf-8"))

    card.rename(target)
    attempted = []
    try:
        for document, (original, updated) in updates.items():
            attempted.append((document, original))
            document.write_bytes(updated)
    except OSError:
        for document, original in reversed(attempted):
            if document.read_bytes() != original:
                document.write_bytes(original)
        target.rename(card)
        raise


def move_card(workflow, task_id, destination, project=PROJECT, root=ROOT, authorize_active=None,
              *, context=None, scope=None):
    stage, card = find_card(workflow, task_id, project, context)
    if context:
        actual_scope = context.card_scope(card)
        if actual_scope != scope:
            raise ValueError(f"{task_id} belongs to scope {actual_scope}, not {scope}.")
        if scope == PROJECT_SCOPE and relationship(card.read_text(encoding="utf-8"), "batch"):
            raise ValueError("A Batch Card must have the same module scope as its Batch.")
        if findings := validate_lot_mapping((card,), context.scope_workspace(scope), root):
            raise ValueError("\n".join(findings))
    if stage == workflow["completed"]:
        raise ValueError("Completed cards are immutable. Create a follow-up card.")
    if "transitions" not in workflow:
        raise ValueError("Configure transitions in kanban/workflow.json before moving cards.")
    if destination not in workflow["transitions"].get(stage, []):
        raise ValueError(f"Transition from {stage} to {destination} is not allowed.")
    active = workflow["active"]
    if authorize_active and (stage in active or destination in active):
        source = card.read_text(encoding="utf-8")
        delivery = header_value(source, "batch") or task_id
        authorize_active(delivery)
    if destination in active and stage not in active:
        if sum(1 for column in active for _ in scoped_cards(column, project, context, scope)) >= workflow["wip_limit"]:
            raise ValueError("WIP limit reached. Finish active work before starting another card.")
    if destination == workflow["completed"]:
        checks = list(acceptance_checks(card.read_text(encoding="utf-8")))
        if not checks or any(re.match(r"[-*+]\s+\[ \]", check) for check in checks):
            raise ValueError("Completion requires a nonempty acceptance checklist with every item checked.")
    target = project / "kanban" / destination / card.name
    if target.exists() or target.is_symlink():
        raise ValueError(f"Destination already exists: {target.relative_to(root)}")
    timestamp = datetime.now(ZoneInfo(workflow["timezone"])).isoformat(timespec="seconds")
    transition = f"{timestamp} — Stage moved from `{stage}` to `{destination}`."
    relocate_card(card, target, project / "kanban" / workflow["completed"], transition, project, root,
                  context=context, scope=scope)
    print(f"Moved {task_id} from {stage} to {destination}.")
    return 0


def reassign_card(workflow, task_id, context, new_scope, is_claimed):
    stage, path = find_card(workflow, task_id, context.board, context)
    old_scope = context.card_scope(path)
    if stage != workflow.get("intake", workflow["stages"][0]) or is_claimed(old_scope):
        raise ValueError("Scope can be reassigned only while the Card is unclaimed in backlog.")
    if old_scope == new_scope:
        print(f"{task_id} already has scope {new_scope}.")
        return 0
    source = path.read_text(encoding="utf-8")
    if relationship(source, "batch") or relationship(source, "specifications"):
        raise ValueError("Resolve Batch and Specification references before reassigning the Card.")
    marker = source.index("\n---", 4)
    header, count = re.subn(r"(?m)^scope:[^\n]*", lambda _: f"scope: {json.dumps(new_scope)}",
                            source[:marker], count=1)
    if count != 1:
        raise ValueError("Expected one scoped Card header.")
    timestamp = datetime.now(ZoneInfo(workflow["timezone"])).isoformat(timespec="seconds")
    updated = (header + source[marker:]).rstrip()
    if not re.search(r"^## History$", updated, re.MULTILINE):
        updated += "\n\n## History"
    replace_text(path, f"{updated}\n\n- {timestamp} — Scope reassigned from `{old_scope}` to `{new_scope}`.\n")
    print(f"Reassigned {task_id} to scope {new_scope}.")
    return 0


@contextmanager
def board_write_lock(project=PROJECT):
    lock = project / "kanban/.write-lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError("Another board write holds kanban/.write-lock. Retry after it finishes.") from None
    try:
        yield
    finally:
        lock.rmdir()


def create_card(workflow, args, project=PROJECT, root=ROOT, *, scope=None, write_lock=None):
    title, owner = args.title.strip(), args.owner.strip()
    if not title or not owner or len(title.splitlines()) != 1 or len(owner.splitlines()) != 1:
        raise ValueError("Title and owner must each be a nonempty single line.")
    entry = workflow.get("intake", workflow["stages"][0])
    if entry not in workflow["stages"] or entry in workflow["active"] or entry == workflow["completed"]:
        raise ValueError("Configure an intake stage outside active and completed work.")

    template_path = ROOT / "agents/templates/card.md"
    if not template_path.exists():
        template_path = ROOT / "agents/templates/kanban-card.md"
    if not template_path.is_file():
        template_path = ROOT / "docs/templates/kanban-card.md"
    if not template_path.is_file():
        template_path = ROOT / "docs/templates/card.md"
    if not template_path.is_file():
        template_path = ROOT / "docs/lot-templates/Card.md"
    if not template_path.is_file():
        template_path = ROOT / "docs/task-template.md"
    template = template_path.read_text(encoding="utf-8")
    slug = normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")[:80].rstrip("-") or "task"

    def prepare():
        highest = 0
        seen = set()
        stages = workflow["stages"]
        if scope is not None:
            stages = [path.name for path in (project / "kanban").iterdir() if path.is_dir()]
        for stage in stages:
            for card in cards(stage, project):
                task_id = CARD_ID.match(card.stem)[1].upper()
                if task_id in seen:
                    raise ValueError(f"Duplicate {task_id}. Resolve the collision before creating a card.")
                seen.add(task_id)
                if task_id.startswith(("CARD-", "TASK-")):
                    highest = max(highest, int(task_id.split("-")[1]))
        if highest >= 99999999:
            raise ValueError("The eight-digit CARD range is exhausted.")
        task_id = f"CARD-{highest + 1:08d}"
        target = project / "kanban" / entry / f"{task_id.lower()}-{slug}.md"
        content = re.sub(r'^id: "(?:CARD|TASK)-NNNNNNNN"$', lambda _: f'id: "{task_id}"',
                         template, count=1, flags=re.MULTILINE)
        if scope is not None:
            content = content.replace(f'id: "{task_id}"\n', f'id: "{task_id}"\nscope: {json.dumps(scope)}\n', 1)
        content = re.sub(r"^# (?:CARD|TASK)-NNNNNNNN(?: — Short title)?$", lambda _: f"# {task_id} — {title}",
                         content, count=1, flags=re.MULTILINE)
        content = re.sub(r"^- Owner:[^\n]*$", lambda _: f"- Owner: {owner}",
                         content, count=1, flags=re.MULTILINE)
        return target, content

    if not args.apply:
        target, content = prepare()
        print(f"Preview {target.relative_to(root)}:\n\n{content}")
        print("Run again with --apply once the project intake rules permit recording the backlog Card.")
        return 0

    with (write_lock if write_lock is not None else board_write_lock(project)):
        target, content = prepare()
        with target.open("x", encoding="utf-8") as stream:
            stream.write(content)
    print(f"Created {target.relative_to(root)}.")
    return 0
