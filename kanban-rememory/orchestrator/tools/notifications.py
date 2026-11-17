"""Remy sends optional Slack or Telegram alerts for Kanban Rememory."""

import argparse
import csv
import getpass
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import socket
import sqlite3
import subprocess
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen
import warnings

ROOT = Path(__file__).resolve().parents[3]
TOKEN = re.compile(r"[0-9]+:[A-Za-z0-9_-]+")
SLACK_WEBHOOK = re.compile(r"https://hooks\.slack\.com/services/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+/[A-Za-z0-9_-]+")
TEST = "Remy: Kanban Rememory setup test."
UNCERTAIN = "Delivery uncertain. Check Telegram before sending again."
OFFLINE = "Connection failed. Check your network and try again."
HTTP = {
    401: "Token rejected. Copy the API token from BotFather.",
    403: "Access denied. Unblock the bot in Telegram and send it /start.",
    409: "A webhook or another reader is using this bot. Remote settings were preserved.",
    429: "Telegram is rate limiting requests. Wait before trying again.",
}
ICONS = {"attention": "🔔", "completed": "✅"}
LABELS = {
    "en": {"attention": "Action required", "completed": "Work completed", "project": "Project",
           "reference": "Reference", "summary": "Summary", "next_action": "Next action"},
    "fr": {"attention": "Action requise", "completed": "Travail terminé", "project": "Projet",
           "reference": "Référence", "summary": "Résumé", "next_action": "Prochaine action"},
}
STATUS = {
    "sent": ("confirmed delivery.", 0),
    "duplicate": ("already confirmed; not sent again.", 0),
    "unconfirmed": ("delivery not confirmed and the outcome is unknown. Check the destination, then rerun "
                    "with --confirm-retry to send again.", 2),
    "failed": ("not sent, the request was refused. Retrying is safe.", 1),
}


class TelegramError(Exception):
    """A failed request; definite is false when the message may still have been delivered."""

    def __init__(self, message, definite=True):
        super().__init__(message)
        self.definite = definite


def config_path(platform=None, environ=None, home=None):
    platform = platform or sys.platform
    environ = os.environ if environ is None else environ
    home = Path.home() if home is None else Path(home)
    if platform == "win32":
        return Path(environ.get("LOCALAPPDATA") or home / "AppData" / "Local") / "KanbanRememory" / "telegram.json"
    return home / ".config" / "kanban-rememory" / "telegram.json"


def active_config(telegram_path=None):
    telegram_path = config_path() if telegram_path is None else telegram_path
    slack_path = telegram_path.with_name("slack.json")
    if slack_path.exists() or slack_path.is_symlink():
        return "Slack", slack_path
    return "Telegram", telegram_path


class NoWebhookRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def send_slack(webhook, message):
    escaped = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    payload = {"text": escaped, "mrkdwn": False, "unfurl_links": False, "unfurl_media": False}
    request = Request(webhook, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    uncertain = "Slack did not confirm delivery. Check the Slack channel before sending again."
    try:
        with build_opener(NoWebhookRedirect()).open(request, timeout=20) as response:
            if response.status == 200 and response.read(16).strip() == b"ok":
                return
    except HTTPError as error:
        if error.code == 408 or error.code >= 500:
            raise TelegramError(uncertain, definite=False) from None
        raise TelegramError(f"Slack refused the request (HTTP {error.code}).") from None
    except URLError as error:
        if isinstance(error.reason, (socket.gaierror, ConnectionRefusedError)):
            raise TelegramError(OFFLINE) from None
        raise TelegramError(uncertain, definite=False) from None
    except (OSError, ValueError):
        raise TelegramError(uncertain, definite=False) from None
    raise TelegramError(uncertain, definite=False)


def api(token, method, **parameters):
    request = Request(f"https://api.telegram.org/bot{token}/{method}", data=json.dumps(parameters).encode(),
                      headers={"Content-Type": "application/json"})
    sending = method == "sendMessage"
    # Network exceptions can contain the request URL, hence the token: raise only our own messages.
    try:
        with urlopen(request, timeout=20) as response:
            result = json.load(response)
    except HTTPError as error:
        if sending and error.code >= 500:
            raise TelegramError(UNCERTAIN, definite=False) from None
        raise TelegramError(HTTP.get(error.code, f"Telegram rejected the request (HTTP {error.code}).")) from None
    except URLError as error:
        if sending and not isinstance(error.reason, (socket.gaierror, ConnectionRefusedError)):
            raise TelegramError(UNCERTAIN, definite=False) from None
        raise TelegramError(OFFLINE) from None
    except (OSError, ValueError):  # timeout or unreadable reply: a message may have been delivered
        raise TelegramError(UNCERTAIN if sending else OFFLINE, definite=not sending) from None
    if not isinstance(result, dict) or result.get("ok") is not True or "result" not in result:
        raise TelegramError("Telegram did not confirm the request.")
    return result["result"]


def check_config(config):
    if (not isinstance(config, dict) or config.get("version") != 1
            or not isinstance(config.get("token"), str) or not TOKEN.fullmatch(config["token"])
            or not isinstance(config.get("chat_id"), str) or not re.fullmatch(r"[0-9]+", config["chat_id"])):
        raise TelegramError("Invalid configuration. Run the setup again to replace it.")
    return config


def check_slack_config(config):
    if (not isinstance(config, dict) or config.get("version") != 1
            or not isinstance(config.get("webhook"), str) or not SLACK_WEBHOOK.fullmatch(config["webhook"])):
        raise TelegramError("Invalid Slack webhook. Use the Incoming Webhooks URL from your Slack app.")
    return config


def load_config(path, check=check_config):
    try:
        if path.is_symlink():
            raise TelegramError("The configuration file must not be a symbolic link.")
        if sys.platform != "win32" and path.stat().st_mode & 0o077:
            raise TelegramError("Configuration file permissions are too broad. Restore them with chmod 600.")
        return check(json.loads(path.read_text(encoding="utf-8")))
    except FileNotFoundError:
        if check is check_slack_config:
            raise TelegramError("Slack is not configured; nothing was sent. Run setup-slack.") from None
        raise TelegramError("Telegram is not configured; nothing was sent. "
                            "Set it up with: python3 kanban-rememory/orchestrator/tools/notifications.py") from None
    except (OSError, ValueError):
        raise TelegramError("Could not read the configuration. Run the setup again.") from None


def protect_file(path, platform=None):
    """Restrict an EMPTY new file to the current user before any credential is written."""
    if (platform or sys.platform) != "win32":
        path.chmod(0o600)
        return
    try:
        result = subprocess.run(["whoami", "/user", "/fo", "csv", "/nh"], check=True, capture_output=True, text=True)
        sid = next(csv.reader(io.StringIO(result.stdout)))[1]
        if not re.fullmatch(r"S-1-[0-9-]+", sid):
            raise ValueError("Invalid SID")
        subprocess.run(["icacls", str(path), "/inheritance:r", "/grant:r", f"*{sid}:F"],
                       check=True, capture_output=True, text=True)
    except (OSError, ValueError, IndexError, StopIteration, subprocess.CalledProcessError):
        raise TelegramError("Could not secure the Windows file. No token was saved.") from None


def save_config(path, config, check=check_config):
    check(config)
    if path.is_symlink():
        raise TelegramError("Cannot replace a configuration file that is a symbolic link.")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.stem}-", dir=path.parent)
    os.close(descriptor)
    temporary = Path(temporary)
    try:
        protect_file(temporary)
        with temporary.open("w", encoding="utf-8") as stream:
            json.dump(config, stream)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def yes(prompt, ask):
    return ask(prompt + " [y/N] ").strip().lower() in ("o", "oui", "y", "yes")


def setup_slack(path):
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        webhook = getpass.getpass("Slack Incoming Webhook URL (hidden input): ").strip()
    save_config(path, {"version": 1, "webhook": webhook}, check_slack_config)
    print("Slack configuration saved. Run test --send to verify that the alert reaches the channel.")
    return 0


def private_matches(updates, challenge):
    if not isinstance(updates, list):
        raise TelegramError("Invalid Telegram update list. No settings were saved.")
    chats = {}
    for update in updates:
        message = update.get("message", {})
        chat = message.get("chat", {})
        if (message.get("text", "").strip() == challenge and chat.get("type") == "private"
                and isinstance(chat.get("id"), int) and chat["id"] > 0):
            chats[str(chat["id"])] = chat
    return chats


def setup(path, ask=input, secret=getpass.getpass, call=api):
    print("Telegram setup for macOS and Windows. Press Ctrl+C to cancel and keep your existing configuration.")
    if path.exists() and not yes("Replace the existing configuration after a successful test?", ask):
        print("Canceled. Existing configuration kept.")
        return 0
    with warnings.catch_warnings():  # never fall back to echoed input in a redirected terminal
        warnings.simplefilter("error", getpass.GetPassWarning)
        token = secret("Bot API token (hidden input): ").strip()
    if not TOKEN.fullmatch(token):
        raise TelegramError("Invalid token format. Enter the API token from BotFather.")
    bot = call(token, "getMe")
    if not isinstance(bot, dict) or not bot.get("is_bot") or not re.fullmatch(r"[A-Za-z0-9_]+", bot.get("username", "")):
        raise TelegramError("Could not identify the bot. No settings were saved.")
    print(f"Verified bot: {bot.get('first_name', '')} — @{bot['username']}")
    webhook = call(token, "getWebhookInfo")
    if not isinstance(webhook, dict):
        raise TelegramError("Invalid Telegram response. No settings were saved.")
    if webhook.get("url"):
        raise TelegramError("This bot uses a webhook. Use a dedicated notification bot. The webhook was preserved.")
    challenge = "/setup_" + secrets.token_hex(4)
    print(f"1. Open https://t.me/{bot['username']} and press Start if needed.")
    print(f"2. Send this exact message to the bot: {challenge}")
    print("The bot does not reply automatically. Return to this terminal after sending the code.")
    while True:
        ask("3. Press Enter after sending the code to find your chat: ")
        updates = call(token, "getUpdates", timeout=5, limit=100)
        chats = private_matches(updates, challenge)
        if len(chats) > 1:
            raise TelegramError("Multiple chats sent this code. Run the setup again to get a new code.")
        if chats:
            chat_id, chat = next(iter(chats.items()))
            break
        print("Code not found. Check the bot link and the text you sent. No chat ID lookup is needed.")
        if len(updates) >= 100:
            raise TelegramError("This bot has too many pending messages. Use a dedicated bot. No messages were deleted.")
        if not yes("Try again after sending the code in this chat?", ask):
            print("Canceled. Previous configuration kept.")
            return 0
    name = " ".join(str(chat.get(key, "")) for key in ("first_name", "last_name")).strip()
    print(f"Recipient found: {name} (chat ID {chat_id}).")
    if not yes("Allow notifications to this recipient and send a test?", ask):
        print("Canceled. No message was sent. Previous configuration kept.")
        return 0
    call(token, "sendMessage", chat_id=chat_id, text=TEST)
    print("Telegram confirmed that the test was sent.")
    if not yes("Did you receive the message in this Telegram chat?", ask):
        print("Receipt was not confirmed. Previous configuration kept. Check Telegram before trying again.")
        return 0
    save_config(path, {"version": 1, "token": token, "chat_id": chat_id, "bot_username": bot["username"]})
    print(f"Configuration saved: {path}")
    print("Ready. Agents send alerts with notifications.py attention or completed.")
    return 0


def render(event, language, project, module, card, text, next_action, chat_name, link=None):
    labels = LABELS[language]
    action = f"{next_action} — {chat_name}" + (f"\n{link}" if link else "")
    return (f"{ICONS[event]} {labels[event]}\n\n{labels['project']}: {project}\n"
            f"{labels['reference']}: {module} / {card}\n{labels['summary']}: {text}\n\n"
            f"{labels['next_action']}: {action}")


def deliver(ledger, key, send, confirm_retry=False):
    """Send once per key. Return sent, duplicate, unconfirmed (resend blocked) or failed."""
    with sqlite3.connect(ledger, timeout=20) as connection:
        connection.execute("CREATE TABLE IF NOT EXISTS alerts (chat TEXT, project TEXT, kind TEXT, ident TEXT, "
                           "state TEXT, PRIMARY KEY (chat, project, kind, ident))")
        connection.execute("BEGIN IMMEDIATE")
        row = connection.execute("SELECT state FROM alerts WHERE (chat,project,kind,ident) = (?,?,?,?)", key).fetchone()
        if row and row[0] == "sent":
            return "duplicate"
        if row and not confirm_retry:
            return "unconfirmed"
        # Record the attempt first: an interrupted send must never count as not attempted.
        connection.execute("INSERT OR REPLACE INTO alerts VALUES (?,?,?,?,'unconfirmed')", key)
        connection.commit()
        connection.execute("BEGIN IMMEDIATE")
        try:
            send()
        except TelegramError as failure:
            if failure.definite:
                connection.execute("DELETE FROM alerts WHERE (chat,project,kind,ident) = (?,?,?,?)", key)
                connection.commit()
                return "failed"
            connection.commit()
            return "unconfirmed"
        connection.execute("UPDATE alerts SET state='sent' WHERE (chat,project,kind,ident) = (?,?,?,?)", key)
        return "sent"


def alert(args, path, call=api):
    sys.path.insert(0, str(ROOT / "kanban-rememory/orchestrator/tools"))
    from kanban.board import find_card
    from kanban.project import common_directory, load_project

    project = load_project(ROOT)
    module = find_card(project, args.card)[0]
    message = render(args.command, args.language, project.name, module, args.card, args.text,
                     args.next_action, args.chat_name, args.link)
    if not args.send:
        print(f"Preview, not sent (add --send):\n\n{message}")
        return 0
    service, target = active_config(path)
    if service == "Slack":
        webhook = load_config(target, check_slack_config)["webhook"]
        recipient = hashlib.sha256(webhook.encode()).hexdigest()
        send = lambda: send_slack(webhook, message)
    else:
        config = load_config(target)
        recipient = config["chat_id"]
        send = lambda: call(config["token"], "sendMessage", chat_id=recipient, text=message)
    key = (recipient, project.name, args.command, json.dumps([module, args.card, args.id], ensure_ascii=False))
    try:
        outcome = deliver(common_directory(ROOT) / f"{service.lower()}-notifications.sqlite3", key, send,
                          args.confirm_retry)
    except (OSError, sqlite3.Error):
        print(f"{service}: delivery could not be confirmed. Check the destination before any retry.", file=sys.stderr)
        return 2
    text, code = STATUS[outcome]
    print(f"{service}: {text}", file=sys.stderr if code else sys.stdout)
    return code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("setup", help="interactive private setup (default)")
    sub.add_parser("setup-slack", help="privately configure a Slack incoming webhook")
    sub.add_parser("status", help="show the active service without revealing credentials")
    test = sub.add_parser("test", help="preview or send a test message")
    test.add_argument("--send", action="store_true")
    for event, purpose in (("attention", "a decision, an action or a merge approval is needed"),
                           ("completed", "the agreed delivery is verified")):
        work = sub.add_parser(event, help=purpose)
        work.add_argument("--card", required=True, type=str.upper, help="Card ID")
        work.add_argument("--id", required=True, help="stable event ID: intervention-N, merge-REVISION or delivery")
        work.add_argument("--text", required=True, help="at most two sentences")
        work.add_argument("--next-action", required=True, help="a verb and where to act, or no action required")
        work.add_argument("--chat-name", required=True, help="the chat to return to, with its application")
        work.add_argument("--link", help="direct link to the chat, only when the environment provides one")
        work.add_argument("--language", choices=LABELS, default="en")
        work.add_argument("--send", action="store_true", help="send; without it, only preview")
        work.add_argument("--confirm-retry", action="store_true",
                          help="send again once it is known that an unconfirmed alert did not arrive")
    args = parser.parse_args()
    if args.command in ICONS:
        if not re.fullmatch(r"CARD-[0-9]{8}", args.card):
            parser.error("--card takes a Card ID such as CARD-00000001.")
        if not re.fullmatch(r"[A-Za-z0-9@:._-]{1,80}", args.id):
            parser.error("--id takes up to 80 letters, digits and @:._- characters.")
        for name in ("text", "next_action", "chat_name"):
            value = getattr(args, name)
            if not value.strip() or "\n" in value or "\r" in value:
                parser.error(f"--{name.replace('_', '-')} must be a nonempty single line.")
        if args.link and not re.fullmatch(r"[a-z][a-z0-9+.-]*://\S+", args.link, re.IGNORECASE):
            parser.error("--link must be a full address such as https://example.invalid/chat.")
    path = config_path()
    try:
        if args.command in (None, "setup", "setup-slack"):
            if not sys.stdin.isatty():
                raise TelegramError("Run this file in an interactive terminal: python3 kanban-rememory/orchestrator/tools/notifications.py "
                                    "on macOS, py -3 kanban-rememory/orchestrator/tools/notifications.py on Windows. "
                                    "Piped input and python - are unsupported.")
            if args.command == "setup-slack":
                return setup_slack(path.with_name("slack.json"))
            return setup(path)
        if args.command in ICONS:
            return alert(args, path)
        service, target = active_config(path)
        if service == "Slack":
            config = load_config(target, check_slack_config)
            print(f"Configuration: Slack, file {target}")
            if args.command == "test" and args.send:
                send_slack(config["webhook"], TEST)
                print("Slack confirmed the send. Check the configured channel for the test.")
            elif args.command == "test":
                print("Preview only. Add --send to send the test.")
            return 0
        config = load_config(target)
        print(f"Configuration: @{config.get('bot_username', '?')}, recipient {config['chat_id']}, file {path}")
        if args.command == "test":
            if not args.send:
                print("Preview only. Add --send to send the test.")
                return 0
            api(config["token"], "sendMessage", chat_id=config["chat_id"], text=TEST)
            print("Telegram confirmed the send. Check your Telegram chat for the test.")
        return 0
    except (KeyboardInterrupt, EOFError):
        print("\nInput interrupted. Previous configuration kept.", file=sys.stderr)
    except getpass.GetPassWarning:
        print("Hidden input unavailable. Open a regular terminal and try again.", file=sys.stderr)
    except (TelegramError, ValueError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
    except OSError:
        print("Local file or permission error. Use status to check the saved configuration.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
