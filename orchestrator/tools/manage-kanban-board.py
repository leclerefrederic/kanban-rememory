"""Initialize, validate, display, create, or move cards on a Markdown Kanban board."""

import argparse
import re
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError
from zoneinfo import ZoneInfo

from kanban.batches import verify_approval
from kanban.cards import board_write_lock, create_card, find_card, move_card, reassign_card, show_board
from kanban.coordination import Coordination, exclusive
from kanban.files import CARD_ID, ROOT, check_module_records
from kanban.project import PROJECT_SCOPE, coordination_root, invocation_module, load_project, primary_worktree
from kanban.specifications import specification_root
from kanban.specification_retirement import retire_batch_specifications
from kanban.validation import validate
from kanban.workflow import TEMPLATES, initialize, load_workflow


def board_context():
    local = load_project(ROOT)
    if (ROOT / ".git").exists() or local.modules:
        primary = primary_worktree(ROOT)
        canonical = local if primary == ROOT else load_project(primary)
        if canonical.modules:
            return canonical
        if local.modules:
            raise ValueError("Activate modules from the primary worktree before using tracking tools.")
    return local


def historical_path(project, reference, requested_scope):
    qualified, sep, identifier = reference.partition("/")
    if project.flat_board:
        workflow = project.workflow
        stage, path = find_card(workflow, (identifier if sep else qualified).upper(), project.board, project)
        expected = qualified if sep else requested_scope
        if (expected and project.card_scope(path) != expected
                or stage not in {workflow["completed"], "cancellation"}):
            raise ValueError(f"{reference} is not a closed Card in that module.")
        print(path.relative_to(project.root))
        return 0
    scope = qualified if sep else PROJECT_SCOPE
    task_id = (identifier if sep else qualified).upper()
    if not (match := CARD_ID.fullmatch(task_id)) or match[1] != task_id:
        raise ValueError("Expected a Card ID or an archived module/Card ID.")
    if requested_scope is not None and requested_scope != scope:
        raise ValueError("The archived reference does not belong to the selected scope.")
    workspace = project.scope_workspace(scope)
    check_module_records(workspace)
    matching = [path for path in (workspace / "kanban").glob("*/*.md")
                if (match := CARD_ID.match(path.stem)) and match[1].upper() == task_id
                and stage_is_archive(project, scope, path)]
    if len(matching) != 1:
        raise ValueError(f"Expected one archived Card for {reference}, found {len(matching)}.")
    print(matching[0].relative_to(project.root))
    return 0


def stage_is_archive(project, scope, path):
    if scope != PROJECT_SCOPE:
        return path.parent.name in project.archived_stages(project.scope_workspace(scope))
    return (project.module_boards or project.card_scope(path, allow_legacy=True) is None) and path.parent.name in {
        load_workflow(project.board)["completed"], "cancellation",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", "--module", dest="global_scope", help="Module ID or @project")
    commands = parser.add_subparsers(dest="command", required=True)
    validation = commands.add_parser("validate")
    approval = commands.add_parser("verify-approval")
    approval.add_argument("batch_id")
    approval.add_argument("revision", help="Full commit ID from the trusted approval record")
    retirement = commands.add_parser("retire-specifications")
    retirement.add_argument("batch_id")
    retirement.add_argument("approval", help="Full commit ID from the trusted approval record")
    new = commands.add_parser("new")
    new.add_argument("title")
    new.add_argument("--owner", required=True)
    new.add_argument("--apply", action="store_true", help="Create the approved card")
    move = commands.add_parser("move")
    move.add_argument("task_id")
    move.add_argument("destination")
    move.add_argument("--owner-token", help="Recorded delivery owner for active module moves")
    reassign = commands.add_parser("reassign", help="Change the approved scope of a backlog Card")
    reassign.add_argument("task_id")
    reassign.add_argument("--to-scope", "--to-module", required=True)
    init = commands.add_parser("init")
    source = init.add_mutually_exclusive_group(required=True)
    source.add_argument("--template", choices=TEMPLATES)
    source.add_argument("--config", type=Path, help="Approved custom workflow JSON")
    init.add_argument("--wip-limit", type=int, help="Template WIP limit (default: 1)")
    init.add_argument("--timezone", help="Template IANA time zone (default: UTC)")
    init.add_argument("--with-batches", action="store_true", help="Set up project Specifications and Batches")
    init.add_argument("--apply", action="store_true", help="Apply the approved preview")
    board = commands.add_parser("show")
    board.add_argument("--wip-limit", type=int, help="WIP limit per scope for this display")
    board.add_argument("--timezone", help="IANA time zone for age")
    history = commands.add_parser("history", help="Find a frozen Card by its historical reference")
    history.add_argument("reference")
    locate = commands.add_parser("path", help="Resolve a stable Card ID to its current path")
    locate.add_argument("task_id")
    for command in (validation, approval, retirement, new, move, reassign, init, board, history, locate):
        command.add_argument("--scope", "--module", dest="scope", help="Module ID or @project")
    args = parser.parse_args()
    if args.scope and args.global_scope and args.scope != args.global_scope:
        parser.error("Conflicting scope selections.")
    scope = args.scope or args.global_scope
    id_field = {"move": "task_id", "verify-approval": "batch_id"}.get(args.command)
    if id_field:
        reference = getattr(args, id_field)
        if "/" in reference:
            qualified_module, _, local_id = reference.partition("/")
            if not qualified_module or not local_id or "/" in local_id:
                parser.error("Expected a qualified reference such as module/CARD-00000001.")
            if scope is not None and scope != qualified_module:
                parser.error("The qualified reference does not belong to the selected module.")
            if args.command == "move":
                parser.error("Use a project-wide Card ID for moves. Qualified historical Card IDs are read-only.")
            scope = qualified_module
            setattr(args, id_field, local_id)
    if args.command == "init" and args.config and (args.wip_limit is not None or args.timezone):
        init.error("Set wip_limit and timezone in the custom configuration.")
    try:
        scope = invocation_module(scope)
        project = board_context()
        root, workspace = project.root, project.board
        context = project if project.modules else None
        if scope is not None:
            project.validate_scope(scope)
        if context:
            check_module_records(workspace)
        if args.command == "history":
            return historical_path(project, args.reference, scope)
        if context:
            context.check_legacy_boards()
        if args.command in {"init", "new", "move", "reassign"}:
            specification_root(workspace if scope is None else project.scope_workspace(scope))
        if args.command == "init":
            if context and context.flat_board:
                raise ValueError("The workflow is defined in project/settings.json.")
            if scope is not None and scope != PROJECT_SCOPE:
                raise ValueError("The workflow is shared. Configure it in project scope.")
            if context and args.with_batches:
                raise ValueError("Set up Specifications and Batches in each selected module workspace.")
            return initialize(args, workspace, root)
        workflow = load_workflow(workspace, context=context)
        if args.command == "path":
            _, path = find_card(workflow, args.task_id.upper(), workspace, context)
            if scope is not None and context and context.card_scope(path) != scope:
                raise ValueError(f"{args.task_id} does not belong to {scope}.")
            print(path.relative_to(root))
            return 0
        if args.command == "retire-specifications":
            if context:
                raise ValueError("Use qualified closure retire for a module Batch.")
            if not re.fullmatch(r"Batch-[0-9]{3,}", args.batch_id):
                raise ValueError("Supply a Batch ID such as Batch-001.")
            description = Path("project/batches") / args.batch_id.lower() / "description.md"
            with board_write_lock(workspace):
                paths = retire_batch_specifications(root, Path("project"), description, args.approval)
            for path in paths:
                print(path)
            return 0
        if args.command == "verify-approval":
            if context and (scope is None or scope == PROJECT_SCOPE):
                raise ValueError("Select the Batch's module scope explicitly.")
            records = project.scope_workspace(scope) if context else workspace
            if context:
                check_module_records(records)
            return verify_approval(args.batch_id, args.revision, records, root)
        if args.command == "new":
            if context and context.module_boards and scope in (None, PROJECT_SCOPE):
                scope = context.misc_module
            if context and scope is None:
                raise ValueError("Choose a module scope or @project explicitly before creating a Card.")
            if context and context.module_boards:
                check_module_records(project.card_workspace(scope))
            lock = exclusive(coordination_root(root) / "projects" / project.id, "board-write") if context else None
            return create_card(workflow, args, workspace, root, scope=scope if context else None,
                               write_lock=lock, context=context)
        if args.command == "reassign":
            if not context or scope != PROJECT_SCOPE:
                raise ValueError("Reassignment requires explicit @project scope.")
            task_id = args.task_id.upper()
            target_scope = project.validate_scope(args.to_scope)
            if project.module_boards and target_scope == PROJECT_SCOPE:
                target_scope = project.misc_module
            check_module_records(project.scope_workspace(target_scope))
            directory = coordination_root(root) / "projects" / project.id

            def is_claimed(current_scope):
                state = Coordination(ROOT, current_scope).status()
                return bool(state and state.get("delivery") == task_id)

            with exclusive(directory, "board-write"):
                return reassign_card(workflow, task_id, project, target_scope, is_claimed)
        if args.command == "move":
            task_id = args.task_id.upper()
            if context:
                _, path = find_card(workflow, task_id, workspace, context)
                actual_scope = context.card_scope(path)
                if context.module_boards and path.is_relative_to(workspace / "kanban"):
                    raise ValueError("The project Kanban is historical. Move Cards on a module board.")
                if scope is not None and scope != actual_scope:
                    raise ValueError(f"{task_id} belongs to scope {actual_scope}, not {scope}.")
                scope = actual_scope
                coordination = Coordination(ROOT, scope)
                lock = exclusive(coordination.directory, f"module-{scope}")
                write_lock = exclusive(coordination.directory, "board-write")
                check_module_records(context.scope_workspace(scope))
            else:
                lock = nullcontext()
                write_lock = board_write_lock(workspace)

            def authorize(delivery):
                if not args.owner_token:
                    raise ValueError("Active scoped moves require the recorded --owner-token.")
                coordination.require_owner(args.owner_token, delivery)

            with lock, write_lock:
                return move_card(
                    workflow, task_id, args.destination, workspace, root,
                    authorize_active=authorize if context else None, context=context, scope=scope,
                )
        if args.command == "validate":
            return validate(workflow, workspace, project.modules.values(), root,
                            context=context, selected_scope=scope if context else None)
    except (OSError, ValueError, CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    if args.wip_limit is not None and args.wip_limit < 1:
        board.error("--wip-limit must be positive")
    try:
        today = datetime.now(ZoneInfo(args.timezone or workflow["timezone"])).date()
    except (KeyError, ValueError):
        board.error(f"unknown time zone: {args.timezone}")
    try:
        return show_board(workflow, args.wip_limit or workflow["wip_limit"], today, workspace, root,
                          context=context, scope=scope if context else None)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")



if __name__ == "__main__":
    raise SystemExit(main())
