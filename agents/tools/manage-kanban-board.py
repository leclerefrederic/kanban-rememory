"""Initialize, validate, display, create, or move cards on a Markdown Kanban board."""

import argparse
from contextlib import nullcontext
from datetime import datetime
from pathlib import Path
from subprocess import CalledProcessError
from zoneinfo import ZoneInfo

from kanban.batches import verify_approval
from kanban.cards import board_write_lock, create_card, move_card, show_board
from kanban.coordination import Coordination, exclusive
from kanban.files import ROOT, check_module_records
from kanban.project import control_workspace, invocation_module, load_project
from kanban.validation import validate
from kanban.workflow import TEMPLATES, initialize, load_workflow


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", dest="global_module", help="Select a configured module")
    commands = parser.add_subparsers(dest="command", required=True)
    validation = commands.add_parser("validate")
    approval = commands.add_parser("verify-approval")
    approval.add_argument("batch_id")
    approval.add_argument("revision", help="Full commit ID from the trusted approval record")
    new = commands.add_parser("new")
    new.add_argument("title")
    new.add_argument("--owner", required=True)
    new.add_argument("--apply", action="store_true", help="Create the approved card")
    move = commands.add_parser("move")
    move.add_argument("task_id")
    move.add_argument("destination")
    move.add_argument("--owner-token", help="Recorded delivery owner for active module moves")
    init = commands.add_parser("init")
    source = init.add_mutually_exclusive_group(required=True)
    source.add_argument("--template", choices=TEMPLATES)
    source.add_argument("--config", type=Path, help="Approved custom workflow JSON")
    init.add_argument("--wip-limit", type=int, help="Template WIP limit (default: 1)")
    init.add_argument("--timezone", help="Template IANA time zone (default: UTC)")
    init.add_argument("--apply", action="store_true", help="Apply the approved preview")
    board = commands.add_parser("show")
    board.add_argument("--wip-limit", type=int, help="Overall WIP limit for this board")
    board.add_argument("--timezone", help="IANA time zone for age")
    for command in (validation, approval, new, move, init, board):
        command.add_argument("--module", help="Select a configured module")
    args = parser.parse_args()
    if args.module and args.global_module and args.module != args.global_module:
        parser.error("Conflicting module selections.")
    module = args.module or args.global_module
    id_field = {"move": "task_id", "verify-approval": "batch_id"}.get(args.command)
    if id_field:
        reference = getattr(args, id_field)
        if "/" in reference:
            qualified_module, _, local_id = reference.partition("/")
            if not qualified_module or not local_id or "/" in local_id:
                parser.error("Expected a qualified reference such as module/CARD-00000001.")
            if module is not None and module != qualified_module:
                parser.error("The qualified reference does not belong to the selected module.")
            module = qualified_module
            setattr(args, id_field, local_id)
    if args.command == "init" and args.config and (args.wip_limit is not None or args.timezone):
        init.error("Set wip_limit and timezone in the custom configuration.")
    try:
        module = invocation_module(module)
        local = load_project(ROOT)
        if (ROOT / ".git").exists() or local.modules:
            root, workspace = control_workspace(local, module)
        else:
            root, workspace = ROOT, local.workspace(module)
        project = load_project(root)
        if project.modules:
            check_module_records(workspace)
        if args.command == "init":
            return initialize(args, workspace, root)
        workflow = load_workflow(workspace)
        if args.command == "verify-approval":
            return verify_approval(args.batch_id, args.revision, workspace, root)
        if args.command == "new":
            return create_card(workflow, args, workspace, root)
        if args.command == "move":
            coordination = Coordination(ROOT, module) if project.modules else None
            lock = exclusive(coordination.directory, f"module-{coordination.module}") if coordination else nullcontext()

            def authorize(delivery):
                if not args.owner_token:
                    raise ValueError("Active module moves require the recorded --owner-token.")
                coordination.require_owner(args.owner_token, delivery)

            with lock, board_write_lock(workspace):
                return move_card(
                    workflow, args.task_id.upper(), args.destination, workspace, root,
                    authorize_active=authorize if coordination else None,
                )
        if args.command == "validate":
            return validate(workflow, workspace, project.modules.values(), root)
    except (OSError, ValueError, CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    if args.wip_limit is not None and args.wip_limit < 1:
        board.error("--wip-limit must be positive")
    try:
        today = datetime.now(ZoneInfo(args.timezone or workflow["timezone"])).date()
    except (KeyError, ValueError):
        board.error(f"unknown time zone: {args.timezone}")
    return show_board(workflow, args.wip_limit or workflow["wip_limit"], today, workspace, root)



if __name__ == "__main__":
    raise SystemExit(main())
