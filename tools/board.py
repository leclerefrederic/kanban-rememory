"""Initialize, validate, display, create, or move cards on a Markdown Kanban board."""

import argparse
from collections import defaultdict
from contextlib import contextmanager
from datetime import date, datetime
from hashlib import sha256
import json
import os
from zoneinfo import ZoneInfo
from pathlib import Path
import re
import subprocess
from unicodedata import normalize
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
CARD_ID = re.compile(r"^([A-Z][A-Z0-9]*-[0-9]{8})(?:-|$)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
LINK = re.compile(r"(?<!\\)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")


def card_order(path):
    prefix, _, number = CARD_ID.match(path.stem)[1].rpartition("-")
    return prefix, int(number), path.name


def cards(stage):
    paths = (ROOT / "kanban" / stage).glob("*.md")
    return sorted((path for path in paths if CARD_ID.match(path.stem)), key=card_order)


def prose_lines(lines):
    fence = ""
    for index, line in enumerate(lines):
        marker = FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and set(line.strip()) == {fence[0]}:
                fence = ""
        elif marker:
            fence = marker[1]
        else:
            yield index, line


def markdown_lines(source):
    for _, line in prose_lines(source.splitlines()):
        yield line


def anchors(source):
    result = set()
    for line in markdown_lines(source):
        heading = HEADING.match(line)
        if heading:
            slug = re.sub(r"[^\w -]", "", heading[2].lower()).replace(" ", "-")
            unique = slug
            suffix = 1
            while unique in result:
                unique = f"{slug}-{suffix}"
                suffix += 1
            result.add(unique)
    return result


def acceptance_checks(source):
    section_level = None
    for line in markdown_lines(source):
        heading = HEADING.match(line)
        if heading and (section_level is None or len(heading[1]) <= section_level):
            section_level = len(heading[1]) if heading[2].casefold() == "acceptance criteria" else None
        if section_level and re.match(r"\s*[-*+]\s+\[[ xX]\]", line):
            yield line.strip()


def markdown_files():
    listed = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=ROOT,
    )
    for name in sorted(set(os.fsdecode(listed).split("\0")) - {""}):
        path = ROOT / name
        if path.is_file() and not path.is_symlink():
            yield path


def header_value(source, key, default=None):
    lines = source.splitlines()
    if not lines or lines[0] != "---":
        return default
    if "---" not in lines[1:]:
        raise ValueError("Unclosed YAML front matter.")
    for line in lines[1:lines.index("---", 1)]:
        name, separator, value = line.partition(":")
        if separator and name == key:
            raw = value.strip()
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                if raw.startswith(("[", "{", '"')):
                    raise ValueError(f"Invalid front matter value for {key}. Use JSON flow syntax.")
                return raw
    return default


def relationship(source, key):
    missing = object()
    value = header_value(source, key, missing)
    if value is not missing:
        return value
    legacy = "fiche_ids" if key == "fiches" else f"{key}_id"
    return header_value(source, legacy)


def fiche_entries(source):
    if header_value(source, "type") == "lot":
        entries = header_value(source, "fiches")
        if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
            raise ValueError("Lot front matter requires a fiches list of mappings.")
        for entry in entries:
            yield [entry.get(key) for key in ("id", "revision", "path", "sha256")]
        return
    for line in markdown_lines(source):
        if line.startswith("- Fiche:"):
            yield [part.strip() for part in line.partition(":")[2].split("|")]


def validate_lot_mapping(card_paths):
    findings = []

    def report(path, message):
        findings.append(f"{path.relative_to(ROOT)}: {message}")

    fiches = set()
    frozen = {}
    for state in ("ready", "frozen"):
        for path in (ROOT / "specs" / state).glob("*.md"):
            content = path.read_bytes()
            source = content.decode("utf-8")
            fiche_id = header_value(source, "id") or field(source, "Fiche ID")
            revision = str(header_value(source, "revision") or field(source, "Revision"))
            if not fiche_id:
                continue
            fiches.add(fiche_id)
            if state == "frozen":
                frozen[path.relative_to(ROOT).as_posix()] = (fiche_id, revision, sha256(content).hexdigest())

    lots = {}
    for path in (ROOT / "Lots").glob("*/Description.md"):
        lot_id = path.parent.name
        selected = set()
        lots[lot_id] = selected
        source = path.read_text(encoding="utf-8")
        if header_value(source, "type") == "lot":
            if header_value(source, "id") != lot_id:
                report(path, "Lot ID must match the directory name.")
            companion_ids = []
            for name, kind, other in (("Tests.md", "tests", "report"), ("Report.md", "report", "tests")):
                record = path.with_name(name)
                record_source = record.read_text(encoding="utf-8") if record.is_file() else ""
                record_id = header_value(record_source, "id")
                expected_id = relationship(source, kind)
                sibling_id = relationship(record_source, other)
                if (not isinstance(record_id, str) or not record_id
                        or header_value(record_source, "type") != kind
                        or relationship(record_source, "lot") != lot_id
                        or (expected_id is not None and record_id != expected_id)
                        or (sibling_id is not None and sibling_id != relationship(source, other))):
                    report(path, f"Inconsistent YAML references for {name}.")
                companion_ids.append(record_id)
            if companion_ids[0] and companion_ids[0] == companion_ids[1]:
                report(path, "Tests and Report must have distinct IDs.")
        for parts in fiche_entries(source):
            if len(parts) == 3:
                parts = [*parts, None]
            if (len(parts) != 4 or any(not isinstance(part, str) or not part for part in parts[:3])
                    or (parts[3] is not None and
                        (not isinstance(parts[3], str) or not re.fullmatch(r"[0-9a-f]{64}", parts[3])))):
                report(path, "Fiche entry requires an ID, revision, and path. Legacy digests must be valid.")
                continue
            pinned = frozen.get(parts[2])
            if not pinned or pinned[:2] != tuple(parts[:2]):
                report(path, "Fiche entry must pin a matching frozen ID, revision, and path.")
                continue
            if parts[3] is not None and pinned[2] != parts[3]:
                report(path, f"Frozen Fiche content changed: {parts[2]}")
            if parts[0] in selected:
                report(path, f"duplicate Fiche in Lot: {parts[0]}")
            selected.add(parts[0])
        if not selected:
            report(path, "Lot requires at least one frozen Fiche.")

    for path in card_paths:
        source = path.read_text(encoding="utf-8")
        if header_value(source, "type") == "card":
            if header_value(source, "id") != CARD_ID.match(path.stem)[1]:
                report(path, "Card ID must match the filename.")
            lot_id = relationship(source, "lot")
            fiche_ids = relationship(source, "fiches")
            if ((lot_id is not None and not isinstance(lot_id, str))
                    or not isinstance(fiche_ids, list)
                    or any(not isinstance(item, str) or not item for item in fiche_ids)):
                report(path, "Card references require a Lot ID or null and a list of Fiche IDs.")
                continue
        else:
            lot_id = field(source, "Lot ID")
            fiche_ids = [item.strip() for item in field(source, "Fiche IDs").split(",")]
        if lot_id and lot_id not in lots:
            report(path, f"unknown Lot: {lot_id}")
        for fiche_id in fiche_ids:
            if not fiche_id:
                continue
            if fiche_id not in fiches:
                report(path, f"Fiche is not ready or frozen: {fiche_id}")
            elif lot_id in lots and fiche_id not in lots[lot_id]:
                report(path, f"Fiche {fiche_id} is outside Lot {lot_id}")
    return findings


def validate(workflow):
    findings = []
    by_id = defaultdict(list)
    for stage in workflow["stages"]:
        for path in sorted((ROOT / "kanban" / stage).glob("*.md")):
            match = CARD_ID.match(path.stem)
            if not match or match[1].endswith("-00000000"):
                findings.append(f"{path.relative_to(ROOT)}: expected a task ID with eight digits from 00000001 to 99999999")
                continue
            by_id[CARD_ID.match(path.stem)[1]].append(path.relative_to(ROOT))
            if stage == workflow["completed"]:
                for check in acceptance_checks(path.read_text(encoding="utf-8")):
                    if re.match(r"[-*+]\s+\[ \]", check):
                        findings.append(f"{path.relative_to(ROOT)}: unchecked acceptance criterion: {check}")
    for task_id, paths in by_id.items():
        if len(paths) > 1:
            findings.append(f"duplicate {task_id}: {', '.join(map(str, paths))}")

    findings.extend(validate_lot_mapping(ROOT / path for paths in by_id.values() for path in paths))

    for path in markdown_files():
        name = path.relative_to(ROOT)
        for line in markdown_lines(path.read_text(encoding="utf-8")):
            prose = re.sub(r"`+[^\x60]*`+", "", line)
            for match in LINK.finditer(prose):
                href = match[1] or match[2]
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    continue
                target = path.parent / unquote(url.path) if url.path else path
                if not target.exists():
                    findings.append(f"{name}: missing link target {href}")
                elif url.fragment and target.suffix.lower() == ".md" and target.is_file():
                    if unquote(url.fragment) not in anchors(target.read_text(encoding="utf-8")):
                        findings.append(f"{name}: missing heading anchor {href}")

    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Kanban validation passed.")
    return 0


def field(source, label):
    match = re.search(rf"^[-*] {re.escape(label)}:[ \t]*(.*)$", source, re.MULTILINE)
    return match[1].strip() if match else ""


def show_board(workflow, limit, today):
    wip = 0
    for stage in workflow["stages"]:
        print(stage)
        for path in cards(stage):
            source = path.read_text(encoding="utf-8")
            heading = next((line[2:] for line in markdown_lines(source)
                            if line.startswith("# ")), path.stem)
            task_id = CARD_ID.match(path.stem)[1]
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


def check_workflow(workflow):
    if not isinstance(workflow, dict):
        raise ValueError("workflow.json must contain an object.")
    stages = workflow.get("stages")
    if (not isinstance(stages, list) or not stages
            or any(not isinstance(stage, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", stage)
                   for stage in stages)
            or len(stages) != len(set(stages))):
        raise ValueError("stages must contain unique folder names.")
    active = workflow.get("active")
    completed = workflow.get("completed")
    if (not isinstance(active, list) or not active or any(stage not in stages for stage in active)
            or completed not in stages or completed in active):
        raise ValueError("Define active stages and a distinct completed stage.")
    transitions = workflow.get("transitions", {})
    if not isinstance(transitions, dict) or any(
        source not in stages or not isinstance(destinations, list)
        or any(destination not in stages or destination == source for destination in destinations)
        for source, destinations in transitions.items()
    ):
        raise ValueError("Transitions must map stage names to lists of distinct destination stages.")
    limit = workflow.get("wip_limit")
    if type(limit) is not int or limit < 1:
        raise ValueError("wip_limit must be a positive integer.")
    timezone = workflow.get("timezone")
    if not isinstance(timezone, str) or not timezone:
        raise ValueError("timezone must be an IANA time zone.")
    try:
        ZoneInfo(timezone)
    except (KeyError, ValueError):
        raise ValueError(f"Unknown time zone: {timezone}") from None
    return workflow


def load_workflow():
    path = ROOT / "kanban/workflow.json"
    if not path.is_file():
        raise ValueError("No workflow configured. Follow agents/adoption.md before using the board.")
    workflow = check_workflow(json.loads(path.read_text(encoding="utf-8")))
    missing = [stage for stage in workflow["stages"] if not (ROOT / "kanban" / stage).is_dir()]
    if missing:
        raise ValueError(f"Missing stage folders: {', '.join(missing)}")
    return workflow


TEMPLATES = {
    "short": ([], ["development"]),
    "standard": ([], ["development", "code-review"]),
    "long": (["refinement"], ["development", "code-review", "testing", "deployment"]),
}


def starter_transitions(delivery, active):
    transitions = {
        stage: [following, "archive"] for stage, following in zip(delivery, delivery[1:])
    }
    for stage in active[1:]:
        transitions[stage].append(active[0])
    return transitions


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


def is_closed_lot_report(document):
    relative = document.relative_to(ROOT)
    if len(relative.parts) != 3 or relative.parts[0] != "Lots" or document.name != "Report.md":
        return False
    description = document.with_name("Description.md")
    if not description.is_file():
        return False
    lines = description.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return False
    front_matter = lines[1:lines.index("---", 1)]
    return any(re.fullmatch(r"""status:[ 	]*(?:closed|'closed'|"closed")[ 	]*""", line)
               for line in front_matter)


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
               if CARD_ID.match(card.stem)[1] == task_id]
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
    target = ROOT / "kanban" / destination / card.name
    if target.exists() or target.is_symlink():
        raise ValueError(f"Destination already exists: {target.relative_to(ROOT)}")
    timestamp = datetime.now(ZoneInfo(workflow["timezone"])).isoformat(timespec="seconds")
    transition = f"{timestamp} — Stage moved from `{stage}` to `{destination}`."
    relocate_card(card, target, ROOT / "kanban" / workflow["completed"], transition)
    print(f"Moved {task_id} from {stage} to {destination}.")
    return 0


def initialize(args):
    if args.config:
        workflow = json.loads(args.config.read_text(encoding="utf-8"))
    else:
        preparation, active = TEMPLATES[args.template]
        delivery = ["backlog", *preparation, *active, "completion"]
        workflow = {
            "stages": [*delivery, "archive"],
            "transitions": starter_transitions(delivery, active),
            "active": active,
            "completed": "completion",
            "wip_limit": args.wip_limit if args.wip_limit is not None else 1,
            "timezone": args.timezone or "UTC",
        }
    check_workflow(workflow)

    board = ROOT / "kanban"
    config = board / "workflow.json"
    if board.is_symlink() or config.is_symlink():
        raise ValueError("The board and workflow configuration must be local paths.")
    if config.exists() and json.loads(config.read_text(encoding="utf-8")) != workflow:
        raise ValueError("A different workflow already exists. Use an explicit migration.")
    stages = [board / stage for stage in workflow["stages"]]
    for stage in stages:
        if stage.is_symlink() or (stage.exists() and not stage.is_dir()):
            raise ValueError(f"Stage path is not a local directory: {stage.relative_to(ROOT)}")
    if board.exists():
        outside = [entry.name for entry in board.iterdir()
                   if entry.is_dir() and entry not in stages and any(entry.glob("*.md"))]
        if outside:
            raise ValueError(f"Existing cards outside the proposed stages: {', '.join(sorted(outside))}")

    print(json.dumps(workflow, indent=2))
    for stage in stages:
        if not stage.exists():
            print(f"Create {stage.relative_to(ROOT)}/")
    if not args.apply:
        print("Preview only. Run again with --apply after approval.")
        return 0

    for stage in stages:
        stage.mkdir(parents=True, exist_ok=True)
        if not any(stage.iterdir()):
            (stage / ".gitkeep").touch(exist_ok=True)
    try:
        with config.open("x", encoding="utf-8") as file:
            json.dump(workflow, file, indent=2)
            file.write("\n")
    except FileExistsError:
        if load_workflow() != workflow:
            raise ValueError("A different workflow already exists. Use an explicit migration.") from None
    print("Workflow ready.")
    return 0


@contextmanager
def board_write_lock():
    lock = ROOT / "kanban/.write-lock"
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
                task_id = CARD_ID.match(card.stem)[1]
                if task_id in seen:
                    raise ValueError(f"Duplicate {task_id}. Resolve the collision before creating a card.")
                seen.add(task_id)
                if task_id.startswith("TASK-"):
                    highest = max(highest, int(task_id.split("-")[1]))
        if highest >= 99999999:
            raise ValueError("The eight-digit TASK range is exhausted.")
        task_id = f"TASK-{highest + 1:08d}"
        target = ROOT / "kanban" / entry / f"{task_id}-{slug}.md"
        content = template.replace('id: "TASK-NNNNNNNN"', f'id: "{task_id}"', 1)
        content = content.replace("# TASK-NNNNNNNN — Short title", f"# {task_id} — {title}", 1)
        content = content.replace("- Owner: application, team, or domain", f"- Owner: {owner}", 1)
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


def verify_approval(lot_id, revision):
    if not re.fullmatch(r"Lot-[0-9]+", lot_id):
        raise ValueError("Expected a Lot ID such as Lot-001.")
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision):
        raise ValueError("Supply the full trusted approval commit ID.")
    kind = subprocess.run(["git", "cat-file", "-t", revision], cwd=ROOT, capture_output=True)
    if kind.returncode or kind.stdout.strip() != b"commit":
        raise ValueError("The trusted approval commit is unavailable.")

    description = ROOT / "Lots" / lot_id / "Description.md"

    def approved_bytes(path):
        relative = path.relative_to(ROOT).as_posix()
        recorded = subprocess.run(
            ["git", "show", f"{revision}:{relative}"], cwd=ROOT, capture_output=True,
        )
        if recorded.returncode:
            raise ValueError(f"Approval mismatch: {relative}")
        return recorded.stdout

    approved = approved_bytes(description).decode("utf-8")
    current = description.read_bytes().decode("utf-8")
    status = header_value(current, "status")
    if header_value(approved, "status") != "ready" or status not in ("ready", "validated", "rejected"):
        raise ValueError("Approval verification requires a ready approval and a ready or decided Lot.")
    if status != "ready":
        header, end, body = current[4:].partition("\n---\n") if current.startswith("---\n") else ("", "", "")
        if end:
            header = re.sub(r"(?m)^status:[^\n]*$", "status: ready", header, count=1)
            current = "---\n" + header + end + body
    if current != approved:
        raise ValueError(f"Approval mismatch: {description.relative_to(ROOT)}")
    findings = validate_lot_mapping(())
    if findings:
        raise ValueError("\n".join(findings))
    for entry in fiche_entries(approved):
        fiche = ROOT / entry[2]
        if fiche.read_bytes() != approved_bytes(fiche):
            raise ValueError(f"Approval mismatch: {fiche.relative_to(ROOT)}")
    print(f"Approval verified for {lot_id}.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    approval = commands.add_parser("verify-approval")
    approval.add_argument("lot_id")
    approval.add_argument("revision", help="Full commit ID from the trusted approval record")
    new = commands.add_parser("new")
    new.add_argument("title")
    new.add_argument("--owner", required=True)
    new.add_argument("--apply", action="store_true", help="Create the approved card")
    move = commands.add_parser("move")
    move.add_argument("task_id")
    move.add_argument("destination")
    init = commands.add_parser("init")
    source = init.add_mutually_exclusive_group(required=True)
    source.add_argument("--template", choices=TEMPLATES)
    source.add_argument("--config", type=Path, help="Approved custom workflow JSON")
    init.add_argument("--wip-limit", type=int, help="Template WIP limit (default: 1)")
    init.add_argument("--timezone", help="Template IANA time zone (default: UTC)")
    init.add_argument("--apply", action="store_true", help="Apply the approved preview")
    board = commands.add_parser("show")
    board.add_argument("--wip-limit", type=int, help="Overall WIP limit for this board")
    board.add_argument("--timezone", help="IANA time zone for age")
    args = parser.parse_args()
    if args.command == "init" and args.config and (args.wip_limit is not None or args.timezone):
        init.error("Set wip_limit and timezone in the custom configuration.")
    try:
        if args.command == "init":
            return initialize(args)
        workflow = load_workflow()
        if args.command == "verify-approval":
            return verify_approval(args.lot_id, args.revision)
        if args.command == "new":
            return create_card(workflow, args)
        if args.command == "move":
            with board_write_lock():
                return move_card(workflow, args.task_id, args.destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    if args.command == "validate":
        return validate(workflow)
    if args.wip_limit is not None and args.wip_limit < 1:
        board.error("--wip-limit must be positive")
    try:
        today = datetime.now(ZoneInfo(args.timezone or workflow["timezone"])).date()
    except (KeyError, ValueError):
        board.error(f"unknown time zone: {args.timezone}")
    return show_board(workflow, args.wip_limit or workflow["wip_limit"], today)


if __name__ == "__main__":
    raise SystemExit(main())
