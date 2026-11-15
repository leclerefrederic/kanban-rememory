"""Board and document validation."""

from collections import defaultdict
import re
from urllib.parse import unquote, urlsplit

from .files import (CARD_ID, LINK, acceptance_checks, anchors, check_local_records,
                    header_value, markdown_files, markdown_lines, resource_links)
from .project import MISC


# Exact links in completed Cards that predate the rename of agents/ to orchestrator/.
HISTORICAL_RETIRED_LINKS = {
    ('project/modules/notifications/completion/card-00000161-reconnecter-remy-au-workflow-de-livraison.md',
     '../../../../agents/actions/notify-user.md'),
    ('project/modules/notifications/completion/card-00000161-reconnecter-remy-au-workflow-de-livraison.md',
     '../../../../agents/actions/deliver-card.md'),
    ('project/modules/orchestrator/completion/card-00000160-automatiser-la-livraison-des-cards-avec-accord-avant-fusion.md',
     '../../../../agents/actions/deliver-card.md'),
}


def card_findings(project, workspace, stage, path, task_id):
    findings = []
    name = path.relative_to(project.root)
    try:
        scope = project.card_scope(path)
    except ValueError as error:
        return None, [f"{name}: {error}"]
    if workspace != project.workspace(scope):
        findings.append(f"{name}: Card belongs on the {scope} board")
    source = path.read_text(encoding="utf-8")
    affected = header_value(source, "affected_modules", [])
    if (not isinstance(affected, list)
            or any(not isinstance(module, str) or module not in project.modules or module == MISC
                   for module in affected)
            or (affected and scope != MISC)):
        findings.append(f"{name}: affected_modules must list real modules on a {MISC} Card")
    attachments = project.resources(scope, task_id)
    for href in resource_links(source):
        url = urlsplit(href)
        if url.scheme or url.netloc or not url.path:
            continue
        target = (path.parent / unquote(url.path)).resolve()
        if target.is_relative_to(attachments.parent) and (not target.is_relative_to(attachments)
                                                          or not target.is_file()):
            findings.append(f"{name}: invalid Card attachment {href}")
    if stage == project.workflow["completed"]:
        for check in acceptance_checks(source):
            if re.match(r"[-*+]\s+\[ \]", check):
                findings.append(f"{name}: unchecked acceptance criterion: {check}")
    return scope, findings


def link_findings(path, root):
    findings = []
    name = path.relative_to(root)
    for line in markdown_lines(path.read_text(encoding="utf-8")):
        prose = re.sub(r"`+[^\x60]*`+", "", line)
        for match in LINK.finditer(prose):
            href = match[1] or match[2]
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            target = path.parent / unquote(url.path) if url.path else path
            if not target.exists():
                if (name.as_posix(), href) not in HISTORICAL_RETIRED_LINKS:
                    findings.append(f"{name}: missing link target {href}")
            elif url.fragment and target.suffix.lower() == ".md" and target.is_file():
                if unquote(url.fragment) not in anchors(target.read_text(encoding="utf-8")):
                    findings.append(f"{name}: missing heading anchor {href}")
    return findings


def validate(project, selected_scope=None, checkout=None):
    """Check the primary board and journal, and the documents of the invoking checkout."""
    workflow = project.workflow
    findings = []
    by_id = defaultdict(list)
    card_scopes = {}
    active_counts = defaultdict(int)
    for workspace in project.modules.values():
        check_local_records(workspace)
    for stage in workflow["stages"]:
        for workspace in project.modules.values():
            for path in sorted((workspace / stage).glob("*.md")):
                match = CARD_ID.match(path.stem)
                if not match or match[1].endswith("-00000000"):
                    findings.append(f"{path.relative_to(project.root)}: expected a card ID with eight "
                                    "digits from 00000001 to 99999999")
                    continue
                task_id = match[1].upper()
                by_id[task_id].append(path.relative_to(project.root))
                scope, found = card_findings(project, workspace, stage, path, task_id)
                if scope is None or selected_scope in (None, scope):
                    findings.extend(found)
                if scope is not None:
                    card_scopes[path] = scope
                    if stage in workflow["active"]:
                        active_counts[scope] += 1
    for task_id, paths in by_id.items():
        if len(paths) > 1:
            findings.append(f"duplicate {task_id}: {', '.join(map(str, paths))}")
    for scope in project.modules if selected_scope is None else (selected_scope,):
        if active_counts[scope] > workflow["wip_limit"]:
            findings.append(f"{scope}: Card WIP exceeds the shared workflow limit")

    for path in markdown_files(None, project.root):
        records = next((space for space in project.modules.values() if path.is_relative_to(space)), None)
        if selected_scope is not None and (
            (records is not None and records != project.workspace(selected_scope))
            or card_scopes.get(path, selected_scope) != selected_scope
        ):
            continue
        findings.extend(link_findings(path, project.root))
    if checkout is not None and checkout != project.root:
        for path in markdown_files(None, checkout):
            if not path.is_relative_to(checkout / "project"):
                findings.extend(link_findings(path, checkout))

    for finding in findings:
        print(finding)
    if findings:
        return 1
    print("Kanban validation passed.")
    return 0
