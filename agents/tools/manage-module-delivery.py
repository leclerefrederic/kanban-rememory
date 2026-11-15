"""Inspect or update an authorized module delivery in this Git clone."""

import argparse
import json
import re
import subprocess
import sys

from kanban.closure import Closure
from kanban.coordination import Coordination
from kanban.files import ROOT
from kanban.project import invocation_module
from kanban.runtime import run_check


DELIVERY = re.compile(r"(?:CARD-[0-9]{8}|Batch-[0-9]{3,})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", "--scope", help="Module ID from project.json or @project")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("status")
    claim = commands.add_parser("claim")
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
    closure = commands.add_parser("closure")
    closure.add_argument("action", choices=("retire", "prepare", "publish"))
    closure.add_argument("--closing")
    closure.add_argument("--integration-checkout", help="Separate worktree preparing the closing commit")
    closure.add_argument("--candidate")
    closure.add_argument("--result", choices=("accepted", "rejected"))
    run = commands.add_parser("run-check")
    run.add_argument("--integration-checkout", help="Exact combined revision checkout")
    publish_card = commands.add_parser("publish-card")
    publish_card.add_argument("--closing", required=True)
    for command in (claim, checkpoint, integration, finish, milestone, closure, run, publish_card):
        command.add_argument("delivery")
        command.add_argument("--owner", required=True, help="Recorded session ownership ID")
    claim.add_argument("--base", required=True, help="Approved base commit")
    claim.add_argument("--approval", help="Trusted full Batch approval commit")
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
        coordination = Coordination(ROOT, invocation_module(args.module))
        if args.command == "status":
            state = coordination.status()
        else:
            if not DELIVERY.fullmatch(args.delivery) or not args.owner.strip():
                raise ValueError("Use the tracked Card or Batch ID and a nonempty owner ID.")
            if args.command == "claim":
                state = coordination.claim(args.owner, args.delivery, args.base, args.approval)
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
            elif args.command == "closure":
                action = Closure(coordination, args.owner, args.delivery)
                if args.action == "retire":
                    if not args.integration_checkout:
                        raise ValueError("Supply the separate integration checkout for retirement.")
                    state = action.retire(args.integration_checkout)
                elif args.action == "prepare":
                    if not all((args.closing, args.candidate, args.result)):
                        raise ValueError("Prepare closure with closing commit, candidate and User decision.")
                    state = action.prepare(args.closing, args.candidate, args.result)
                else:
                    state = action.publish()
            elif args.command == "run-check":
                return run_check(coordination, args.owner, args.delivery, command, args.integration_checkout)
            else:
                state = coordination.integration(args.action, args.owner, args.delivery)
        print(json.dumps(state, indent=2))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
