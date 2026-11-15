"""Kanban Rememory: the module boards, one delivery phase at a time, and project setup."""

import argparse
from pathlib import Path
import re
import subprocess
import sys

from kanban import board
from kanban.phase import Phase
from kanban.project import init, load_project
from kanban.validation import validate

ROOT = Path(__file__).resolve().parents[2]


def card(value):
    value = value.upper()
    if not re.fullmatch(r"CARD-[0-9]{8}", value):
        raise argparse.ArgumentTypeError("expected a Card ID such as CARD-00000001")
    return value


def split(argv):
    """Separate the kr arguments from the check commands; each command follows its own --."""
    if "--" not in argv:
        return argv, []
    index = argv.index("--")
    commands = [[]]
    for item in argv[index + 1:]:
        if item == "--":
            commands.append([])
        else:
            commands[-1].append(item)
    return argv[:index], [command for command in commands if command]


def main(argv=None, root=ROOT):
    argv, commands = split(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("show", help="the active phase and the boards")
    show.add_argument("--module")
    sub.add_parser("validate", help="check the records and documents of this checkout")
    path = sub.add_parser("path", help="the current file of a Card")
    path.add_argument("card", type=card)
    new = sub.add_parser("new", help="create a backlog Card")
    new.add_argument("title")
    new.add_argument("--module", default="misc")
    new.add_argument("--body", action="store_true", help="read the Card body, below its title, from stdin")
    move = sub.add_parser("move", help="move a Card to another stage")
    move.add_argument("card", type=card)
    move.add_argument("stage")
    start = sub.add_parser("start", help="open the phase with a Card, or add its next Card")
    start.add_argument("card", type=card)
    where = start.add_mutually_exclusive_group()
    where.add_argument("--main", action="store_true", help="first Card: deliver directly on main")
    where.add_argument("--release", action="store_true", help="first Card: deliver on a release branch, tagged when published")
    start.add_argument("--bump", choices=("patch", "minor", "major"), default="patch", help="release number step")
    sub.add_parser("check", help="validate, then run each command given after --, on the clean phase branch")
    publish = sub.add_parser("publish", help="after approval: close the Cards, commit, push to origin/main, end the phase")
    publish.add_argument("--summary", help="one line for the journal and the delivery alert")
    publish.add_argument("--approval", help="the user's approval, quoted")
    publish.add_argument("--notify", metavar="CHAT", help="send the Remy delivery alert, naming the chat to return to")
    publish.add_argument("--language", choices=("en", "fr"), default="en", help="language of the alert labels")
    setup = sub.add_parser("init", help="create the settings and boards from an approved proposal")
    setup.add_argument("settings", type=Path)
    setup.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    if commands and args.command != "check":
        parser.error("Only check takes commands after --.")
    try:
        if args.command == "init":
            return init(root, args.settings, args.apply)
        project = load_project(root)
        phase = Phase(project)
        if args.command == "show":
            if args.module:
                project.board(args.module)
            return board.show(project, args.module, phase.state(), phase.next_action())
        if args.command == "validate":
            return validate(project)
        if args.command == "path":
            print(board.find_card(project, args.card)[2].relative_to(root))
        elif args.command == "new":
            phase.guard_write()
            board.new(project, args.title, args.module, sys.stdin.read() if args.body else None)
        elif args.command == "move":
            board.move(project, args.card, args.stage, phase.guard_move)
        elif args.command == "start":
            return phase.start(args.card, "main" if args.main else "release" if args.release else None, args.bump)
        elif args.command == "check":
            return phase.check(commands)
        else:
            return phase.publish(args.summary, args.approval, args.notify, args.language)
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
