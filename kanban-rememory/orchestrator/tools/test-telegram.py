"""Risky behavior of telegram.py, with fake credentials and no network: secret handling, setup, alerts."""

import argparse
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

KIT = Path(__file__).resolve().parents[3]
SCRIPT = KIT / "kanban-rememory/orchestrator/tools/telegram.py"
spec = importlib.util.spec_from_file_location("telegram", SCRIPT)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
TOKEN = "123456789:PRIVATE_TEST_TOKEN"
WEBHOOK = "https://hooks.slack.com/services/T123/B123/PRIVATE_TEST_WEBHOOK"
CONFIG = {"version": 1, "token": TOKEN, "chat_id": "42", "bot_username": "RememoryNotifyBot"}


def message(identifier=42, text="/setup_fixed", kind="private"):
    return {"message": {"text": text, "chat": {"id": identifier, "type": kind, "first_name": "Test"}}}


class TelegramTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name)
        self.path = self.base / "config/telegram.json"
        self.calls = []
        self.updates = [message()]

    def api(self, token, method, **values):
        self.assertEqual(token, TOKEN)
        self.calls.append(method)
        return {"getMe": {"is_bot": True, "username": "RememoryNotifyBot", "first_name": "Remy"},
                "getWebhookInfo": {"url": ""}, "getUpdates": self.updates, "sendMessage": {"message_id": 1}}[method]

    def wizard(self, answers, api=None):
        responses = iter(answers)
        output = io.StringIO()
        with contextlib.redirect_stdout(output), patch.object(m.secrets, "token_hex", return_value="fixed"):
            m.setup(self.path, ask=lambda _: next(responses), secret=lambda _: TOKEN, call=api or self.api)
        self.assertNotIn(TOKEN, output.getvalue())
        return output.getvalue()

    def test_setup_saves_a_private_config_only_after_a_confirmed_test(self):
        self.updates = [message(text="/start"), message(kind="group"), message()]
        self.wizard(["", "y", "y"])
        self.assertEqual(m.load_config(self.path), CONFIG)
        self.assertEqual(self.calls, ["getMe", "getWebhookInfo", "getUpdates", "sendMessage"])
        if sys.platform != "win32":
            self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)

    def test_setup_refusals_keep_the_previous_config(self):
        m.save_config(self.path, {**CONFIG, "chat_id": "99"})
        original = self.path.read_bytes()
        self.wizard(["n"])  # keep the existing configuration
        self.wizard(["y", "", "n"])  # recipient refused: no test sent
        self.wizard(["y", "", "y", "n"])  # receipt not confirmed
        self.assertEqual(self.calls.count("sendMessage"), 1)
        self.updates = [message(), message(43)]
        with self.assertRaisesRegex(m.TelegramError, "Multiple"):
            self.wizard(["y", ""])

        def webhook(token, method, **values):
            return {"url": "https://example.invalid/hook"} if method == "getWebhookInfo" else self.api(token, method)
        with self.assertRaisesRegex(m.TelegramError, "webhook was preserved"):
            self.wizard(["y"], webhook)
        self.assertEqual(self.path.read_bytes(), original)

    def test_saving_is_atomic_and_private_on_every_platform(self):
        m.save_config(self.path, CONFIG)
        original = self.path.read_bytes()
        for target, failure in ((m, "protect_file"), (m.os, "replace")):
            with self.subTest(failure=failure), patch.object(target, failure, side_effect=OSError("refused")):
                with self.assertRaises(OSError):
                    m.save_config(self.path, {**CONFIG, "chat_id": "99"})
            self.assertEqual(self.path.read_bytes(), original)
            self.assertEqual(list(self.path.parent.glob(".telegram-*")), [])
        calls = []

        def run(args, **kwargs):  # the ACL must be set while the file is still empty
            calls.append(args)
            if args[0] == "icacls":
                self.assertEqual(Path(args[1]).read_bytes(), b"")
            return subprocess.CompletedProcess(args, 0, stdout='"machine\\user","S-1-5-21-123-1001"\n')
        real = m.protect_file
        with patch.object(m.subprocess, "run", side_effect=run), patch.object(
                m, "protect_file", side_effect=lambda path: real(path, "win32")):
            m.save_config(self.path, CONFIG)
        self.assertEqual(calls[1][2:], ["/inheritance:r", "/grant:r", "*S-1-5-21-123-1001:F"])
        empty = self.base / "empty"
        empty.touch()
        with patch.object(m.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "whoami")):
            with self.assertRaisesRegex(m.TelegramError, "No token was saved"):
                m.protect_file(empty, "win32")

    @unittest.skipIf(sys.platform == "win32", "POSIX file modes")
    def test_unsafe_or_malformed_configs_are_refused_without_the_token(self):
        m.save_config(self.path, CONFIG)
        self.path.chmod(0o644)
        with self.assertRaisesRegex(m.TelegramError, "too broad"):
            m.load_config(self.path)
        link = self.path.with_name("link.json")
        link.symlink_to(self.path)
        with self.assertRaisesRegex(m.TelegramError, "symbolic"):
            m.load_config(link)
        for content in (TOKEN, json.dumps({**CONFIG, "chat_id": 42}), json.dumps({**CONFIG, "token": None})):
            self.path.write_text(content)
            self.path.chmod(0o600)
            with self.assertRaises(m.TelegramError) as error:
                m.load_config(self.path)
            self.assertNotIn(TOKEN, str(error.exception))

    def test_api_errors_are_actionable_and_never_show_the_token(self):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        for code, expected, definite in ((401, "Token rejected", True), (409, "another reader", True),
                                         (429, "rate limiting", True), (500, "uncertain", False)):
            with self.subTest(code=code), patch.object(m, "urlopen", side_effect=HTTPError(url, code, TOKEN, {}, None)):
                with self.assertRaises(m.TelegramError) as error:
                    m.api(TOKEN, "sendMessage", chat_id="42")
                self.assertIn(expected, str(error.exception))
                self.assertEqual(error.exception.definite, definite)
                self.assertNotIn(TOKEN, str(error.exception))
        for failure, definite in ((URLError(TOKEN), False), (TimeoutError(TOKEN), False)):
            with patch.object(m, "urlopen", side_effect=failure), self.assertRaises(m.TelegramError) as error:
                m.api(TOKEN, "sendMessage")
            self.assertEqual(error.exception.definite, definite)
            self.assertNotIn(TOKEN, str(error.exception))
        with patch.object(m, "urlopen", return_value=io.BytesIO(b'{"ok":false}')), self.assertRaises(m.TelegramError):
            m.api(TOKEN, "sendMessage")
        with patch.object(m, "urlopen", return_value=io.BytesIO(b'{"ok":true,"result":{"id":7}}')) as opened:
            self.assertEqual(m.api(TOKEN, "getUpdates", limit=100), {"id": 7})
        self.assertEqual(json.loads(opened.call_args.args[0].data), {"limit": 100})

    def test_alerts_are_sent_once_and_uncertain_sends_wait_for_confirmation(self):
        text = m.render("attention", "en", "Demo", "a", "CARD-00000135", "Choose the file format.",
                        "Return to the chat and choose the format.", "Claude Code · Export",
                        "https://example.invalid/chat/1")
        self.assertEqual(text, "🔔 Action required\n\nProject: Demo\nReference: a / CARD-00000135\n"
                               "Summary: Choose the file format.\n\nNext action: Return to the chat and choose the "
                               "format. — Claude Code · Export\nhttps://example.invalid/chat/1")
        self.assertTrue(m.render("completed", "fr", "Demo", "a", "CARD-1", "Fait.", "Aucune action requise.",
                                 "Codex").startswith("✅ Travail terminé\n\nProjet: Demo\nRéférence: a / CARD-1"))
        ledger, sent = self.base / "ledger.sqlite3", []

        def failing(definite):
            def send():
                raise m.TelegramError("failed", definite)
            return send
        good = lambda: sent.append(1)
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r1"), good), "sent")
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r1"), good), "duplicate")
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r2"), failing(True)), "failed")
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r2"), good), "sent")  # a refusal is retryable
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r3"), failing(False)), "unconfirmed")
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r3"), good), "unconfirmed")
        self.assertEqual(m.deliver(ledger, ("42", "Demo", "attention", "r3"), good, confirm_retry=True), "sent")
        self.assertEqual(len(sent), 3)

    def test_alert_command_previews_the_card_and_refuses_bad_input(self):
        root = self.base / "repo"
        shutil.copytree(KIT / "kanban-rememory/orchestrator/tools", root / "kanban-rememory/orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__", "test-*.py"))
        card = root / "project/modules/a/backlog/card-00000001-export.md"
        card.parent.mkdir(parents=True)
        card.write_text('---\nid: "CARD-00000001"\nmodule: "a"\n---\n')
        settings = json.loads((KIT / "kanban-rememory.json").read_text())
        (root / "kanban-rememory.json").write_text(json.dumps(dict(settings, name="Example", modules=["a", "misc"])))
        environment = {**os.environ, "HOME": str(self.base / "home"), "LOCALAPPDATA": str(self.base / "home")}

        def run(*args):
            return subprocess.run([sys.executable, "kanban-rememory/orchestrator/tools/telegram.py", *args], cwd=root,
                                  env=environment, capture_output=True, text=True)
        full = ("completed", "--card", "card-00000001", "--id", "delivery", "--text", "Export vérifié.",
                "--next-action", "Aucune action requise.", "--chat-name", "Codex · Export", "--language", "fr")
        preview = run(*full)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertIn("Projet: Example\nRéférence: a / CARD-00000001\n", preview.stdout)
        unconfigured = run(*full, "--send")
        self.assertEqual(unconfigured.returncode, 1)
        self.assertIn("nothing was sent", unconfigured.stderr)
        for bad in ((*full[:2], "CARD-1", *full[3:]), (*full, "--link", "not a link"),
                    (*full[:6], " ", *full[7:]), (*full, "--language", "es")):
            self.assertNotEqual(run(*bad).returncode, 0)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        m.save_config(self.path, CONFIG)
        args = argparse.Namespace(command="completed", card="CARD-00000001", id="delivery", text="Export vérifié.",
                                  next_action="Aucune action requise.", chat_name="Codex · Export", link=None,
                                  language="fr", send=True, confirm_retry=False)
        sent = []
        with patch.object(m, "ROOT", root), contextlib.redirect_stdout(io.StringIO()):
            for _ in range(2):  # the second call is a duplicate
                self.assertEqual(m.alert(args, self.path, call=lambda token, method, **values: sent.append(values)), 0)
        self.assertEqual(len(sent), 1)
        self.assertEqual(sent[0]["chat_id"], "42")
        self.assertIn("Référence: a / CARD-00000001\n", sent[0]["text"])
        slack_path = self.path.with_name("slack.json")
        m.save_config(slack_path, {"version": 1, "webhook": WEBHOOK}, m.check_slack_config)
        with patch.object(m, "ROOT", root), patch.object(m, "send_slack") as send_slack, \
                contextlib.redirect_stdout(io.StringIO()):
            for command in ("attention", "completed"):
                args.command = command
                for _ in range(2):
                    self.assertEqual(m.alert(args, self.path, call=self.api), 0)
            self.assertEqual(send_slack.call_count, 2)
            self.assertEqual(send_slack.call_args.args[0], WEBHOOK)
            self.assertIn("Référence: a / CARD-00000001\n", send_slack.call_args.args[1])
            self.assertEqual(self.calls, [])
        piped = subprocess.run([sys.executable, str(SCRIPT)], input=b"", capture_output=True)
        self.assertEqual(piped.returncode, 1)
        self.assertIn(b"interactive terminal", piped.stderr)

    def test_slack_uses_a_private_webhook_and_handles_uncertain_delivery(self):
        slack_path = self.path.with_name("slack.json")
        output = io.StringIO()
        with patch.object(m.getpass, "getpass", return_value=WEBHOOK), contextlib.redirect_stdout(output):
            self.assertEqual(m.setup_slack(slack_path), 0)
        self.assertNotIn(WEBHOOK, output.getvalue())
        if sys.platform != "win32":
            self.assertEqual(slack_path.stat().st_mode & 0o777, 0o600)
        self.assertEqual(m.active_config(self.path), ("Slack", slack_path))
        with patch.object(m, "build_opener") as opener:
            request = opener.return_value.open
            response = request.return_value.__enter__.return_value
            response.status = 200
            response.read.return_value = b"ok"
            m.send_slack(WEBHOOK, "Remy <@example>")
            payload = json.loads(request.call_args.args[0].data)
            self.assertEqual(payload["text"], "Remy &lt;@example&gt;")
            for status in (302, 403, 408, 500):
                with self.subTest(status=status):
                    request.side_effect = HTTPError(WEBHOOK, status, WEBHOOK, {}, None)
                    with self.assertRaises(m.TelegramError) as failure:
                        m.send_slack(WEBHOOK, "Remy")
                    self.assertEqual(failure.exception.definite, status in (302, 403))
                    self.assertNotIn(WEBHOOK, str(failure.exception))

    @unittest.skipIf(sys.platform == "win32", "real POSIX terminal; Windows needs live acceptance")
    def test_real_terminal_hides_the_token(self):
        import pty
        import select
        import time
        harness = self.base / "interactive.py"
        harness.write_text(
            "import importlib.util\nfrom pathlib import Path\n"
            f"s = importlib.util.spec_from_file_location('m', {str(SCRIPT)!r})\n"
            "m = importlib.util.module_from_spec(s); s.loader.exec_module(m)\n"
            f"m.config_path = lambda: Path({str(self.path)!r})\n"
            "m.secrets.token_hex = lambda n: 'fixed'\n"
            "replies = {'getMe': {'is_bot': True, 'username': 'RememoryNotifyBot'}, 'getWebhookInfo': {'url': ''},\n"
            f"           'getUpdates': [{message()!r}], 'sendMessage': {{'message_id': 1}}}}\n"
            "wizard = m.setup\nm.setup = lambda path: wizard(path, call=lambda token, method, **k: replies[method])\n"
            "raise SystemExit(m.main())\n")
        pid, fd = pty.fork()
        if pid == 0:
            os.execl(sys.executable, sys.executable, str(harness))
        data = b""

        def until(marker):
            nonlocal data
            deadline = time.monotonic() + 10
            while marker.encode() not in data:
                if time.monotonic() >= deadline:
                    self.fail(f"Terminal did not reach: {marker}")
                if select.select([fd], [], [], 0.2)[0]:
                    data += os.read(fd, 4096)
        try:
            for marker, answer in (("hidden input", TOKEN), ("Press Enter after sending", ""),
                                   ("Allow notifications", "y"), ("Did you receive", "y")):
                until(marker)
                os.write(fd, (answer + "\n").encode())
            until("Configuration saved")
            _, status = os.waitpid(pid, 0)
            self.assertEqual(os.waitstatus_to_exitcode(status), 0)
            self.assertNotIn(TOKEN.encode(), data)
            self.assertEqual(m.load_config(self.path)["chat_id"], "42")
        finally:
            os.close(fd)


if __name__ == "__main__":
    unittest.main()
