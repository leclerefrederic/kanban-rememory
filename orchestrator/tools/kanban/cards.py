"""Card creation, display, and guarded moves."""

from collections import Counter
from datetime import date, datetime
import json
import os
import re
from unicodedata import normalize
from urllib.parse import quote, unquote, urlsplit
from zoneinfo import ZoneInfo

from .files import (CARD_ID, LINK, ROOT, acceptance_checks, board_cards, field,
                    header_value, markdown_files, markdown_lines, prose_lines)
from .project import MISC


def card_id(path):
    return CARD_ID.match(path.stem)[1].upper()


def scoped_cards(stage, project, scope=None):
    """Read one module board, or all of them, for one stage."""
    workspaces = (project.workspace(scope),) if scope else tuple(project.modules.values())
    for workspace in workspaces:
        for path in board_cards(stage, workspace):
            if scope is None or project.card_scope(path) == scope:
                yield path


def find_card(project, task_id):
    matches = [(stage, path) for stage in project.workflow["stages"]
               for path in scoped_cards(stage, project) if card_id(path) == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one current card for {task_id}, found {len(matches)}.")
    return matches[0]


def show_board(project, limit, today, *, scope=None):
    workflow = project.workflow
    wip = Counter()
    for stage in workflow["stages"]:
        print(stage)
        for path in scoped_cards(stage, project, scope):
            source = path.read_text(encoding="utf-8")
            card_scope = project.card_scope(path)
            heading = next((line[2:] for line in markdown_lines(source)
                            if line.startswith("# ")), path.stem)
            task_id = card_id(path)
            title = heading.removeprefix(task_id).lstrip(" —-")
            print(f"  {task_id} | {card_scope} | {title} | {path.relative_to(project.root)}")
            if stage in workflow["active"]:
                wip[card_scope] += 1
                try:
                    age = f"{(today - date.fromisoformat(field(source, 'Actual start'))).days} days"
                except ValueError:
                    age = "unknown"
                print(f"    Age: {age}")
                for label in ("State", "Blocker"):
                    value = field(source, label)
                    if value:
                        print(f"    {label}: {value}")
        if scope not in (None, MISC):
            for path in scoped_cards(stage, project, MISC):
                affected = header_value(path.read_text(encoding="utf-8"), "affected_modules")
                if isinstance(affected, list) and scope in affected:
                    print(f"  {card_id(path)} | linked from {MISC} | {path.relative_to(project.root)}")
    for item in (project.modules if scope is None else (scope,)):
        print(f"{item} WIP: {wip[item]}/{limit} | Available slots: {max(0, limit - wip[item])}")
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


def relocate_card(project, card, target, scope, transition):
    workspace = project.workspace(scope)
    completed = project.workflow["completed"]
    journal = project.journal()
    updates = {}
    for document in set(markdown_files(None, project.root)) | {card}:
        original = document.read_bytes()
        source = original.decode("utf-8")
        updated = rewrite_card_links(source, document, card, target)
        if document == card:
            updated = updated.rstrip()
            if not re.search(r"^## History$", updated, re.MULTILINE):
                updated += "\n\n## History"
            updated += f"\n\n- {transition}\n"
        if source == updated:
            continue
        if document != card:
            same_scope_card = (document.parent.parent == workspace and CARD_ID.match(document.stem)
                               and project.card_scope(document) == scope)
            if not (same_scope_card or document.is_relative_to(journal)):
                raise ValueError(f"Move would rewrite a protected record: "
                                 f"{document.relative_to(project.root)}. Use a stable Card ID.")
            if document.parent.name == completed:
                raise ValueError(f"Move would rewrite immutable history: {document.relative_to(project.root)}")
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


def move_card(project, task_id, destination, authorize_active, scope=None):
    workflow = project.workflow
    stage, card = find_card(project, task_id)
    actual_scope = project.card_scope(card)
    if scope is not None and scope != actual_scope:
        raise ValueError(f"{task_id} belongs to module {actual_scope}, not {scope}.")
    if stage == workflow["completed"]:
        raise ValueError("Completed cards are immutable. Create a follow-up card.")
    if destination not in workflow["transitions"].get(stage, []):
        raise ValueError(f"Transition from {stage} to {destination} is not allowed.")
    active = workflow["active"]
    if stage in active or destination in active:
        authorize_active(actual_scope, task_id)
    if destination in active and stage not in active:
        if sum(1 for column in active for _ in scoped_cards(column, project, actual_scope)) >= workflow["wip_limit"]:
            raise ValueError("WIP limit reached. Finish active work before starting another card.")
    if destination == workflow["completed"]:
        checks = list(acceptance_checks(card.read_text(encoding="utf-8")))
        if not checks or any(re.match(r"[-*+]\s+\[ \]", check) for check in checks):
            raise ValueError("Completion requires a nonempty acceptance checklist with every item checked.")
    target = project.workspace(actual_scope) / destination / card.name
    if target.exists() or target.is_symlink():
        raise ValueError(f"Destination already exists: {target.relative_to(project.root)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(ZoneInfo(workflow["timezone"])).isoformat(timespec="seconds")
    relocate_card(project, card, target, actual_scope,
                  f"{timestamp} — Stage moved from `{stage}` to `{destination}`.")
    print(f"Moved {task_id} from {stage} to {destination}.")
    return 0


def create_card(project, title, owner, scope, apply, write_lock):
    title, owner = title.strip(), owner.strip()
    if not title or not owner or len(title.splitlines()) != 1 or len(owner.splitlines()) != 1:
        raise ValueError("Title and owner must each be a nonempty single line.")
    workflow = project.workflow
    template = (ROOT / "orchestrator/templates/card.md").read_text(encoding="utf-8")
    slug = normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")[:80].rstrip("-") or "task"

    def prepare():
        highest = project.last_card_id
        seen = set()
        for stage in workflow["stages"]:
            for card in scoped_cards(stage, project):
                task_id = card_id(card)
                if task_id in seen:
                    raise ValueError(f"Duplicate {task_id}. Resolve the collision before creating a card.")
                seen.add(task_id)
                if task_id.startswith("CARD-"):
                    highest = max(highest, int(task_id.split("-")[1]))
        if highest >= 99999999:
            raise ValueError("The eight-digit CARD range is exhausted.")
        task_id = f"CARD-{highest + 1:08d}"
        target = project.workspace(scope) / workflow["stages"][0] / f"{task_id.lower()}-{slug}.md"
        content = template.replace('id: "CARD-NNNNNNNN"\n', f'id: "{task_id}"\n', 1)
        content = re.sub(r'^module: [^\n]*$', lambda _: f"module: {json.dumps(scope)}",
                         content, count=1, flags=re.MULTILINE)
        content = re.sub(r"^# CARD-NNNNNNNN[^\n]*$", lambda _: f"# {task_id} — {title}",
                         content, count=1, flags=re.MULTILINE)
        content = re.sub(r"^- Owner:[^\n]*$", lambda _: f"- Owner: {owner}",
                         content, count=1, flags=re.MULTILINE)
        if f'id: "{task_id}"' not in content or f"module: {json.dumps(scope)}" not in content:
            raise ValueError("The Card template needs id and module header fields.")
        return target, content

    if not apply:
        target, content = prepare()
        print(f"Preview {target.relative_to(project.root)}:\n\n{content}")
        print("Run again with --apply once the project intake rules permit recording the backlog Card.")
        return 0

    with write_lock:
        target, content = prepare()
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as stream:
            stream.write(content)
    print(f"Created {target.relative_to(project.root)}.")
    return 0
