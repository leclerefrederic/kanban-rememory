"""Validate, display, create, locate, or move Cards on the module Kanbans."""

import argparse
from datetime import datetime
from subprocess import CalledProcessError
from zoneinfo import ZoneInfo

from kanban.cards import create_card, find_card, move_card, show_board
from kanban.coordination import Coordination, exclusive
from kanban.files import ROOT
from kanban.project import MISC, coordination_root, load_project, primary_worktree
from kanban.validation import validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", "--module", dest="global_scope", help="Module ID")
    commands = parser.add_subparsers(dest="command", required=True)
    validation = commands.add_parser("validate")
    new = commands.add_parser("new")
    new.add_argument("title")
    new.add_argument("--owner", required=True)
    new.add_argument("--apply", action="store_true", help="Create the approved card")
    move = commands.add_parser("move")
    move.add_argument("task_id")
    move.add_argument("destination")
    move.add_argument("--owner-token", help="Recorded delivery owner for active moves")
    board = commands.add_parser("show")
    board.add_argument("--wip-limit", type=int, help="WIP limit per module for this display")
    board.add_argument("--timezone", help="IANA time zone for age")
    locate = commands.add_parser("path", help="Resolve a stable Card ID to its current path")
    locate.add_argument("task_id")
    for command in (validation, new, move, board, locate):
        command.add_argument("--scope", "--module", dest="scope", help="Module ID")
    args = parser.parse_args()
    if args.scope and args.global_scope and args.scope != args.global_scope:
        parser.error("Conflicting scope selections.")
    scope = args.scope or args.global_scope
    if args.command == "show" and args.wip_limit is not None and args.wip_limit < 1:
        board.error("--wip-limit must be positive")
    try:
        # Tracking records live in the primary checkout, even when called from a worktree.
        project = load_project(primary_worktree(ROOT))
        if scope is not None:
            project.validate_scope(scope)
        project.check_boards()
        if args.command == "validate":
            return validate(project, scope, ROOT)
        if args.command == "path":
            _, path = find_card(project, args.task_id.upper())
            if scope is not None and project.card_scope(path) != scope:
                raise ValueError(f"{args.task_id} does not belong to {scope}.")
            print(path.relative_to(project.root))
            return 0
        directory = coordination_root(ROOT) / "projects" / project.id
        if args.command == "new":
            return create_card(project, args.title, args.owner, scope or MISC, args.apply,
                               exclusive(directory, "board-write"))
        if args.command == "move":
            task_id = args.task_id.upper()
            _, path = find_card(project, task_id)
            actual = project.card_scope(path)

            def authorize(module, delivery):
                if not args.owner_token:
                    raise ValueError("Active moves require the recorded --owner-token.")
                Coordination(ROOT, module).require_owner(args.owner_token, delivery, member=True)

            with exclusive(directory, f"module-{actual}"), exclusive(directory, "board-write"):
                return move_card(project, task_id, args.destination, authorize, scope)
        try:
            today = datetime.now(ZoneInfo(args.timezone or project.workflow["timezone"])).date()
        except (KeyError, ValueError):
            board.error(f"unknown time zone: {args.timezone}")
        return show_board(project, args.wip_limit or project.workflow["wip_limit"], today, scope=scope)
    except (OSError, ValueError, CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
