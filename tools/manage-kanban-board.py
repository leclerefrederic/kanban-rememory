"""Initialize, validate, display, create, or move cards on a Markdown Kanban board."""

import argparse
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from kanban.batches import verify_approval
from kanban.cards import board_write_lock, create_card, move_card, show_board
from kanban.validation import validate
from kanban.workflow import TEMPLATES, initialize, load_workflow


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate")
    approval = commands.add_parser("verify-approval")
    approval.add_argument("lot_id")
    approval.add_argument("revision", help="Full commit ID from the trusted approval record")
    new = commands.add_parser("new")
    new.add_argument("title")
    new.add_argument("--owner", required=True)
    new.add_argument("--apply", action="store_true", help="Create the approved card")
    move = commands.add_parser("move")
    move.add_argument("task_id")
    move.add_argument("destination")
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
    args = parser.parse_args()
    if args.command == "init" and args.config and (args.wip_limit is not None or args.timezone):
        init.error("Set wip_limit and timezone in the custom configuration.")
    try:
        if args.command == "init":
            return initialize(args)
        workflow = load_workflow()
        if args.command == "verify-approval":
            return verify_approval(args.lot_id, args.revision)
        if args.command == "new":
            return create_card(workflow, args)
        if args.command == "move":
            with board_write_lock():
                return move_card(workflow, args.task_id.upper(), args.destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")
    if args.command == "validate":
        return validate(workflow)
    if args.wip_limit is not None and args.wip_limit < 1:
        board.error("--wip-limit must be positive")
    try:
        today = datetime.now(ZoneInfo(args.timezone or workflow["timezone"])).date()
    except (KeyError, ValueError):
        board.error(f"unknown time zone: {args.timezone}")
    return show_board(workflow, args.wip_limit or workflow["wip_limit"], today)



if __name__ == "__main__":
    raise SystemExit(main())
