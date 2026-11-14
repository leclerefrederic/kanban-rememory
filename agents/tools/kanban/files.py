"""Repository paths and Markdown readers."""

import json
import os
from pathlib import Path
import re
import subprocess


ROOT = Path(os.environ["KRR_VALIDATION_ROOT"]).resolve() if "KRR_VALIDATION_ROOT" in os.environ else Path(__file__).resolve().parents[3]


PROJECT = ROOT / "project"


CARD_ID = re.compile(r"^([A-Z][A-Z0-9]*-[0-9]{8})(?:-|$)", re.ASCII | re.IGNORECASE)


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*$")


HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")


LINK = re.compile(r"(?<!\\)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")


def card_order(path):
    prefix, _, number = CARD_ID.match(path.stem)[1].upper().rpartition("-")
    return prefix, int(number), path.name


def cards(stage):
    paths = (PROJECT / "kanban" / stage).glob("*.md")
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


def field(source, label):
    match = re.search(rf"^[-*] {re.escape(label)}:[ \t]*(.*)$", source, re.MULTILINE)
    return match[1].strip() if match else ""
