"""Markdown readers for Cards, the journal and documents."""

from datetime import datetime
import json
import os
import re
import subprocess

CARD_FILE = re.compile(r"card-([0-9]{8})(?=-|$)", re.IGNORECASE)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*#*\s*$")
LINK = re.compile(r"(?<!\\)\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\s*\)")
MOVE = re.compile(r"^(?:- )?(\S+) — Stage moved from `[^`]+` to `([^`]+)`", re.MULTILINE)
UNCHECKED = re.compile(r"[-*+]\s+\[ \]")


def card_id(path):
    match = CARD_FILE.match(path.stem)
    return f"CARD-{match[1]}" if match else None


def prose_lines(lines):
    """Yield (index, line) outside fenced code blocks."""
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


def anchors(source):
    result = set()
    for _, line in prose_lines(source.splitlines()):
        heading = HEADING.match(line)
        if heading:
            slug = re.sub(r"[^\w -]", "", heading[2].lower()).replace(" ", "-")
            unique, suffix = slug, 1
            while unique in result:
                unique, suffix = f"{slug}-{suffix}", suffix + 1
            result.add(unique)
    return result


def acceptance_checks(source):
    """Checklist items of the Acceptance criteria section."""
    level = None
    for _, line in prose_lines(source.splitlines()):
        heading = HEADING.match(line)
        if heading and (level is None or len(heading[1]) <= level):
            level = len(heading[1]) if heading[2].casefold() == "acceptance criteria" else None
        if level and re.match(r"\s*[-*+]\s+\[[ xX]\]", line):
            yield line.strip()


def unchecked(source):
    """True when the acceptance checklist is empty or has an open item."""
    checks = list(acceptance_checks(source))
    return not checks or any(UNCHECKED.match(check) for check in checks)


def resource_links(source):
    section = re.search(r"(?ms)^## Resources[ \t]*$(.*?)(?=^## |\Z)", source)
    if section:
        for _, line in prose_lines(section.group(1).splitlines()):
            for match in LINK.finditer(line):
                yield match[1] or match[2]


def front_matter(source):
    """(key, value) pairs of the front matter; values use JSON flow syntax when quoted or bracketed."""
    lines = source.splitlines()
    if lines[:1] != ["---"]:
        return []
    if "---" not in lines[1:]:
        raise ValueError("Unclosed front matter.")
    pairs = []
    for line in lines[1:lines.index("---", 1)]:
        key, separator, raw = line.partition(":")
        if separator:
            raw = raw.strip()
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                if raw.startswith(("[", "{", '"')):
                    raise ValueError(f"Invalid front matter value for {key}. Use JSON flow syntax.") from None
                value = raw
            pairs.append((key, value))
    return pairs


def header_value(source, key, default=None):
    return next((value for name, value in front_matter(source) if name == key), default)


def field(source, label):
    match = re.search(rf"^[-*] {re.escape(label)}:[ \t]*(.*)$", source, re.MULTILINE)
    return match[1].strip() if match else ""


def moves(source):
    """(time, destination) of each stage move recorded in a Card's History."""
    return [(datetime.fromisoformat(at), stage) for at, stage in MOVE.findall(source)]


def markdown_files(root):
    """Tracked and untracked, not ignored, Markdown files of a checkout."""
    listed = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard", "--", "*.md"], cwd=root)
    for name in sorted(set(os.fsdecode(listed).split("\0")) - {""}):
        path = root / name
        if path.suffix.lower() == ".md" and path.is_file() and not path.is_symlink():
            yield path
