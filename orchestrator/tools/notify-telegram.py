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
LABELS = {
    "en": {"attention": "Action required", "completed": "Work completed",
           "project": "Project", "reference": "Reference", "summary": "Summary", "next_action": "Next action",
           },
    "fr": {"attention": "Action requise", "completed": "Travail terminé",
           "project": "Projet", "reference": "Référence", "summary": "Résumé", "next_action": "Prochaine action",
           },
}


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


def labels_for(args):
    """English is the unknown-language fallback; the agent supplies other translations."""
    labels = dict(LABELS.get(args.language, LABELS["en"]))
    for field in ("project", "reference", "summary", "next_action"):
        value = getattr(args, field + "_label", None)
        if value:
            labels[field] = value
    return labels


def describe(args):
    """Return (kind, task, id, label, text)."""
    return args.event, args.task, args.id, args.label or labels_for(args)[args.event], args.text


def render(args, project):
    kind, task, ident, label, text = describe(args)
    labels = labels_for(args)
    icon = ICONS[kind]
    label = label.removeprefix(icon).lstrip()
    action = args.next_action
    if args.chat_name:
        action += f" — {args.chat_name}"
    if args.link:
        action += f"\n{args.link}"
    reference = f"{args.module} / {args.reference}"
    return (f"{icon} {label}\n\n"
            f"{labels['project']}: {project}\n"
            f"{labels['reference']}: {reference}\n"
            f"{labels['summary']}: {text}\n\n"
            f"{labels['next_action']}: {action}")


def receipt_ident(task, ident, module, reference):
    # JSON avoids delimiter collisions; text, language and chat name are deliberately absent.
    return "v3:" + json.dumps([module, reference, task, ident], ensure_ascii=False, separators=(",", ":"))


def notify(args, token, chat, ledger, sender=send_message, project="project", project_id=None):
    """Send once per alert. Return 'sent', 'duplicate', 'unconfirmed' (resend blocked) or 'failed'."""
    if args.event == "test":
        sender(token, chat, "Kanban Rememory notification test.")
        return "sent"

    kind, task, ident, label, text = describe(args)
    ident = receipt_ident(task, ident, args.module, args.reference)
    message = render(args, project)
    key = (chat, project_id if project_id is not None else project, kind, ident)
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
    parser.add_argument("event", choices=("test", "attention", "completed"))
    parser.add_argument("--task", help="the requested task in human-readable terms")
    parser.add_argument("--id", help="stable ID of the request or task, used to avoid duplicates")
    parser.add_argument("--text", help="summary in the conversation language, at most two sentences")
    parser.add_argument("--reference", help="Card ID for attention/completed events")
    parser.add_argument("--next-action", help="specific action and where to act, or explicitly no action required")
    parser.add_argument("--language", default="en", help="conversation language (en/fr built in); unknown defaults to en")
    for field in ("project", "reference", "summary", "next-action"):
        parser.add_argument("--" + field + "-label", help="translated field label for other conversation languages")
    parser.add_argument("--label", help="translated hook text without the emoji; defaults to the selected language")
    parser.add_argument("--chat-name", help="title of the conversation to resume, with the application")
    parser.add_argument("--link", help="direct link to the conversation, only if the environment provides one")
    parser.add_argument("--project", help="display name; defaults to the configured project name or repository folder name")
    parser.add_argument("--module", "--scope", help="owning module ID; optional with a single module")
    parser.add_argument("--send-to", help="Explicitly confirm the configured numeric chat ID")
    parser.add_argument("--confirm-retry", action="store_true",
                        help="send again after checking the destination of an unconfirmed alert")
    args = parser.parse_args()
    if args.event == "test" and args.module is not None:
        parser.error("--module is only for work alerts.")
    if args.event != "test":
        if not all((args.task, args.text, args.chat_name)) or not re.fullmatch(r"[A-Za-z0-9@:._-]{1,80}", args.id or ""):
            parser.error("Provide --task, --id (letters, digits and @:._-), --text and --chat-name.")
        if not (args.next_action and args.next_action.strip()):
            parser.error("Provide --text (brief summary) and --next-action for every alert.")
        if not re.fullmatch(r"CARD-[0-9]{8}", args.reference or "", re.IGNORECASE):
            parser.error("Provide --reference with the relevant Card ID.")
        args.reference = args.reference.upper()
        if args.language not in LABELS and not all(
            (args.label, args.project_label, args.reference_label, args.summary_label, args.next_action_label)
        ):
            parser.error("For another known language, translate --label and all field labels.")
        for field in ("task", "id", "text", "next_action", "chat_name", "label", "project",
                      "project_label", "reference_label", "summary_label", "next_action_label"):
            value = getattr(args, field, None)
            if value is not None and (not value.strip() or "\n" in value or "\r" in value):
                parser.error("Alert fields must be nonempty single lines.")
    if args.link and not re.fullmatch(r"[a-z][a-z0-9+.-]*://\S+", args.link, re.IGNORECASE):
        parser.error("--link must be a full address such as https://example.invalid/chat.")

    chat = os.environ.get("TELEGRAM_CHAT_ID", "")
    events = os.environ.get("TELEGRAM_EVENTS", "").split(",")
    if args.event != "test" and args.event not in events:
        print("Telegram: this event is disabled; nothing was sent.")
        return 0
    if not re.fullmatch(r"-?[0-9]+", chat):
        parser.error("Set TELEGRAM_CHAT_ID to the numeric destination. Nothing was sent.")
    root = Path(__file__).resolve().parents[2]
    project = args.project or root.name
    project_id = None
    if args.event != "test":
        from kanban.project import load_project

        try:
            context = load_project(root)
            args.module = context.select_module(args.module)
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            parser.error(str(error))
        project = args.project or context.name
        if "\n" in project or "\r" in project:
            parser.error("The project display name must be a single line.")
        project_id = context.id
    if args.send_to is None:
        print(f"Preview: {args.event} notification to chat {chat}. Confirm with --send-to {chat}.")
        if args.event != "test":
            print(render(args, project))
        return 0
    if args.send_to != chat:
        parser.error("Confirmed destination does not match TELEGRAM_CHAT_ID.")
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    if not re.fullmatch(r"[0-9]+:[A-Za-z0-9_-]+", token):
        parser.error("Set TELEGRAM_BOT_TOKEN in the execution environment. Nothing was sent.")
    try:
        git_dir = subprocess.check_output(
            ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
            cwd=root, text=True,
        ).strip()
        outcome = notify(
            args, token, chat, Path(git_dir) / "telegram-notifications.sqlite3",
            project=project, project_id=project_id,
        )
    except (OSError, ValueError, sqlite3.Error, subprocess.CalledProcessError, SendFailed):
        # Network exceptions can contain the request URL and token.
        print("Telegram: delivery could not be confirmed. Check the token, chat access, and network.", file=sys.stderr)
        return 2
    message, code = STATUS[outcome]
    print(message, file=sys.stderr if code else sys.stdout)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
