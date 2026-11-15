"""Inspect or update an authorized module delivery in this Git clone."""

import argparse
import json
import re
import subprocess

from kanban.coordination import Coordination
from kanban.files import ROOT
from kanban.project import invocation_module


DELIVERY = re.compile(r"(?:CARD-[0-9]{8}|Batch-[0-9]{3,})")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", help="Module ID from the root project.json")
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
    milestone.add_argument("--evidence", required=True, help="Evidence path relative to the control checkout")
    milestone.add_argument("--shared", action="store_true", help="Also record the impact in the global journal")
    for command in (claim, checkpoint, integration, finish, milestone):
        command.add_argument("delivery")
        command.add_argument("--owner", required=True, help="Recorded session ownership ID")
    claim.add_argument("--base", required=True, help="Approved base commit")
    claim.add_argument("--approval", help="Trusted full Batch approval commit")
    checkpoint.add_argument("label", help="Next action or point of resumption")
    args = parser.parse_args()
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
                                              args.revision, args.evidence, args.shared)
            else:
                state = coordination.integration(args.action, args.owner, args.delivery)
        print(json.dumps(state, indent=2))
    except (OSError, subprocess.CalledProcessError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
