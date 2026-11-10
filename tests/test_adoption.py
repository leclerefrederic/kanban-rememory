import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


KIT = Path(__file__).resolve().parents[1]
INSTALL_FILES = (
    "agents/adoption.md", "agents/working-instructions.md",
    "docs/kanban.md", "docs/software-development.md",
    "docs/card-guide.md", "docs/task-template.md",
    "tools/board.py", "Rememory/README.md", "Rememory/daily-template.md",
)


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.board = self.root / "kanban"
        for name in INSTALL_FILES:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(KIT / name, destination)
        (self.root / "AGENTS.md").write_text(
            "Read the [shared working instructions](agents/working-instructions.md) "
            "before adopting the kit or working on cards.\n", encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def run_board(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, "tools/board.py", *args],
            cwd=self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def lifecycle(self, template, stages):
        options = ("init", "--template", template)
        self.assertIn("Preview only", self.run_board(*options))
        self.assertFalse(self.board.exists())
        self.run_board(*options, "--apply")
        self.run_board("validate")
        self.assertEqual(self.run_board("show").splitlines()[:-1], stages)
        card = self.board / stages[0] / "TASK-00000001-example.md"
        self.assertIn("Preview", self.run_board("new", "Example", "--owner", "Test team"))
        self.assertFalse(card.exists())
        self.run_board("new", "Example", "--owner", "Test team", "--apply")
        self.assertIn("- Owner: Test team", card.read_text())
        journal = self.root / "Rememory/journal.md"
        journal.write_text(
            f"[Criteria](../kanban/{stages[0]}/{card.name}#acceptance-criteria)\n"
            "`[Example](../kanban/backlog/TASK-00000001-example.md)`\n"
            "[External](https://example.com/kanban/backlog/TASK-00000001-example.md)\n"
        )
        sibling = card.parent / "TASK-00000002-sibling.md"
        sibling.write_text("# TASK-00000002 — Sibling\n")
        with card.open("a") as stream:
            stream.write(f"\n[Related]({sibling.name})\n")
        self.run_board(*options, "--apply")
        self.run_board("validate")
        for stage in stages[1:stages.index("completion") + 1]:
            if stage == "completion":
                self.assertIn("acceptance checklist", self.run_board(
                    "move", "TASK-00000001", stage, expected=1))
                card.write_text(card.read_text().replace("[ ]", "[x]"))
            self.run_board("move", "TASK-00000001", stage)
            card = self.board / stage / card.name
            self.assertIn(f"kanban/{stage}/{card.name}", self.run_board("show"))
            self.assertIn(f"../kanban/{stage}/{card.name}#acceptance-criteria", journal.read_text())
            self.assertIn("`[Example](../kanban/backlog/TASK-00000001-example.md)`", journal.read_text())
            self.assertIn("https://example.com/kanban/backlog/TASK-00000001-example.md", journal.read_text())
            self.assertIn(f"[Related](../backlog/{sibling.name})", card.read_text())
            self.run_board("validate")
        self.run_board("validate")

    def test_short(self):
        self.lifecycle("short", ["backlog", "development", "completion", "archive"])

    def test_standard(self):
        self.lifecycle("standard", ["backlog", "development", "code-review", "completion", "archive"])

    def test_long(self):
        self.lifecycle("long", ["backlog", "refinement", "development", "code-review",
                                "testing", "deployment", "completion", "archive"])

    def test_custom_and_conflict(self):
        source = self.root / "custom.json"
        source.write_text(json.dumps({
            "stages": ["queue", "build", "shipped"], "active": ["build"],
            "completed": "shipped", "wip_limit": 2, "timezone": "UTC",
        }))
        self.run_board("init", "--config", "custom.json", "--apply")
        config = (self.board / "workflow.json").read_bytes()
        self.assertIn("WIP: 0/2", self.run_board("show"))
        self.assertIn("different workflow", self.run_board(
            "init", "--template", "short", "--apply", expected=1))
        self.assertEqual((self.board / "workflow.json").read_bytes(), config)
        self.assertFalse((self.board / "backlog").exists())
        self.run_board("validate")

    def test_move_guards_and_rework(self):
        self.run_board("init", "--template", "standard", "--apply")
        name = "TASK-00000001-example.md"
        source = self.board / "backlog" / name
        content = "# TASK-00000001 — Example\n- Actual start: 2026-11-10\n"
        source.write_text(content)
        self.assertIn("not allowed", self.run_board("move", "TASK-00000001",
                                                    "code-review", expected=1))
        self.run_board("move", "TASK-00000001", "development")
        second = self.board / "backlog/TASK-00000002-example.md"
        second.touch()
        self.assertIn("WIP limit reached", self.run_board("move", "TASK-00000002",
                                                          "development", expected=1))
        self.assertTrue(second.exists())
        self.run_board("move", "TASK-00000001", "code-review")
        self.run_board("move", "TASK-00000001", "development")
        self.assertEqual((self.board / "development" / name).read_text(), content)

    def test_new_uses_custom_intake_and_archived_ids(self):
        source = self.root / "custom.json"
        source.write_text(json.dumps({
            "stages": ["queue", "build", "shipped", "archive"],
            "active": ["build"], "completed": "shipped",
            "wip_limit": 1, "timezone": "UTC",
        }))
        self.run_board("init", "--config", "custom.json", "--apply")
        archived = self.board / "archive/TASK-00000009-archived.md"
        archived.touch()
        self.run_board("new", "Test adoption", "--owner", "Maintainers", "--apply")
        self.assertTrue((self.board / "queue/TASK-00000010-test-adoption.md").is_file())
        (self.board / "shipped" / archived.name).touch()
        self.assertIn("Duplicate TASK-00000009", self.run_board(
            "new", "Another card", "--owner", "Maintainers", "--apply", expected=1))
        self.assertEqual(len(list((self.board / "queue").glob("*.md"))), 1)
