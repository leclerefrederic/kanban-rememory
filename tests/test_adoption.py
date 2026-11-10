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
        card.write_text("# TASK-00000001 — Example\n\n## Acceptance criteria\n\n- [ ] Verified\n")
        self.run_board(*options, "--apply")
        for stage in stages[1:stages.index("completion") + 1]:
            card = card.rename(self.board / stage / card.name)
            self.assertIn(f"kanban/{stage}/{card.name}", self.run_board("show"))
        self.assertIn("unchecked acceptance criterion", self.run_board("validate", expected=1))
        card.write_text(card.read_text().replace("[ ]", "[x]"))
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
