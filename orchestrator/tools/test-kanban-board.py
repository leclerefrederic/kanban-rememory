"""Verify the module Kanbans, kit documentation and work alerts with local Git only."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


KIT = Path(__file__).resolve().parents[2]
MODULES = ("a", "b", "misc")


class KanbanBoardTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        shutil.copytree(KIT / "orchestrator/tools", self.root / "orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__", "test-*.py"))
        shutil.copytree(KIT / "orchestrator/templates", self.root / "orchestrator/templates")
        settings = json.loads((KIT / "project/settings.json").read_text())
        settings.update(project={"id": "fixture", "name": "Fixture"}, last_card_id=0,
                        modules={name: {"workspace": f"project/modules/{name}"} for name in MODULES})
        self.settings = self.root / "project/settings.json"
        self.settings.parent.mkdir()
        self.settings.write_text(json.dumps(settings))
        for name in MODULES:
            for stage in (*settings["workflow"]["stages"], "resources"):
                (self.board(name) / stage).mkdir(parents=True)
        self.journal = self.root / "project/rememory"
        self.journal.mkdir()
        self.git("init", "-q", "-b", "main")

    def board(self, module):
        return self.root / "project/modules" / module

    def git(self, *args, cwd=None):
        return subprocess.check_output(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", *args],
            cwd=cwd or self.root, text=True,
        ).strip()

    def run_board(self, *args, expected=0, cwd=None):
        result = subprocess.run(
            [sys.executable, "orchestrator/tools/manage-kanban-board.py", *args],
            cwd=cwd or self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def new(self, title, module="a"):
        self.run_board("new", title, "--owner", "Orchestrator", "--scope", module, "--apply")
        return next((self.board(module) / "backlog").glob(f"*-{title.lower().replace(' ', '-')}.md"))

    def test_new_previews_then_allocates_project_wide_ids(self):
        preview = self.run_board("new", "First", "--owner", "Orchestrator", "--scope", "a")
        self.assertIn('module: "a"', preview)
        self.assertFalse(list((self.board("a") / "backlog").glob("*.md")))
        first = self.new("First")
        self.assertEqual(first.name, "card-00000001-first.md")
        source = first.read_text()
        self.assertIn('id: "CARD-00000001"\nmodule: "a"\n', source)
        self.assertIn("# CARD-00000001 — First\n", source)
        self.assertIn("- Owner: Orchestrator\n", source)
        self.run_board("new", "Default", "--owner", "Orchestrator", "--apply")
        self.assertTrue((self.board("misc") / "backlog/card-00000002-default.md").is_file())
        settings = json.loads(self.settings.read_text())
        settings["last_card_id"] = 40
        self.settings.write_text(json.dumps(settings))
        self.assertTrue(self.new("Later", "b").name.startswith("card-00000041-"))
        shutil.copy(first, self.board("b") / "backlog" / first.name)
        self.assertIn("Duplicate CARD-00000001", self.run_board(
            "new", "Collision", "--owner", "Orchestrator", "--apply", expected=1))
        self.assertIn("Unknown module", self.run_board(
            "new", "Elsewhere", "--owner", "Orchestrator", "--scope", "@project", expected=1))
        self.assertIn("nonempty single line", self.run_board(
            "new", " ", "--owner", "Orchestrator", expected=1))

    def test_moves_follow_transitions_and_ownership(self):
        card = self.new("Example")
        self.assertIn("not allowed", self.run_board("move", "CARD-00000001", "completion", expected=1))
        self.assertIn("--owner-token", self.run_board("move", "CARD-00000001", "development", expected=1))
        self.git("commit", "-q", "--allow-empty", "-m", "Initial")
        self.assertIn("No matching ownership", self.run_board(
            "move", "CARD-00000001", "development", "--owner-token", "nobody", expected=1))
        self.assertIn("belongs to module a", self.run_board(
            "move", "CARD-00000001", "cancellation", "--scope", "b", expected=1))
        self.run_board("move", "CARD-00000001", "cancellation")
        moved = self.board("a") / "cancellation" / card.name
        self.assertIn("Stage moved from `backlog` to `cancellation`.", moved.read_text())
        self.assertIn("not allowed", self.run_board("move", "CARD-00000001", "backlog", expected=1))

    def test_move_rewrites_links_and_protects_other_records(self):
        card = self.new("Example")
        sibling = self.new("Sibling")
        entry = self.journal / "2026-01-01.md"
        entry.write_text(f"[Card](../modules/a/backlog/{card.name}#acceptance-criteria)\n"
                         f"`[Code](../modules/a/backlog/{card.name})`\n")
        with card.open("a") as stream:
            stream.write(f"\n[Sibling]({sibling.name})\n")
        guide = self.root / "documentation/guide.md"
        guide.parent.mkdir()
        guide.write_text(f"[Card](../project/modules/a/backlog/{card.name})\n")
        self.assertIn("protected record", self.run_board("move", "CARD-00000001", "cancellation", expected=1))
        self.assertTrue(card.is_file())
        guide.unlink()
        self.run_board("move", "CARD-00000001", "cancellation")
        moved = self.board("a") / "cancellation" / card.name
        self.assertIn(f"(../modules/a/cancellation/{card.name}#acceptance-criteria)", entry.read_text())
        self.assertIn(f"`[Code](../modules/a/backlog/{card.name})`", entry.read_text())
        self.assertIn(f"[Sibling](../backlog/{sibling.name})", moved.read_text())
        self.run_board("validate")

    def test_validate_reports_board_and_link_problems(self):
        card = self.new("Example")
        self.run_board("validate")
        (self.board("a") / "backlog/notes.md").write_text("x\n")
        card.write_text(card.read_text().replace('module: "a"', 'module: "b"', 1)
                        + "\n[Missing](missing.md)\n[Anchor](#nowhere)\n")
        misc = self.new("Shared", "misc")
        misc.write_text(misc.read_text().replace('module: "misc"', 'module: "misc"\naffected_modules: ["misc"]', 1))
        done = self.board("b") / "completion/card-00000009-done.md"
        done.write_text('---\ntype: card\nid: "CARD-00000009"\nmodule: "b"\n---\n\n## Acceptance criteria\n\n- [ ] Open.\n')
        (self.board("b") / "backlog/card-00000010-bare.md").write_text("# CARD-00000010\n")
        output = self.run_board("validate", expected=1)
        for expected in ("notes.md: expected a card ID", "Card belongs on the b board", "missing link target missing.md",
                         "missing heading anchor #nowhere", "affected_modules must list real modules",
                         "unchecked acceptance criterion", "Expected one module field"):
            self.assertIn(expected, output)
        (self.board("a") / "backlog/notes.md").unlink()
        os.symlink(self.root, self.board("a") / "resources/link")
        self.assertIn("symbolic link", self.run_board("validate", expected=1))

    def test_attachments_must_live_under_the_card_resources(self):
        card = self.new("Example")
        resources = self.board("a") / "resources"
        (resources / "card-00000001").mkdir()
        (resources / "card-00000001/spec.png").write_text("image")
        (resources / "other.png").write_text("image")
        card.write_text(card.read_text().replace(
            "## Resources\n", "## Resources\n\n- [Spec](../resources/card-00000001/spec.png): mockup.\n", 1))
        self.run_board("validate")
        card.write_text(card.read_text().replace("card-00000001/spec.png", "other.png", 1))
        self.assertIn("invalid Card attachment", self.run_board("validate", expected=1))

    def test_show_and_path_filter_by_module(self):
        self.new("Alpha")
        shared = self.new("Shared", "misc")
        shared.write_text(shared.read_text().replace('module: "misc"', 'module: "misc"\naffected_modules: ["b"]', 1))
        board = self.run_board("show")
        self.assertIn("CARD-00000001 | a | Alpha |", board)
        self.assertIn("a WIP: 0/1 | Available slots: 1", board)
        scoped = self.run_board("show", "--scope", "b")
        self.assertIn("CARD-00000002 | linked from misc |", scoped)
        self.assertNotIn("Alpha", scoped)
        self.assertEqual(self.run_board("path", "card-00000001").strip(),
                         "project/modules/a/backlog/card-00000001-alpha.md")
        self.assertIn("does not belong to b", self.run_board("path", "CARD-00000001", "--scope", "b", expected=1))
        self.assertIn("must be positive", self.run_board("show", "--wip-limit", "0", expected=2))

    def test_worktree_commands_use_the_primary_records(self):
        self.git("add", ".")
        self.git("commit", "-qm", "Initialize")
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        worktree = Path(scratch.name) / "candidate"
        self.git("worktree", "add", "-qb", "candidate", str(worktree))
        self.run_board("new", "From branch", "--owner", "Orchestrator", "--scope", "a", "--apply", cwd=worktree)
        name = "project/modules/a/backlog/card-00000001-from-branch.md"
        self.assertTrue((self.root / name).is_file())
        self.assertFalse((worktree / name).exists())
        self.assertIn("From branch", self.run_board("show", "--scope", "a", cwd=worktree))

    def test_kit_documentation_names_existing_tools_and_links(self):
        documents = [path for path in (*KIT.glob("*.md"), *KIT.glob("documentation/**/*.md"),
                                       *KIT.glob("orchestrator/**/*.md"))]
        tools = {match for path in documents
                 for match in re.findall(r"orchestrator/tools/[\w./-]+\.py", path.read_text(encoding="utf-8"))}
        self.assertTrue(tools)
        for tool in tools:
            self.assertTrue((KIT / tool).is_file(), tool)
        result = subprocess.run([sys.executable, str(KIT / "orchestrator/tools/manage-kanban-board.py"), "validate"],
                                cwd=KIT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def load_notifier(self):
        spec = importlib.util.spec_from_file_location("notify_telegram", KIT / "orchestrator/tools/notify-telegram.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def alert(self, notifier, ledger, sender, event="attention", confirm_retry=False, project="demo", **fields):
        values = dict(event=event, task=None, id=None, text=None, label=None, chat_name=None, link=None,
                      confirm_retry=confirm_retry, language="en", module="a", reference="CARD-00000135",
                      next_action="Return to the chat and choose the format.")
        values.update(fields)
        return notifier.notify(argparse.Namespace(**values), "token", "42", ledger, sender=sender, project=project)

    def test_attention_and_completion_alerts_are_sent_once_per_declared_event(self):
        module = self.load_notifier()
        ledger = self.root / "ledger.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)
        fields = dict(task="Export report", text="Choose the file format.", chat_name="Claude Code · Export",
                      link="https://example.invalid/chat/1")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **fields), "sent")
        self.assertEqual(sent[0], "🔔 Action required\n\nProject: demo\nReference: a / CARD-00000135\n"
                                  "Summary: Choose the file format.\n\n"
                                  "Next action: Return to the chat and choose the format. — Claude Code · Export\n"
                                  "https://example.invalid/chat/1")
        done = dict(fields, text="Rapport exporté et vérifié.", language="fr", next_action="Aucune action requise.")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="delivery", **done), "sent")
        self.assertTrue(sent[1].startswith("✅ Travail terminé\n\nProjet: demo"))
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **fields), "duplicate")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="delivery", **done), "duplicate")
        # Rewording, language and chat changes are resends; a new ID, task, module or project is a new alert.
        self.assertEqual(self.alert(module, ledger, sender, id="request-1",
                                    **dict(fields, text="Choose a format, please.", chat_name="Resumed")), "duplicate")
        self.assertEqual(self.alert(module, ledger, sender, id="request-2", **fields), "sent")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **dict(fields, task="Import report")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", module="b", **fields), "sent")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", project="other", **fields), "sent")
        self.assertEqual(len(sent), 6)

    def test_labels_follow_the_conversation_language(self):
        module = self.load_notifier()
        ledger = self.root / "languages.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)
        self.alert(module, ledger, sender, "completed", task="Export", id="done", text="Export verified.",
                   next_action="No action required.", chat_name="Codex · Export")
        self.assertIn("✅ Work completed", sent[-1])
        self.alert(module, ledger, sender, task="Export", id="es", language="es", label="🔔 Acción requerida",
                   project_label="Proyecto", reference_label="Referencia", summary_label="Resumen",
                   next_action_label="Próxima acción", text="La exportación está lista.",
                   next_action="Elige el formato.", chat_name="Codex · Exportación")
        self.assertIn("🔔 Acción requerida\n\nProyecto: demo", sent[-1])
        self.assertIn("Próxima acción: Elige el formato. — Codex · Exportación", sent[-1])

    def test_unknown_delivery_is_not_resent_blindly(self):
        module = self.load_notifier()
        ledger = self.root / "ledger.sqlite3"
        sent = []

        def failing(definite):
            def sender(token, chat, text):
                raise module.SendFailed(definite)
            return sender

        fields = dict(task="Task", text="Need a decision.", chat_name="Chat", id="request-1")
        good = lambda token, chat, text: sent.append(text)
        self.assertEqual(self.alert(module, ledger, failing(True), **fields), "failed")
        self.assertEqual(self.alert(module, ledger, good, **fields), "sent")  # A definite failure is retryable.
        fields["id"] = "request-2"
        self.assertEqual(self.alert(module, ledger, failing(False), **fields), "unconfirmed")
        self.assertEqual(self.alert(module, ledger, good, **fields), "unconfirmed")  # Blocked until checked.
        self.assertEqual(len(sent), 1)
        self.assertEqual(self.alert(module, ledger, good, confirm_retry=True, **fields), "sent")
        self.assertEqual(self.alert(module, ledger, good, **fields), "duplicate")

    def test_alert_command_reports_state_and_validates_input(self):
        def run(*args, **environment):
            return subprocess.run([sys.executable, str(self.root / "orchestrator/tools/notify-telegram.py"), *args],
                                  cwd=self.root, env={**{k: v for k, v in os.environ.items() if not k.startswith("TELEGRAM_")},
                                       **environment}, capture_output=True, text=True)

        full = ("attention", "--task", "Task", "--id", "r1", "--text", "Need you.", "--chat-name", "Chat",
                "--reference", "CARD-00000135", "--next-action", "Choose the format in the chat.", "--module", "a")
        disabled = run(*full, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="completed")
        self.assertEqual(disabled.returncode, 0)
        self.assertIn("disabled; nothing was sent", disabled.stdout)
        missing = run(*full, TELEGRAM_EVENTS="attention")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("Nothing was sent", missing.stderr)
        preview = run(*full, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="attention")
        self.assertIn("Preview:", preview.stdout)
        self.assertIn("Project: Fixture\nReference: a / CARD-00000135", preview.stdout)
        unscoped = run(*full[:-2], TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="attention")
        self.assertIn("Choose a module explicitly", unscoped.stderr)
        for bad in (("attention", "--task", "Task", "--id", "r1", "--text", "x"),  # No chat name.
                    (*full, "--reference", "Batch-001"),
                    (*full, "--next-action", " "),
                    (*full, "--language", "es"),  # A known language needs translated labels.
                    (*full, "--link", "not a link"),
                    ("delivered", *full[1:])):
            self.assertNotEqual(run(*bad, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="attention").returncode, 0)


if __name__ == "__main__":
    unittest.main()
