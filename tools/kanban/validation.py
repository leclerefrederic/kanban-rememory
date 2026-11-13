"""Board and document validation."""

from collections import defaultdict
import re
from urllib.parse import unquote, urlsplit

from .batches import validate_lot_mapping
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, anchors,
                    markdown_files, markdown_lines)


def validate(workflow):
    findings = []
    by_id = defaultdict(list)
    for stage in workflow["stages"]:
        for path in sorted((PROJECT / "kanban" / stage).glob("*.md")):
            match = CARD_ID.match(path.stem)
            if not match or match[1].endswith("-00000000"):
                findings.append(f"{path.relative_to(ROOT)}: expected a task ID with eight digits from 00000001 to 99999999")
                continue
            by_id[CARD_ID.match(path.stem)[1].upper()].append(path.relative_to(ROOT))
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
                if not target.exists() and path.is_relative_to(PROJECT / "batches"):
                    target = target.with_name(target.name.lower())
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
