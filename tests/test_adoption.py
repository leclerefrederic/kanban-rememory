from hashlib import sha256
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
    "agents/actor-user.md", "agents/actor-specification-agent.md", "agents/actor-development-agent.md",
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

    def test_move_preserves_closed_history(self):
        self.run_board("init", "--template", "short", "--apply")
        self.run_board("new", "Linked task", "--owner", "Maintainers", "--apply")
        card = self.board / "backlog/TASK-00000001-linked-task.md"
        specs = self.root / "specs"
        specs.mkdir()
        (specs / "sheet.md").write_text("# Specification\n")
        card.write_text(card.read_text().replace(
            "- Link to other authoritative references.", "- Reference: [Sheet](../../specs/sheet.md)"
        ).replace("[ ]", "[x]"))
        completed = self.board / "completion/TASK-00000002-history.md"
        completed.write_text(f"[Task](../backlog/{card.name})\n")
        original = completed.read_bytes()
        self.assertIn("immutable history", self.run_board("move", "TASK-00000001",
                                                         "development", expected=1))
        self.assertEqual(completed.read_bytes(), original)
        self.assertTrue(card.exists())
        completed.write_text("Reference: TASK-00000001\n")
        lot = self.root / "Lots/Lot-001"
        lot.mkdir(parents=True)
        (specs / "frozen").mkdir()
        (specs / "frozen/FICHE-001-r1.md").write_text("- Fiche ID: FICHE-001\n- Revision: 1\n")
        digest = sha256((specs / "frozen/FICHE-001-r1.md").read_bytes()).hexdigest()
        (lot / "Description.md").write_text(
            f"---\nstatus: closed\n---\n- Fiche: FICHE-001 | 1 | specs/frozen/FICHE-001-r1.md | {digest}\n"
        )
        report = lot / "Report.md"
        report.write_text(f"[Task](../../kanban/backlog/{card.name})\n")
        original = report.read_bytes()
        self.assertIn("immutable history", self.run_board("move", "TASK-00000001",
                                                         "development", expected=1))
        self.assertEqual(report.read_bytes(), original)
        self.assertTrue(card.exists())
        report.write_text("Reference: TASK-00000001\n")
        self.run_board("move", "TASK-00000001", "development")
        self.run_board("move", "TASK-00000001", "completion")
        self.run_board("validate")

    def test_lot_mapping(self):
        self.run_board("init", "--template", "short", "--apply")
        for stage in ("draft", "ready", "frozen"):
            (self.root / "specs" / stage).mkdir(parents=True)
        for stage, number in (("frozen", 1), ("ready", 2), ("draft", 3)):
            (self.root / "specs" / stage / f"FICHE-00{number}-r1.md").write_text(
                f"- Fiche ID: FICHE-00{number}\n- Revision: 1\n"
            )
        lot = self.root / "Lots/Lot-001"
        lot.mkdir(parents=True)
        description = lot / "Description.md"
        description.write_text("# Lot\n")
        self.assertIn("at least one frozen Fiche", self.run_board("validate", expected=1))
        frozen = self.root / "specs/frozen/FICHE-001-r1.md"
        original = frozen.read_bytes()
        digest = sha256(original).hexdigest()
        description.write_text(f"- Fiche: FICHE-001 | 2 | specs/frozen/FICHE-001-r1.md | {digest}\n")
        self.assertIn("matching frozen ID, revision, and path", self.run_board("validate", expected=1))
        description.write_text(f"- Fiche: FICHE-001 | 1 | specs/frozen/FICHE-001-r1.md | {digest}\n")
        frozen.write_bytes(original + b"\nEdited after approval.\n")
        self.assertIn("Frozen Fiche content changed", self.run_board("validate", expected=1))
        frozen.write_bytes(original)
        card = self.board / "backlog/TASK-00000001-linked.md"
        card.write_text("- Lot ID: Lot-001\n- Fiche IDs: FICHE-001, FICHE-002, FICHE-003\n")
        result = self.run_board("validate", expected=1)
        self.assertIn("Fiche FICHE-002 is outside Lot Lot-001", result)
        self.assertIn("Fiche is not ready or frozen: FICHE-003", result)
        card.write_text("- Lot ID: Lot-999\n")
        self.assertIn("unknown Lot", self.run_board("validate", expected=1))
        card.write_text("- Lot ID: Lot-001\n- Fiche IDs: FICHE-001\n")
        self.run_board("validate")
        card.write_text("- Fiche IDs: FICHE-001, FICHE-002\n")
        self.run_board("validate")
