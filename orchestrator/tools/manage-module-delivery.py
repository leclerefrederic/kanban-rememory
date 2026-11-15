"""Inspect or update an authorized module delivery in this Git clone."""

import argparse
import json
import re
import subprocess
import sys

from kanban.coordination import Coordination
from kanban.files import ROOT
from kanban.runtime import run_check


DELIVERY = re.compile(r"CARD-[0-9]{8}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", "--scope", help="Module ID from project settings")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    claim = commands.add_parser("claim")
    add_card = commands.add_parser("add-card", help="Add a backlog Card to the active phase")
    checkpoint = commands.add_parser("checkpoint")
    integration = commands.add_parser("integration")
    integration.add_argument("action", choices=("begin", "verify", "release"))
    finish = commands.add_parser("finish")
    finish.add_argument("--revision", required=True, help="Full verified closing revision")
    milestone = commands.add_parser("milestone")
    milestone.add_argument("event", help="Stable milestone identifier")
    milestone.add_argument("--summary", required=True)
    milestone.add_argument("--revision", required=True)
    milestone.add_argument("--evidence", help="Evidence path relative to the control checkout for local notes")
    milestone.add_argument("--published", action="store_true", help="Record the verified publication in the project journal")
    run = commands.add_parser("run-check")
    run.add_argument("--integration-checkout", help="Exact combined revision checkout")
    publish_card = commands.add_parser("publish-card")
    publish_card.add_argument("--closing", required=True)
    for command in (claim, add_card, checkpoint, integration, finish, milestone, run, publish_card):
        command.add_argument("delivery")
        command.add_argument("--owner", required=True, help="Recorded session ownership ID")
    add_card.add_argument("card", help="Backlog Card to join to the phase")
    claim.add_argument("--base", required=True, help="Approved base commit")
    checkpoint.add_argument("label", help="Next action or point of resumption")
    argv = sys.argv[1:]
    if "--" in argv:
        delimiter = argv.index("--")
        argv, command = argv[:delimiter], argv[delimiter + 1:]
    else:
        command = []
    args = parser.parse_args(argv)
    if command and args.command != "run-check":
        parser.error("Only run-check accepts a command after --.")
    try:
        coordination = Coordination(ROOT, args.module)
        if args.command == "status":
            state = coordination.status()
        else:
            if not DELIVERY.fullmatch(args.delivery) or not args.owner.strip():
                raise ValueError("Use the tracked Card ID and a nonempty owner ID.")
            if args.command == "claim":
                state = coordination.claim(args.owner, args.delivery, args.base)
            elif args.command == "add-card":
                if not DELIVERY.fullmatch(args.card):
                    raise ValueError("Use the tracked Card ID.")
                state = coordination.add_card(args.owner, args.delivery, args.card)
            elif args.command == "checkpoint":
                state = coordination.checkpoint(args.owner, args.delivery, args.label)
            elif args.command == "finish":
                state = coordination.finish(args.owner, args.delivery, args.revision)
            elif args.command == "milestone":
                if not re.fullmatch(r"[A-Za-z0-9_-]+", args.event):
                    raise ValueError("Use a stable alphanumeric milestone identifier.")
                state = coordination.milestone(args.owner, args.delivery, args.event, args.summary,
                                              args.revision, args.evidence, args.published)
            elif args.command == "publish-card":
                state = coordination.publish_card(args.owner, args.delivery, args.closing)
            elif args.command == "run-check":
                return run_check(coordination, args.owner, args.delivery, command, args.integration_checkout)
            else:
                state = coordination.integration(args.action, args.owner, args.delivery)
        print(json.dumps(state, indent=2))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
