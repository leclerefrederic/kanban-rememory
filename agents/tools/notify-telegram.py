"""Preview or send Telegram alerts: intervention needed, task completed."""

import argparse
import json
import os
from pathlib import Path
import re
import socket
import sqlite3
import subprocess
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ICONS = {"attention": "🔔", "completed": "✅"}
LABELS = {"attention": "Intervention needed", "completed": "Task completed"}
LEGACY = {"delivered": "attention", "blocked": "attention", "closed": "completed"}


class SendFailed(Exception):
    """A send that failed. `definite` is true when Telegram certainly did not deliver the message."""

    def __init__(self, definite):
        super().__init__("send failed")
        self.definite = definite


def send_message(token, chat, message):
    body = json.dumps({"chat_id": chat, "text": message}).encode()
    request = Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body, headers={"Content-Type": "application/json"},
    )
    # Network exceptions can contain the request URL and token: raise only a bare failure.
    try:
        with urlopen(request, timeout=15) as response:
            confirmed = json.load(response).get("ok") is True
    except HTTPError as error:
        raise SendFailed(error.code < 500) from None
    except URLError as error:
        raise SendFailed(isinstance(error.reason, (socket.gaierror, ConnectionRefusedError))) from None
    except (OSError, ValueError):
        raise SendFailed(False) from None  # Timeout or bad reply: the message may have been delivered.
    if not confirmed:
        raise SendFailed(True)


def describe(args):
    """Return (kind, task, id, label, text) for the alert, mapping the Batch events."""
    kind = LEGACY.get(args.event, args.event)
    label = args.label or LABELS[kind]
    if args.event == "delivered":
        text = args.text or f"{args.batch} is ready for acceptance (revision {args.revision[:7]}). Review tests.md."
        return kind, args.task or args.batch, f"{args.batch}@{args.revision}", label, text
    if args.event == "blocked":
        text = args.text or f"Action needed. Review report.md for blocker {args.blocker_id}."
        return kind, args.task or args.batch, f"{args.batch}:{args.blocker_id}", label, text
    if args.event == "closed":
        text = args.text or "Closure verified. See the outcome in report.md."
        return kind, args.task or args.batch, args.batch, label, text
    return kind, args.task, args.id, label, args.text


def render(kind, project, task, label, text, chat_name, link):
    lines = [f"{ICONS[kind]} {label}", f"{project} — {task}", text]
    if chat_name:
        lines.append(f"💬 {chat_name}")
    if link:
        lines.append(link)
    return "\n".join(lines)


def notify(args, token, chat, ledger, sender=send_message, project="project"):
    """Send once per alert. Return 'sent', 'duplicate', 'unconfirmed' (resend blocked) or 'failed'."""
    if args.event == "test":
        sender(token, chat, "Kanban Rememory notification test.")
        return "sent"

    kind, task, ident, label, text = describe(args)
    message = render(kind, project, task, label, text, args.chat_name, args.link)
    key = (chat, project, kind, ident)
    with sqlite3.connect(ledger, timeout=20) as connection:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS alerts (chat TEXT, project TEXT, kind TEXT, ident TEXT, state TEXT,"
            " PRIMARY KEY (chat, project, kind, ident))"
        )
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute(
            "SELECT state FROM alerts WHERE (chat,project,kind,ident) = (?,?,?,?)", key).fetchone()
        if row and row[0] == "sent":
            return "duplicate"
        if row and not args.confirm_retry:
            return "unconfirmed"
        # Record the attempt before sending so an interrupted send is never treated as not attempted.
        connection.execute("INSERT OR REPLACE INTO alerts VALUES (?,?,?,?,'unconfirmed')", key)
        connection.commit()
        connection.execute("BEGIN IMMEDIATE")
        try:
            sender(token, chat, message)
        except SendFailed as failure:
            if failure.definite:
                connection.execute("DELETE FROM alerts WHERE (chat,project,kind,ident) = (?,?,?,?)", key)
                connection.commit()
                return "failed"
            connection.commit()
            return "unconfirmed"
        connection.execute("UPDATE alerts SET state='sent' WHERE (chat,project,kind,ident) = (?,?,?,?)", key)
        return "sent"


STATUS = {
    "sent": ("Telegram: confirmed delivery.", 0),
    "duplicate": ("Telegram: this alert was already confirmed; not sent again.", 0),
    "unconfirmed": ("Telegram: delivery not confirmed and the outcome is unknown. Check the destination, then "
                    "rerun with --confirm-retry to send again.", 2),
    "failed": ("Telegram: not sent, the request was refused. Retrying is safe.", 1),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("event", choices=("test", "attention", "completed", *LEGACY))
    parser.add_argument("--task", help="the requested task in human-readable terms")
    parser.add_argument("--id", help="stable ID of the request or task, used to avoid duplicates")
    parser.add_argument("--text", help="what is waiting, or the verified result, in the conversation language")
    parser.add_argument("--label", help="localized heading; defaults to the English one")
    parser.add_argument("--chat-name", help="title of the conversation to resume, with the application")
    parser.add_argument("--link", help="direct link to the conversation, only if the environment provides one")
    parser.add_argument("--project", help="project name; defaults to the repository folder name")
    parser.add_argument("--batch")
    parser.add_argument("--blocker-id")
    parser.add_argument("--revision", help="full tested commit, required for delivered")
    parser.add_argument("--send-to", help="Explicitly confirm the configured numeric chat ID")
    parser.add_argument("--confirm-retry", action="store_true",
                        help="send again after checking the destination of an unconfirmed alert")
    args = parser.parse_args()
    if args.event in ("attention", "completed"):
        if not all((args.task, args.text, args.chat_name)) or not re.fullmatch(r"[A-Za-z0-9@:._-]{1,80}", args.id or ""):
            parser.error("Provide --task, --id (letters, digits and @:._-), --text and --chat-name.")
        if args.batch or args.blocker_id or args.revision:
            parser.error("--batch, --blocker-id and --revision belong to the Batch events.")
    if args.event in LEGACY and not re.fullmatch(r"Batch-[0-9]+", args.batch or "", re.IGNORECASE):
        parser.error("Provide a Batch ID such as Batch-001.")
    if args.event in LEGACY:
        args.batch = "Batch-" + args.batch.split("-", 1)[1]
    if args.event == "blocked" and not re.fullmatch(r"[A-Za-z0-9-]{1,40}", args.blocker_id or ""):
        parser.error("Provide a stable blocker ID.")
    if args.event != "blocked" and args.blocker_id is not None:
        parser.error("--blocker-id is only for blocked events.")
    if args.event == "delivered" and not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", args.revision or ""):
        parser.error("Provide the full tested commit with --revision.")
    if args.event != "delivered" and args.revision is not None:
        parser.error("--revision is only for delivered events.")
    if args.link and not re.fullmatch(r"[a-z][a-z0-9+.-]*://\S+", args.link, re.IGNORECASE):
        parser.error("--link must be a full address such as https://example.invalid/chat.")

    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    events = os.environ.get("TELEGRAM_EVENTS", "").split(",")
    wanted = args.event if args.event == "test" else LEGACY.get(args.event, args.event)
    if args.event != "test" and not ({args.event, wanted} & set(events)):
        print("Telegram: this event is disabled; nothing was sent.")
        return 0
    if not re.fullmatch(r"-?[0-9]+", chat):
        parser.error("Set TELEGRAM_CHAT_ID to the numeric destination. Nothing was sent.")
    if args.send_to is None:
        print(f"Preview: {args.event} notification to chat {chat}. Confirm with --send-to {chat}.")
        return 0
    if args.send_to != chat:
        parser.error("Confirmed destination does not match TELEGRAM_CHAT_ID.")
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]+", token):
        parser.error("Set TELEGRAM_BOT_TOKEN in the execution environment. Nothing was sent.")
    try:
        root = Path(__file__).resolve().parents[2]
        git_dir = subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=root, text=True,
        ).strip()
        project = args.project or root.name
        outcome = notify(args, token, chat, Path(git_dir) / "telegram-notifications.sqlite3", project=project)
    except (OSError, ValueError, sqlite3.Error, subprocess.CalledProcessError, SendFailed):
        # Network exceptions can contain the request URL and token.
        print("Telegram: delivery could not be confirmed. Check the token, chat access, and network.", file=sys.stderr)
        return 2
    message, code = STATUS[outcome]
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
