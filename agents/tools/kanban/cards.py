"""Card creation, display, and guarded moves."""

from contextlib import contextmanager
from datetime import date, datetime
import os
import re
from unicodedata import normalize
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo

from .batches import is_closed_lot_report
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, cards, field,
                    header_value, markdown_files, markdown_lines, prose_lines)


def show_board(workflow, limit, today):
    wip = 0
    for stage in workflow["stages"]:
        print(stage)
        for path in cards(stage):
            source = path.read_text(encoding="utf-8")
            heading = next((line[2:] for line in markdown_lines(source)
                            if line.startswith("# ")), path.stem)
            task_id = CARD_ID.match(path.stem)[1].upper()
            title = heading.removeprefix(task_id).lstrip(" —-")
            print(f"  {task_id} | {title} | {path.relative_to(ROOT)}")
            if stage in workflow["active"]:
                wip += 1
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
    print(f"WIP: {wip}/{limit} | Available slots: {max(0, limit - wip)}")
    return 0


def rewrite_card_links(source, document, card, target):
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


def relocate_card(card, target, completed, transition):
    updates = {}
    for document in set(markdown_files()) | {card}:
        original = document.read_bytes()
        source = original.decode("utf-8")
        updated = rewrite_card_links(source, document, card, target)
        if document == card and header_value(source, "type") == "card":
            updated = updated.rstrip()
            if not re.search(r"^## History$", updated, re.MULTILINE):
                updated += "\n\n## History"
            updated += f"\n\n- {transition}\n"
        if source != updated:
            if (document.parent == completed and CARD_ID.match(document.stem)) or is_closed_lot_report(document):
                raise ValueError(f"Move would rewrite immutable history: {document.relative_to(ROOT)}")
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


def move_card(workflow, task_id, destination):
    matches = [(stage, card) for stage in workflow["stages"] for card in cards(stage)
               if CARD_ID.match(card.stem)[1].upper() == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one card for {task_id}, found {len(matches)}.")
    stage, card = matches[0]
    if stage == workflow["completed"]:
        raise ValueError("Completed cards are immutable. Create a follow-up card.")
    if "transitions" not in workflow:
        raise ValueError("Configure transitions in kanban/workflow.json before moving cards.")
    if destination not in workflow["transitions"].get(stage, []):
        raise ValueError(f"Transition from {stage} to {destination} is not allowed.")
    active = workflow["active"]
    if destination in active and stage not in active:
        if sum(len(cards(column)) for column in active) >= workflow["wip_limit"]:
            raise ValueError("WIP limit reached. Finish active work before starting another card.")
    if destination == workflow["completed"]:
        checks = list(acceptance_checks(card.read_text(encoding="utf-8")))
        if not checks or any(re.match(r"[-*+]\s+\[ \]", check) for check in checks):
            raise ValueError("Completion requires a nonempty acceptance checklist with every item checked.")
    target = PROJECT / "kanban" / destination / card.name
    if target.exists() or target.is_symlink():
        raise ValueError(f"Destination already exists: {target.relative_to(ROOT)}")
    timestamp = datetime.now(ZoneInfo(workflow["timezone"])).isoformat(timespec="seconds")
    transition = f"{timestamp} — Stage moved from `{stage}` to `{destination}`."
    relocate_card(card, target, PROJECT / "kanban" / workflow["completed"], transition)
    print(f"Moved {task_id} from {stage} to {destination}.")
    return 0


@contextmanager
def board_write_lock():
    lock = PROJECT / "kanban/.write-lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError("Another board write holds kanban/.write-lock. Retry after it finishes.") from None
    try:
        yield
    finally:
        lock.rmdir()


def create_card(workflow, args):
    title, owner = args.title.strip(), args.owner.strip()
    if not title or not owner or len(title.splitlines()) != 1 or len(owner.splitlines()) != 1:
        raise ValueError("Title and owner must each be a nonempty single line.")
    entry = workflow.get("intake", workflow["stages"][0])
    if entry not in workflow["stages"] or entry in workflow["active"] or entry == workflow["completed"]:
        raise ValueError("Configure an intake stage outside active and completed work.")

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
        for stage in workflow["stages"]:
            for card in cards(stage):
                task_id = CARD_ID.match(card.stem)[1].upper()
                if task_id in seen:
                    raise ValueError(f"Duplicate {task_id}. Resolve the collision before creating a card.")
                seen.add(task_id)
                if task_id.startswith("TASK-"):
                    highest = max(highest, int(task_id.split("-")[1]))
        if highest >= 99999999:
            raise ValueError("The eight-digit TASK range is exhausted.")
        task_id = f"TASK-{highest + 1:08d}"
        target = PROJECT / "kanban" / entry / f"{task_id.lower()}-{slug}.md"
        content = template.replace('id: "TASK-NNNNNNNN"', f'id: "{task_id}"', 1)
        content = re.sub(r"^# TASK-NNNNNNNN(?: — Short title)?$", lambda _: f"# {task_id} — {title}",
                         content, count=1, flags=re.MULTILINE)
        content = re.sub(r"^- Owner:[^\n]*$", lambda _: f"- Owner: {owner}",
                         content, count=1, flags=re.MULTILINE)
        return target, content

    if not args.apply:
        target, content = prepare()
        print(f"Preview {target.relative_to(ROOT)}:\n\n{content}")
        print("Run again with --apply after backlog approval.")
        return 0

    with board_write_lock():
        target, content = prepare()
        with target.open("x", encoding="utf-8") as stream:
            stream.write(content)
    print(f"Created {target.relative_to(ROOT)}.")
    return 0
