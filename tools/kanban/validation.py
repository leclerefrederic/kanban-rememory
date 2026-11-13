"""Board and document validation."""

from collections import defaultdict
import re
import subprocess
from urllib.parse import unquote, urlsplit

from .batches import validate_lot_mapping
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, anchors,
                    markdown_files, markdown_lines)


# Preserve the exact historical references recorded before this policy.
HISTORICAL_CARD_REFERENCES = {
    ("project/batches/batch-001/report.md", "TASK-00000029"): 1,
    ("project/batches/batch-002/report.md", "TASK-00000058"): 1,
}
BATCH_CARD_ID = re.compile(r"\bTASK-[0-9]{8}\b", re.IGNORECASE)


def archived_specification_resource(source, target):
    active = PROJECT / "specs/resources/active"
    if source.parent != PROJECT / "specs/approved" or not target.is_relative_to(active):
        return False
    archived = PROJECT / "specs/resources/archived" / target.relative_to(active)
    if not archived.is_file():
        return False
    spec_path = source.relative_to(ROOT).as_posix()
    resource_path = target.relative_to(ROOT).as_posix()
    history = subprocess.check_output(
        ["git", "log", "--all", "--format=%H", "--", spec_path, resource_path], cwd=ROOT, text=True
    )
    for commit in history.splitlines():
        original = subprocess.run(["git", "show", f"{commit}:{spec_path}"], cwd=ROOT, capture_output=True)
        if original.returncode or original.stdout != source.read_bytes():
            continue
        resource = subprocess.run(["git", "show", f"{commit}:{resource_path}"], cwd=ROOT, capture_output=True)
        if resource.returncode == 0 and resource.stdout == archived.read_bytes():
            return True
    return False


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
        batch_record = len(name.parts) >= 4 and name.parts[:2] in {
            ("project", "batches"), ("project", "lots"), ("project", "Lots"),
        }
        if batch_record:
            references = defaultdict(int)
            for match in BATCH_CARD_ID.finditer(path.read_text(encoding="utf-8")):
                references[match[0].upper()] += 1
            for task_id, count in references.items():
                if count > HISTORICAL_CARD_REFERENCES.get((name.as_posix(), task_id), 0):
                    findings.append(f"{name}: Batch records cannot reference Card {task_id}")
        for line in markdown_lines(path.read_text(encoding="utf-8")):
            prose = re.sub(r"`+[^\x60]*`+", "", line)
            for match in LINK.finditer(prose):
                href = match[1] or match[2]
                url = urlsplit(href)
                if batch_record and url.path:
                    link_path = unquote(url.path)
                    board = ROOT / "project" / "kanban"
                    resolved = (path.parent / link_path).resolve()
                    if resolved.is_relative_to(board) or re.search(r"(?:^|/)project/kanban(?:/|$)", link_path):
                        findings.append(f"{name}: Batch records cannot link to Kanban paths: {href}")
                if url.scheme or url.netloc:
                    continue
                target = path.parent / unquote(url.path) if url.path else path
                if not target.exists() and path.is_relative_to(PROJECT / "batches"):
                    target = target.with_name(target.name.lower())
                if not target.exists() and archived_specification_resource(path, target.resolve()):
                    continue
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
