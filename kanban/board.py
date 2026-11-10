"""Read the Markdown Kanban repository without writing to it."""

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
CARD_ID = re.compile(r"^([A-Z][A-Z0-9]*-\d+)(?:-|$)")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
LINK = re.compile(r"(?<!\\)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")


def cards(stage):
    return sorted(path for path in (ROOT / "kanban" / stage).glob("*.md")
                  if CARD_ID.match(path.stem))


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


def validate(workflow):
    findings = []
    by_id = defaultdict(list)
    for stage in workflow["stages"]:
        for path in cards(stage):
            by_id[CARD_ID.match(path.stem)[1]].append(path.relative_to(ROOT))
            if stage == workflow["completed"]:
                section_level = None
                for line in markdown_lines(path.read_text(encoding="utf-8")):
                    heading = HEADING.match(line)
                    if heading and (section_level is None or len(heading[1]) <= section_level):
                        section_level = (len(heading[1])
                                         if heading[2].casefold() == "acceptance criteria" else None)
                    if section_level and re.match(r"\s*[-*+]\s+\[ \]", line):
                        findings.append(f"{path.relative_to(ROOT)}: unchecked acceptance criterion: {line.strip()}")
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


def load_workflow():
    path = ROOT / "kanban/workflow.json"
    if not path.is_file():
        raise ValueError("No workflow configured. Follow kanban/adoption.md before using the board.")
    workflow = json.loads(path.read_text(encoding="utf-8"))
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
    missing = [stage for stage in stages if not (ROOT / "kanban" / stage).is_dir()]
    if missing:
        raise ValueError(f"Missing stage folders: {', '.join(missing)}")
    return workflow


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    board = commands.add_parser("show")
    board.add_argument("--wip-limit", type=int, help="Overall WIP limit for this board")
    board.add_argument("--timezone", help="IANA time zone for age")
    args = parser.parse_args()
    try:
        workflow = load_workflow()
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
