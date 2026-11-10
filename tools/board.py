"""Initialize, validate, display, or move cards on a Markdown Kanban board."""

import argparse
from collections import defaultdict
from datetime import date, datetime
import json
from zoneinfo import ZoneInfo
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

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


def markdown_lines(source):
    fence = ""
    for line in source.splitlines():
        marker = FENCE.match(line)
        if fence:
            if line.strip().startswith(fence) and set(line.strip()) == {fence[0]}:
                fence = ""
        elif marker:
            fence = marker[1]
        else:
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

    listed = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"],
        cwd=ROOT,
    )
    for name in sorted(set(listed.decode().split("\0")) - {""}):
        path = ROOT / name
        if not path.is_file():
            continue
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


def move_card(workflow, task_id, destination):
    matches = [(stage, card) for stage in workflow["stages"] for card in cards(stage)
               if CARD_ID.match(card.stem)[1] == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one card for {task_id}, found {len(matches)}.")
    stage, card = matches[0]
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
    card.rename(target)
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
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
        if args.command == "move":
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
