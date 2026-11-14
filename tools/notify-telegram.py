"""Preview or send Telegram notifications for Delivery Batch events."""

import argparse
import json
import os
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
from urllib.request import Request, urlopen


def send_message(token, chat, message):
    body = json.dumps({"chat_id": chat, "text": message}).encode()
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"},
    )
    with urlopen(request, timeout=15) as response:
        if json.load(response).get("ok") is not True:
            raise ValueError("Telegram did not confirm delivery.")


def notify(args, token, chat, ledger, sender=send_message):
    if args.event == "test":
        sender(token, chat, "Kanban Rememory notification test.")
        return True

    messages = {
        "delivered": "Ready for acceptance. Review tests.md.",
        "blocked": f"Action needed. Review report.md for blocker {args.blocker_id}.",
        "closed": "Closure verified. See the outcome in report.md.",
    }
    key = (chat, args.batch, args.event, args.blocker_id or "")
    with sqlite3.connect(ledger, timeout=20) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS sent (chat TEXT, batch TEXT, event TEXT, blocker TEXT,"
            " PRIMARY KEY (chat, batch, event, blocker))"
        )
        connection.execute("BEGIN IMMEDIATE")
        if connection.execute("SELECT 1 FROM sent WHERE (chat,batch,event,blocker) = (?,?,?,?)", key).fetchone():
            return False
        sender(token, chat, f"{args.batch}: {messages[args.event]}")
        connection.execute("INSERT INTO sent VALUES (?,?,?,?)", key)
        return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", choices=("test", "delivered", "blocked", "closed"))
    parser.add_argument("--batch")
    parser.add_argument("--blocker-id")
    parser.add_argument("--send-to", help="Explicitly confirm the configured numeric chat ID")
    args = parser.parse_args()
    if args.event != "test" and not re.fullmatch(r"Batch-[0-9]+", args.batch or "", re.IGNORECASE):
        parser.error("Provide a Batch ID such as Batch-001.")
    if args.event != "test":
        args.batch = "Batch-" + args.batch.split("-", 1)[1]
    if args.event == "blocked" and not re.fullmatch(r"[A-Za-z0-9-]{1,40}", args.blocker_id or ""):
        parser.error("Provide a stable blocker ID.")
    if args.event != "blocked" and args.blocker_id is not None:
        parser.error("--blocker-id is only for blocked events.")

    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    events = os.environ.get("TELEGRAM_EVENTS", "").split(",")
    if args.event != "test" and args.event not in events:
        print("Telegram event disabled.")
        return 0
    if not re.fullmatch(r"-?[0-9]+", chat):
        parser.error("Set TELEGRAM_CHAT_ID to the numeric destination.")
    if args.send_to is None:
        print(f"Preview: {args.event} notification to chat {chat}. Confirm with --send-to {chat}.")
        return 0
    if args.send_to != chat:
        parser.error("Confirmed destination does not match TELEGRAM_CHAT_ID.")
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]+", token):
        parser.error("Set TELEGRAM_BOT_TOKEN in the execution environment.")
    try:
        root = Path(__file__).resolve().parents[1]
        git_dir = subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=root, text=True,
        ).strip()
        sent = notify(args, token, chat, Path(git_dir) / "telegram-notifications.sqlite3")
    except (OSError, ValueError, sqlite3.Error, subprocess.CalledProcessError):
        # Network exceptions can contain the request URL and token.
        print("Telegram delivery could not be confirmed. Check the token, chat access, and network.", file=sys.stderr)
        return 1
    print("Telegram confirmed delivery." if sent else "Notification already recorded as sent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
