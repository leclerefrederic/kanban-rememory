"""Board and document validation."""

from collections import defaultdict
import re
import subprocess
from urllib.parse import unquote, urlsplit

from .batches import relationship, validate_lot_mapping
from .files import (CARD_ID, LINK, PROJECT, ROOT, acceptance_checks, anchors,
                    check_module_records, markdown_files, markdown_lines)
from .project import PROJECT_SCOPE


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
    active = project / "specs/resources/active"
    if source.parent != project / "specs/approved" or not target.is_relative_to(active):
        return False
    archived = project / "specs/resources/archived" / target.relative_to(active)
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
    for stage in workflow["stages"]:
        for path in sorted((project / "kanban" / stage).glob("*.md")):
            match = CARD_ID.match(path.stem)
            if not match or match[1].endswith("-00000000"):
                findings.append(f"{path.relative_to(root)}: expected a card ID with eight digits from 00000001 to 99999999")
                continue
            by_id[CARD_ID.match(path.stem)[1].upper()].append(path.relative_to(root))
            if context:
                try:
                    scope = context.card_scope(path, allow_legacy=True)
                except ValueError as error:
                    findings.append(f"{path.relative_to(root)}: {error}")
                    continue
                if scope is None and stage not in {workflow["completed"], "cancellation"}:
                    findings.append(f"{path.relative_to(root)}: assign a scope to unfinished Cards before switching boards")
                    continue
                scoped_paths[scope or PROJECT_SCOPE].append(path)
                if scope is not None:
                    card_scopes[path] = scope
                    if (scope == PROJECT_SCOPE and selected_scope in {None, PROJECT_SCOPE}
                            and relationship(path.read_text(encoding="utf-8"), "batch")):
                        findings.append(f"{path.relative_to(root)}: Batch Cards require a module scope")
                    if stage in workflow["active"]:
                        active_counts[scope] += 1
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
            findings.extend(validate_lot_mapping(scoped_paths[scope], context.scope_workspace(scope), root))
    else:
        findings.extend(validate_lot_mapping(
            (root / path for paths in by_id.values() for path in paths), project, root,
        ))

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
