"""Tell Kanban Rememory Runner (KRR) that this session waits for the user or has resumed.

Only a session started by KRR defines KRR_SESSION_DIR; elsewhere the command refuses and writes nothing.
"""

import argparse
import json
import os
from pathlib import Path
import re
import sys
import time


def signal(event, ident, directory):
    """Append one line to signals.jsonl in the session directory."""
    folder = Path(directory or "")
    if not directory or not folder.is_dir():
        raise ValueError("Not in a KRR session: KRR_SESSION_DIR is unset or missing. Nothing was written.")
    line = {"event": event, "time": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    if event == "waiting":
        line["id"] = ident
    # One short append is atomic enough for the single reader that polls this file.
    with open(folder / "signals.jsonl", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(line) + "\n")


def main(argv=None, environ=os.environ):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", choices=("waiting", "resumed"))
    parser.add_argument("--id", help="unique ID of this request to the user (required for waiting)")
    args = parser.parse_args(argv)
    if args.event == "waiting" and not re.fullmatch(r"[A-Za-z0-9._-]{1,80}", args.id or ""):
        parser.error("waiting needs --id with letters, digits, dot, underscore or dash.")
    if args.event == "resumed" and args.id is not None:
        parser.error("--id is only for waiting.")
    try:
        signal(args.event, args.id, environ.get("KRR_SESSION_DIR"))
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"KRR signal recorded: {args.event}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
