"""Checks of the records and documents of one checkout."""

import re
from urllib.parse import unquote, urlsplit

from .markdown import (LINK, anchors, card_id, front_matter,
                       markdown_files, prose_lines, resource_links)
from .project import MISC, MODULES

TOOL = re.compile(r"orchestrator/tools/[\w./-]+\.py")


def validate(project):
    """Print every finding; return 1 when there is one."""
    root = project.root
    findings = [f"{path.relative_to(root)}: symbolic link in the records"
                for path in (root / "project").rglob("*") if path.is_symlink()]
    findings += board_findings(project)
    history = {project.board(module) / stage for module in project.modules for stage in project.frozen}
    for path in markdown_files(root):
        if path.parent not in history:  # completed and cancelled Cards keep the links of their time
            findings += document_findings(path, root)
    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Kanban validation passed.")
    return 0


def board_findings(project):
    root, workflow = project.root, project.workflow
    findings, seen = [], {}
    boards = root / MODULES
    for path in sorted(boards.iterdir()) if boards.is_dir() else ():
        if path.name not in project.modules and not path.name.startswith("."):
            findings.append(f"{path.relative_to(root)}: module missing from the settings")
    for module in project.modules:
        board = project.board(module)
        for path in sorted(board.iterdir()) if board.is_dir() else ():
            if path.name not in (*workflow["stages"], "resources") and not path.name.startswith("."):
                findings.append(f"{path.relative_to(root)}: stage missing from the workflow")
        active = 0
        for stage in workflow["stages"]:
            for path in sorted((board / stage).glob("*.md")):
                task_id = card_id(path)
                if not task_id or task_id.endswith("-00000000"):
                    findings.append(f"{path.relative_to(root)}: expected card-NNNNNNNN-title.md, "
                                    "eight digits from 00000001")
                    continue
                if task_id in seen:
                    findings.append(f"duplicate {task_id}: {seen[task_id]}, {path.relative_to(root)}")
                seen[task_id] = path.relative_to(root)
                active += stage in workflow["active"]
                findings += card_findings(project, module, stage, path, task_id)
        if active > workflow["wip_limit"]:
            findings.append(f"{module}: {active} active Cards exceed the WIP limit {workflow['wip_limit']}")
    return findings


def card_findings(project, module, stage, path, task_id):
    name = path.relative_to(project.root)
    source = path.read_text(encoding="utf-8")
    try:
        fields = front_matter(source)
    except ValueError as error:
        return [f"{name}: {error}"]
    findings = []
    if [value for key, value in fields if key == "id"] != [task_id]:
        findings.append(f"{name}: needs exactly one id field set to {task_id}")
    if [value for key, value in fields if key == "module"] != [module]:
        findings.append(f"{name}: needs exactly one module field set to {module}")
    affected = next((value for key, value in fields if key == "affected_modules"), [])
    if (not isinstance(affected, list) or (affected and module != MISC)
            or any(other not in project.modules or other == MISC for other in affected)):
        findings.append(f"{name}: affected_modules must list other real modules, on a {MISC} Card only")
    attachments = project.board(module) / "resources" / task_id.lower()
    for href in resource_links(source):
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (path.parent / unquote(url.path)).resolve()
        if target.is_relative_to(attachments.parent) and not (target.is_relative_to(attachments)
                                                               and target.is_file()):
            findings.append(f"{name}: attachment {href} must be a file in resources/{task_id.lower()}/")
    return findings


def document_findings(path, root):
    """Missing link targets, anchors and, outside the records, named tools."""
    findings = []
    name = path.relative_to(root)
    source = path.read_text(encoding="utf-8")
    if not path.is_relative_to(root / "project"):
        findings += [f"{name}: missing tool {tool}" for tool in sorted(set(TOOL.findall(source)))
                     if not (root / tool).is_file()]
    for _, line in prose_lines(source.splitlines()):
        for match in LINK.finditer(re.sub(r"`+[^`]*`+", "", line)):
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
    return findings
