"""Board and document validation."""

from collections import defaultdict
import re
import subprocess
from urllib.parse import unquote, urlsplit

from .batches import relationship, validate_lot_mapping
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, anchors,
                    check_module_records, header_value, markdown_files, markdown_lines, resource_links)
from .project import PROJECT_SCOPE
from .specifications import SPECIFICATION_NAMES, specification_root


# Preserve the exact historical references recorded before this policy.
HISTORICAL_CARD_REFERENCES = {
    ("project/batches/batch-001/report.md", "CARD-00000029"): 1,
    ("project/batches/batch-002/report.md", "CARD-00000058"): 1,
}
# Exact links retained in frozen records after CARD-00000142 removed the redirects.
HISTORICAL_RETIRED_LINKS = {
    ('project/kanban/completion/card-00000078-align-the-documentation-and-tools-with-the-delivery-workflow.md',
     '../../../agents/runner/build-and-run.md'),
    ('project/kanban/completion/card-00000086-group-companion-app-sources-and-builds-under-apps.md',
     '../../../agents/runner/build-and-run.md'),
    ('project/batches/batch-001/tests.md',
     '../../../agents/batches/resume-a-batch.md'),
    ('project/kanban/completion/card-00000003-software-development.md',
     '../../../agents/kanban/software-development-workflow.md#example'),
    ('project/kanban/completion/card-00000078-align-the-documentation-and-tools-with-the-delivery-workflow.md',
     '../../../agents/work-in-a-project.md'),
    ('project/kanban/completion/card-00000078-align-the-documentation-and-tools-with-the-delivery-workflow.md',
     '../../../agents/batches/batch-workflow.md'),
    ('project/kanban/completion/card-00000078-align-the-documentation-and-tools-with-the-delivery-workflow.md',
     '../../../agents/batches/start-and-close-batches.md'),
    ('project/kanban/completion/card-00000078-align-the-documentation-and-tools-with-the-delivery-workflow.md',
     '../../../agents/batches/delivery-example.md'),
    ('project/kanban/completion/card-00000083-apply-the-shared-lean-manifesto-through-explicit-agent-rules.md',
     '../../../agents/lean-specifications.md'),
    ('project/kanban/completion/card-00000085-keep-one-readme-and-name-documentation-entry-points-explicitly.md',
     '../../../agents/maintain-rememory.md'),
    ('project/kanban/completion/card-00000140-parallelize-independent-work-within-an-approved-assignment.md',
     '../../../agents/orchestrate-work.md'),
    ('project/specs/approved/spec-012-r1.md',
     '../../../agents/roles/specification-agent.md'),
    ('project/specs/approved/spec-012-r1.md',
     '../../../agents/roles/development-agent.md'),
    ('project/specs/approved/spec-016-r1.md',
     '../../../agents/work-in-a-project.md'),
    ('project/specs/approved/spec-016-r1.md',
     '../../../agents/batches/batch-workflow.md'),
    ('project/specs/approved/spec-019-r1.md',
     '../../../agents/batches/batch-workflow.md'),
}

# These frozen links record CARD-128's original stage and must stay byte-identical.
CARD_128_BACKLOG_NAME = "card-00000128-protect-the-agent-settings-from-edits-and-cover-codex-with-role-limits.md"
FROZEN_CARD_MOVE_LINKS = {
    ("project/kanban/completion/card-00000095-design-how-role-limits-know-the-active-role.md",
     f"../backlog/{CARD_128_BACKLOG_NAME}"),
    ("project/kanban/completion/card-00000096-enforce-role-limits-with-hooks-for-each-llm.md",
     f"../backlog/{CARD_128_BACKLOG_NAME}"),
    ("project/specs/approved/spec-012-r2.md", f"../../kanban/backlog/{CARD_128_BACKLOG_NAME}"),
}

BATCH_CARD_ID = re.compile(r"\b(?:CARD|TASK)-([0-9]{8})\b", re.IGNORECASE)


def archived_specification_resource(source, target, project=PROJECT, root=ROOT):
    if source.parent not in {project / name / "approved" for name in SPECIFICATION_NAMES}:
        return False
    try:
        specifications = specification_root(project)
    except ValueError:
        return False
    active = specifications / "resources/active"
    if source.parent not in (specifications / "approved", specifications / "retired") or not target.is_relative_to(active):
        return False
    archived = specifications / "resources/archived" / target.relative_to(active)
    if not archived.is_file():
        return False
    spec_path = source.relative_to(root).as_posix()
    resource_path = target.relative_to(root).as_posix()
    history = subprocess.check_output(
        ["git", "log", "--all", "--format=%H", "--", spec_path, resource_path], cwd=root, text=True
    )
    for commit in history.splitlines():
        original = subprocess.run(["git", "show", f"{commit}:{spec_path}"], cwd=root, capture_output=True)
        if original.returncode or original.stdout != source.read_bytes():
            continue
        resource = subprocess.run(["git", "show", f"{commit}:{resource_path}"], cwd=root, capture_output=True)
        if resource.returncode == 0 and resource.stdout == archived.read_bytes():
            return True
    return False


def validate(workflow, project=PROJECT, workspaces=(), root=ROOT, *, context=None, selected_scope=None):
    findings = []
    by_id = defaultdict(list)
    scoped_paths = defaultdict(list)
    card_scopes = {}
    active_counts = defaultdict(int)
    if context:
        for workspace in workspaces:
            check_module_records(workspace)
    card_workspaces = context.card_workspaces() if context else (project,)
    historical = {workflow["completed"], "cancellation"}
    for stage in workflow["stages"]:
        paths = [(workspace, path) for workspace in card_workspaces
                 for path in sorted(((context.card_directory(workspace) if context else workspace / "kanban")
                                     / stage).glob("*.md"))]
        for workspace, path in paths:
            match = CARD_ID.match(path.stem)
            if not match or match[1].endswith("-00000000"):
                findings.append(f"{path.relative_to(root)}: expected a card ID with eight digits from 00000001 to 99999999")
                continue
            task_id = match[1].upper()
            if context:
                try:
                    scope = context.card_scope(path, allow_legacy=True)
                except ValueError as error:
                    findings.append(f"{path.relative_to(root)}: {error}")
                    continue
                if scope is None and (context.flat_board or stage not in historical):
                    findings.append(f"{path.relative_to(root)}: assign a scope to unfinished Cards before switching boards")
                    continue
                if context.module_boards and workspace != project and scope is None and stage in historical:
                    continue  # Older module archives retain their qualified IDs.
                if context.module_boards and stage not in historical and workspace == project:
                    findings.append(f"{path.relative_to(root)}: move unfinished Cards to their module board")
                if context.module_boards and workspace != project and scope is not None:
                    if workspace != context.card_workspace(scope):
                        findings.append(f"{path.relative_to(root)}: Card belongs on the {scope} board")
                    source = path.read_text(encoding="utf-8")
                    affected = header_value(source, "affected_modules", [])
                    if (not isinstance(affected, list) or any(
                        not isinstance(module, str) or module not in context.modules or module == context.misc_module
                        for module in affected
                    ) or (affected and scope != context.misc_module)):
                        findings.append(f"{path.relative_to(root)}: affected_modules must list real modules on a {context.misc_module} Card")
                    attachments = context.card_resources(workspace, task_id)
                    for href in resource_links(source):
                        url = urlsplit(href)
                        if url.scheme or url.netloc or not url.path:
                            continue
                        target = (path.parent / unquote(url.path)).resolve()
                        resources = attachments.parent
                        if target.is_relative_to(resources) and (not target.is_relative_to(attachments)
                                                                 or not target.is_file()):
                            findings.append(f"{path.relative_to(root)}: invalid Card attachment {href}")
                scoped_paths[scope or PROJECT_SCOPE].append(path)
                if scope is not None:
                    card_scopes[path] = scope
                    if (scope == PROJECT_SCOPE and selected_scope in {None, PROJECT_SCOPE}
                            and relationship(path.read_text(encoding="utf-8"), "batch")):
                        findings.append(f"{path.relative_to(root)}: Batch Cards require a module scope")
                    if stage in workflow["active"]:
                        active_counts[scope] += 1
            by_id[task_id].append(path.relative_to(root))
            if stage == workflow["completed"]:
                for check in acceptance_checks(path.read_text(encoding="utf-8")):
                    if re.match(r"[-*+]\s+\[ \]", check):
                        findings.append(f"{path.relative_to(root)}: unchecked acceptance criterion: {check}")
    for task_id, paths in by_id.items():
        if len(paths) > 1:
            findings.append(f"duplicate {task_id}: {', '.join(map(str, paths))}")

    if context:
        for scope in (PROJECT_SCOPE, *context.modules) if selected_scope is None else (selected_scope,):
            if active_counts[scope] > workflow["wip_limit"]:
                findings.append(f"{scope}: Card WIP exceeds the shared workflow limit")
            findings.extend(validate_lot_mapping(scoped_paths[scope], context.scope_workspace(scope), root,
                                                 standalone=context.flat_board))
    else:
        findings.extend(validate_lot_mapping(
            (root / path for paths in by_id.values() for path in paths), project, root,
        ))

    if context and context.flat_board:
        board_paths = tuple(space / stage for space in workspaces for stage in workflow["stages"])
    else:
        board_paths = (root / "project/kanban", *(space / "kanban" for space in workspaces))
    batch_folders = ("batches", "lots", "Lots")
    for path in markdown_files(None if project == root / "project" else project, root):
        name = path.relative_to(root)
        records = next((space for space in workspaces if path.is_relative_to(space)), project)
        if selected_scope is not None and (
            (records != project and records != context.scope_workspace(selected_scope))
            or (path in card_scopes and card_scopes[path] != selected_scope)
        ):
            continue
        batch_record = any(path.is_relative_to(records / folder) for folder in batch_folders)
        if batch_record:
            references = defaultdict(int)
            for match in BATCH_CARD_ID.finditer(path.read_text(encoding="utf-8")):
                references[f"CARD-{match[1]}"] += 1
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
                    resolved = (path.parent / link_path).resolve()
                    if any(resolved.is_relative_to(board) for board in board_paths) or re.search(r"(?:^|/)project/kanban(?:/|$)", link_path):
                        findings.append(f"{name}: Batch records cannot link to Kanban paths: {href}")
                if url.scheme or url.netloc:
                    continue
                target = path.parent / unquote(url.path) if url.path else path
                if path in card_scopes and url.path:
                    resolved = target.resolve()
                    expected = context.scope_workspace(card_scopes[path])
                    if any(resolved.is_relative_to(space / folder)
                           for space in (project, *workspaces) if space != expected for folder in batch_folders):
                        findings.append(f"{name}: Card cannot link to a Batch in a different scope: {href}")
                if not target.exists() and path.is_relative_to(records / "batches"):
                    target = target.with_name(target.name.lower())
                if not target.exists():
                    resolved = target.resolve()
                    for workspace in (project, *workspaces):
                        try:
                            approved = specification_root(workspace) / "approved"
                        except ValueError:
                            continue
                        if resolved.parent == approved and re.fullmatch(r"spec-[0-9]+\.md", target.name):
                            retired = approved.parent / "retired" / target.name
                            if retired.is_file():
                                target = retired
                            break
                if not target.exists() and archived_specification_resource(path, target.resolve(), records, root):
                    continue
                reference = (name.as_posix(), href)
                if not target.exists() and (reference in HISTORICAL_RETIRED_LINKS
                                            or reference in FROZEN_CARD_MOVE_LINKS):
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
