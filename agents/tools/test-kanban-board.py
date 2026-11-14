from hashlib import sha256
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
INSTALL_FILES = (
    "documentation/index.md", "documentation/understand-the-framework.md",
    "documentation/start-a-project.md", "documentation/deliver-a-batch.md",
    "documentation/test-and-accept-a-batch.md", "documentation/use-kanban-rememory-runner.md",
    "documentation/lean-specifications.md",
    "documentation/assign-a-task.md", "documentation/resume-work.md", "documentation/report-a-defect.md", "documentation/use-with-chatgpt-and-claude.md",
    "documentation/examples/project-specification.md", "documentation/examples/batch-description.md",
    "documentation/examples/kanban-card.md", "documentation/examples/batch-tests.md",
    "documentation/examples/batch-report.md",
    "agents/configure-a-project.md", "agents/work-in-a-project.md", "agents/lean-specifications.md",
    "agents/roles/user.md", "agents/roles/specification-agent.md", "agents/roles/development-agent.md",
    "agents/kanban/board-guide.md", "agents/kanban/software-development-workflow.md",
    "agents/kanban/write-task-cards.md", "agents/templates/kanban-card.md", "agents/templates/project-layout.md",
    "agents/tools/manage-kanban-board.py", "agents/maintain-rememory.md", "project/rememory/daily-template.md",
)


class KanbanBoardTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.board = self.root / "project/kanban"
        for name in INSTALL_FILES:
            destination = self.root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(KIT / name, destination)
        shutil.copytree(KIT / "agents/tools/kanban", self.root / "agents/tools/kanban",
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "AGENTS.md").write_text(
            "Read the [shared working instructions](agents/work-in-a-project.md) "
            "before adopting the kit or working on cards.\n", encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def run_board(self, *args, expected=0):
        result = subprocess.run(
            [sys.executable, "agents/tools/manage-kanban-board.py", *args],
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
        card = self.board / stages[0] / "task-00000001-example.md"
        self.assertIn("Preview", self.run_board("new", "Example", "--owner", "Test team"))
        self.assertFalse(card.exists())
        self.run_board("new", "Example", "--owner", "Test team", "--apply")
        self.assertIn("- Owner: Test team", card.read_text())
        card.write_text(card.read_text().replace("## Acceptance criteria\n", "## Acceptance criteria\n\n- [ ] Verified.\n", 1))
        journal = self.root / "project/rememory/journal.md"
        journal.write_text(
            f"[Criteria](../kanban/{stages[0]}/{card.name}#acceptance-criteria)\n"
            "`[Example](../kanban/backlog/task-00000001-example.md)`\n"
            "[External](https://example.com/kanban/backlog/task-00000001-example.md)\n"
        )
        sibling = card.parent / "task-00000002-sibling.md"
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
            self.assertIn(f"project/kanban/{stage}/{card.name}", self.run_board("show"))
            self.assertIn(f"to `{stage}`.", card.read_text())
            self.assertIn(f"../kanban/{stage}/{card.name}#acceptance-criteria", journal.read_text())
            self.assertIn("`[Example](../kanban/backlog/task-00000001-example.md)`", journal.read_text())
            self.assertIn("https://example.com/kanban/backlog/task-00000001-example.md", journal.read_text())
            self.assertIn(f"[Related](../backlog/{sibling.name})", card.read_text())
            self.run_board("validate")
        self.run_board("validate")

    def test_short(self):
        self.lifecycle("short", ["backlog", "development", "completion", "cancellation"])

    def test_standard(self):
        self.lifecycle("standard", ["backlog", "development", "code-review", "completion", "cancellation"])

    def test_long(self):
        self.lifecycle("long", ["backlog", "refinement", "development", "code-review",
                                "testing", "deployment", "completion", "cancellation"])

    def test_custom_and_conflict(self):
        source = self.root / "custom.json"
        source.write_text(json.dumps({
            "stages": ["backlog", "development", "completion", "cancellation"], "active": ["development"],
            "completed": "completion", "wip_limit": 2, "timezone": "UTC",
        }))
        self.run_board("init", "--config", "custom.json", "--apply")
        config = (self.board / "workflow.json").read_bytes()
        self.assertIn("WIP: 0/2", self.run_board("show"))
        self.assertIn("different workflow", self.run_board(
            "init", "--template", "short", "--apply", expected=1))
        self.assertEqual((self.board / "workflow.json").read_bytes(), config)
        self.assertTrue((self.board / "cancellation").is_dir())
        self.run_board("validate")

    def test_move_guards_and_rework(self):
        self.run_board("init", "--template", "standard", "--apply")
        name = "task-00000001-example.md"
        source = self.board / "backlog" / name
        content = "# TASK-00000001 — Example\n- Actual start: 2026-11-10\n"
        source.write_text(content)
        self.assertIn("not allowed", self.run_board("move", "TASK-00000001",
                                                    "code-review", expected=1))
        self.run_board("move", "TASK-00000001", "development")
        second = self.board / "backlog/task-00000002-example.md"
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
        self.assertIn("Missing required stages", self.run_board(
            "init", "--config", "custom.json", "--apply", expected=1))
        for stage in ("queue", "build", "shipped", "archive"):
            (self.board / stage).mkdir(parents=True)
        (self.board / "workflow.json").write_bytes(source.read_bytes())
        archived = self.board / "archive/task-00000009-archived.md"
        archived.touch()
        self.run_board("new", "Test adoption", "--owner", "Maintainers", "--apply")
        self.assertTrue((self.board / "queue/task-00000010-test-adoption.md").is_file())
        (self.board / "shipped" / archived.name).touch()
        self.assertIn("Duplicate TASK-00000009", self.run_board(
            "new", "Another card", "--owner", "Maintainers", "--apply", expected=1))
        self.assertEqual(len(list((self.board / "queue").glob("*.md"))), 1)

    def test_move_preserves_closed_history(self):
        self.run_board("init", "--template", "short", "--apply")
        self.run_board("new", "Linked task", "--owner", "Maintainers", "--apply")
        card = self.board / "backlog/task-00000001-linked-task.md"
        specs = self.root / "project/specs"
        specs.mkdir()
        (specs / "sheet.md").write_text("# Specification\n")
        card.write_text(card.read_text().replace(
            "## Acceptance criteria\n", "## Acceptance criteria\n\n- [x] Verified.\n", 1
        ) + "\n- Reference: [Sheet](../../specs/sheet.md)\n")
        completed = self.board / "completion/task-00000002-history.md"
        completed.write_text(f"[Task](../backlog/{card.name})\n")
        original = completed.read_bytes()
        self.assertIn("immutable history", self.run_board("move", "TASK-00000001",
                                                         "development", expected=1))
        self.assertEqual(completed.read_bytes(), original)
        self.assertTrue(card.exists())
        completed.write_text("Reference: TASK-00000001\n")
        lot = self.root / "project/lots/Lot-001"
        lot.mkdir(parents=True)
        (specs / "frozen").mkdir()
        (specs / "frozen/fiche-001-r1.md").write_text("- Fiche ID: FICHE-001\n- Revision: 1\n")
        digest = sha256((specs / "frozen/fiche-001-r1.md").read_bytes()).hexdigest()
        (lot / "description.md").write_text(
            f"---\nstatus: closed\n---\n- Fiche: FICHE-001 | 1 | project/specs/frozen/fiche-001-r1.md | {digest}\n"
        )
        report = lot / "report.md"
        report.write_text(f"[Task](../../kanban/backlog/{card.name})\n")
        original = report.read_bytes()
        self.assertIn("immutable history", self.run_board("move", "TASK-00000001",
                                                         "development", expected=1))
        self.assertEqual(report.read_bytes(), original)
        self.assertTrue(card.exists())
        self.assertIn("cannot link to Kanban", self.run_board("validate", expected=1))
        report.write_text("Reference: TASK-00000001\n")
        self.assertIn("cannot reference Card", self.run_board("validate", expected=1))
        report.write_text("Historical delivery evidence.\n")
        self.run_board("move", "TASK-00000001", "development")
        self.run_board("move", "TASK-00000001", "completion")
        self.run_board("validate")

    def test_lot_mapping(self):
        self.run_board("init", "--template", "short", "--apply")
        for stage in ("draft", "ready", "frozen"):
            (self.root / "project/specs" / stage).mkdir(parents=True)
        for stage, number in (("frozen", 1), ("ready", 2), ("draft", 3)):
            (self.root / "project/specs" / stage / f"fiche-00{number}-r1.md").write_text(
                f"- Fiche ID: FICHE-00{number}\n- Revision: 1\n"
            )
        lot = self.root / "project/lots/Lot-001"
        lot.mkdir(parents=True)
        description = lot / "description.md"
        description.write_text("# Lot\n")
        self.assertIn("at least one approved specification", self.run_board("validate", expected=1))
        frozen = self.root / "project/specs/frozen/fiche-001-r1.md"
        original = frozen.read_bytes()
        digest = sha256(original).hexdigest()
        description.write_text(f"- Fiche: FICHE-001 | 2 | project/specs/frozen/fiche-001-r1.md | {digest}\n")
        self.assertIn("matching approved ID, revision, and path", self.run_board("validate", expected=1))
        description.write_text(f"- Fiche: FICHE-001 | 1 | project/specs/frozen/fiche-001-r1.md | {digest}\n")
        frozen.write_bytes(original + b"\nEdited after approval.\n")
        self.assertIn("Approved specification content changed", self.run_board("validate", expected=1))
        frozen.write_bytes(original)
        card = self.board / "backlog/task-00000001-linked.md"
        card.write_text("- Lot ID: Lot-001\n- Fiche IDs: FICHE-001, FICHE-002, FICHE-003\n")
        result = self.run_board("validate", expected=1)
        self.assertIn("Specification FICHE-002 is outside batch Lot-001", result)
        self.assertIn("Specification is not ready or approved: FICHE-003", result)
        card.write_text("- Lot ID: Lot-999\n")
        self.assertIn("Unknown batch", self.run_board("validate", expected=1))
        card.write_text("- Lot ID: Lot-001\n- Fiche IDs: FICHE-001\n")
        self.run_board("validate")
        card.write_text("- Fiche IDs: FICHE-001, FICHE-002\n")
        self.run_board("validate")

    def test_verify_approval_detects_external_edits(self):
        self.run_board("init", "--template", "short", "--apply")
        fiche = self.root / "project/specs/frozen/fiche-001-r1.md"
        fiche.parent.mkdir(parents=True)
        original = b"- Fiche ID: FICHE-001\n- Revision: 1\nApproved scope\n"
        fiche.write_bytes(original)
        description = self.root / "project/Lots/Lot-001/description.md"
        description.parent.mkdir(parents=True)
        digest = sha256(original).hexdigest()
        approved = (f"---\nstatus: ready\n---\n- Fiche: FICHE-001 | 1 | "
                    f"project/specs/frozen/fiche-001-r1.md | {digest}\nMission: export CSV\n")
        description.write_text(approved)
        subprocess.run(["git", "add", "project/Lots", "project/specs"], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "Approve Lot"], cwd=self.root, check=True)
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        approved_folder = fiche.parent.with_name("approved")
        fiche.parent.rename(approved_folder)
        fiche = approved_folder / fiche.name
        command = ("verify-approval", "Lot-001", revision)
        self.run_board(*command)
        changed = original + b"External edit\n"
        fiche.write_bytes(changed)
        self.assertIn("Approved specification content changed", self.run_board(*command, expected=1))
        description.write_text(approved.replace(digest, sha256(changed).hexdigest()))
        self.run_board("validate")
        self.assertIn("Approval mismatch", self.run_board(*command, expected=1))
        fiche.write_bytes(original)
        description.write_text(approved.replace("export CSV", "export all records"))
        self.assertIn("Approval mismatch", self.run_board(*command, expected=1))
        description.write_text(approved)
        self.run_board(*command)

    def populate_lot_templates(self, lot):
        templates = KIT / "agents/templates"
        for name in ("description.md", "tests.md", "report.md"):
            source = (templates / f"batch-{name}").read_text()
            document_id = "Batch-001" if name == "description.md" else f"Batch-001-{Path(name).stem.title()}"
            source = source.replace("id: null", f'id: "{document_id}"').replace("batch: null", 'batch: "Batch-001"')
            source = source.replace("status: draft", "status: ready").replace(
                "specifications: []", 'specifications: [{"id":"SPEC-001","revision":"1","path":"project/specs/approved/spec-001-r1.md"}]'
            )
            (lot / name).write_text(source)

    def test_digest_free_approval_and_closure(self):
        self.run_board("init", "--template", "short", "--apply")
        fiche = self.root / "project/specs/approved/spec-001-r1.md"
        fiche.parent.mkdir(parents=True)
        original = b'- Fiche ID: SPEC-001\n- Revision: 1\n'
        fiche.write_bytes(original)
        lot = self.root / "project/batches/batch-001"
        lot.mkdir(parents=True)
        self.populate_lot_templates(lot)
        subprocess.run(["git", "add", "project/batches", "project/specs"], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "Approve Lot"], cwd=self.root, check=True)
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        command = ("verify-approval", "Batch-001", revision)
        self.run_board(*command)
        description = lot / "description.md"
        description.write_text(description.read_text().replace("status: ready", "status: validated"))
        self.run_board(*command)
        fiche.write_bytes(original + b"Changed scope\n")
        self.run_board("validate")
        self.assertIn("Approval mismatch", self.run_board(*command, expected=1))

    def test_yaml_lot_cross_references(self):
        self.run_board("init", "--template", "short", "--apply")
        fiche = self.root / "project/specs/approved/spec-001-r1.md"
        fiche.parent.mkdir(parents=True)
        fiche.write_text('---\ntype: specification\nid: "SPEC-001"\nrevision: "1"\n---\n')
        lot = self.root / "project/batches/batch-001"
        lot.mkdir(parents=True)
        self.populate_lot_templates(lot)
        self.run_board("new", "Check Lot", "--owner", "Test", "--apply")
        card = self.board / "backlog/task-00000001-check-lot.md"
        source = card.read_text().replace("batch: null", 'batch: "Batch-001"')
        card.write_text(source.replace("specifications: []", 'specifications: ["SPEC-001"]'))
        self.run_board("validate")
        report = lot / "report.md"
        report.write_text(report.read_text().replace('batch: "Batch-001"', 'batch: "Batch-999"'))
        self.assertIn("Inconsistent YAML references for report.md", self.run_board("validate", expected=1))
        report.write_text(report.read_text().replace('batch: "Batch-999"', 'batch: "Batch-001"'))
        description = lot / "description.md"
        tests = lot / "tests.md"
        for document, old_refs in (
            (description, 'tests: "Batch-001-Tests"\nreport: "Batch-001-Report"\n'),
            (tests, 'report: "Batch-001-Report"\n'),
            (report, 'tests: "Batch-001-Tests"\n'),
        ):
            document.write_text(document.read_text().replace("---\n", "---\n" + old_refs, 1))
        for document in (lot / "description.md", lot / "tests.md", report, card):
            source = document.read_text()
            for key in ("tests", "report"):
                source = source.replace(f"\n{key}:", f"\n{key}_id:")
            source = source.replace("\nbatch:", "\nlot_id:")
            if document == card:
                source = source.replace("\nspecifications:", "\nfiche_ids:")
            document.write_text(source)
        self.run_board("validate")


    def test_draft_batch_preparation_keeps_ready_requirements(self):
        self.run_board("init", "--template", "short", "--apply")
        batch = self.root / "project/batches/batch-001"
        batch.mkdir(parents=True)
        description = batch / "description.md"
        draft = (KIT / "agents/templates/batch-description.md").read_text().replace(
            "id: null", 'id: "Batch-001"')
        description.write_text(draft)
        self.run_board("validate")
        description.write_text(draft.replace("status: draft", "status: []"))
        self.assertIn("Unknown Batch status", self.run_board("validate", expected=1))
        description.write_text(draft.replace("status: draft", "status: ready"))
        result = self.run_board("validate", expected=1)
        self.assertIn("at least one approved specification", result)
        self.assertIn("Inconsistent YAML references for tests.md", result)

        spec = self.root / "project/specs/ready/spec-001-r1.md"
        spec.parent.mkdir(parents=True)
        spec.write_text('---\ntype: specification\nid: "SPEC-001"\nrevision: "1"\n---\n')
        selection = json.dumps([{"id": "SPEC-001", "revision": "1", "path": str(spec.relative_to(self.root))}])
        prepared = draft.replace("specifications: []", "specifications: " + selection)
        description.write_text(prepared)
        self.run_board("validate")
        description.write_text(prepared.replace('"revision": "1"', '"revision": "2"'))
        self.assertIn("matching ready or approved", self.run_board("validate", expected=1))
        self.populate_lot_templates(batch)
        description.write_text(prepared.replace("status: draft", "status: ready"))
        self.assertIn("matching approved", self.run_board("validate", expected=1))
        approved = spec.parent.with_name("approved")
        approved.mkdir()
        spec.rename(approved / spec.name)
        ready = description.read_text().replace("project/specs/ready/", "project/specs/approved/")
        description.write_text(ready)
        self.run_board("validate")
        description.write_text(ready.replace("status: ready", "status: draft"))
        report = batch / "report.md"
        report.write_text(report.read_text().replace('batch: "Batch-001"', 'batch: "Batch-999"'))
        self.assertIn("Inconsistent YAML references for report.md", self.run_board("validate", expected=1))

    def test_batch_ids_and_approval_through_correction(self):
        self.run_board("init", "--template", "short", "--apply")
        spec = self.root / "project/specs/approved/spec-001-r1.md"
        spec.parent.mkdir(parents=True)
        spec.write_text('---\ntype: specification\nid: "SPEC-001"\nrevision: "1"\n---\n')
        batch = self.root / "project/batches/batch-001"
        batch.mkdir(parents=True)
        self.assertIn("batch_id", self.run_board("verify-approval", "--help"))
        for record_id in ("Batch-001", "batch-001"):
            with self.subTest(record_id=record_id):
                self.populate_lot_templates(batch)
                for path in batch.glob("*.md"):
                    path.write_text(path.read_text().replace("Batch-001", record_id))
                self.run_board("validate")
                subprocess.run(["git", "add", "project"], cwd=self.root, check=True)
                subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                                "commit", "-qm", "Approve Batch"], cwd=self.root, check=True)
                revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
                description = batch / "description.md"
                original = description.read_text()
                for status in ("ready", "in-progress", "delivered", "validated", "rejected", "closed"):
                    description.write_text(original.replace("status: ready", "status: " + status))
                    self.run_board("verify-approval", "batch-001", revision)
                    self.run_board("verify-approval", "Batch-001", revision)
                description.write_text(original.replace("status: ready", "status: draft"))
                self.assertIn("past draft", self.run_board("verify-approval", "batch-001", revision, expected=1))
                description.write_text(original + "\nChanged approved mission\n")
                self.assertIn("Approval mismatch", self.run_board("verify-approval", "batch-001", revision, expected=1))

    def test_batch_module_installation_and_worked_example(self):
        shutil.copytree(KIT / "agents/batches", self.root / "agents/batches")
        for name in ("project-specification.md", "batch-description.md", "batch-tests.md", "batch-report.md"):
            shutil.copy(KIT / "agents/templates" / name, self.root / "agents/templates" / name)
        shutil.copy(KIT / "agents/run-scheduled-batch-job.md", self.root / "agents")
        shutil.copy(KIT / "agents/tools/guard-batch-work.py", self.root / "agents/tools")
        self.run_board("init", "--template", "short", "--apply")
        self.run_board("validate")
        example = (self.root / "agents/batches/delivery-example.md").read_text()
        records = re.findall(r"```markdown\n(.*?)\n```", example, re.DOTALL)
        self.assertEqual(len(records), 4)
        destinations = ("project/specs/approved/spec-001-r1.md", "project/batches/batch-001/description.md",
                        "project/batches/batch-001/tests.md", "project/batches/batch-001/report.md")
        for destination, record in zip(destinations, records):
            path = self.root / destination
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(record + "\n")
        self.run_board("validate")

    def test_batch_guard_uses_workflow_and_configured_build_files(self):
        shutil.copy(KIT / "agents/tools/guard-batch-work.py", self.root / "agents/tools")
        self.run_board("init", "--template", "short", "--apply")
        workflow = self.board / "workflow.json"
        config = json.loads(workflow.read_text())
        config["active"] = ["review"]
        config["stages"].insert(1, "review")
        workflow.write_text(json.dumps(config))
        (self.board / "review").mkdir()
        (self.board / "review/task-00000001-example.md").write_text("card\n")

        def git(*args):
            return subprocess.check_output(["git", "-c", "user.name=Test", "-c", "user.email=t@example.invalid",
                                            *args], cwd=self.root, text=True).strip()

        def guard(record, *args, expected=0):
            path = self.root / "record.json"
            path.write_text(json.dumps(record))
            result = subprocess.run([sys.executable, "agents/tools/guard-batch-work.py", *args, "record.json"],
                                    cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result.stdout + result.stderr

        (self.root / "app").mkdir()
        (self.root / "app/artifact").write_text("build\n")
        git("add", "."); git("commit", "-qm", "base")
        base = git("rev-parse", "HEAD")
        (self.root / "build-app.sh").write_text("echo build\n")
        git("add", "build-app.sh"); git("commit", "-qm", "build script")
        head = git("rev-parse", "HEAD")
        digest = subprocess.check_output([sys.executable, "-c",
            "import importlib.util as u;s=u.spec_from_file_location('g','agents/tools/guard-batch-work.py');"
            "m=u.module_from_spec(s);s.loader.exec_module(m);from pathlib import Path;"
            "print(m.artifact_digest(Path('app/artifact')))"], cwd=self.root, text=True).strip()
        record = {"authorized_cards": ["TASK-00000001"], "base_revision": base,
                  "acceptance": {"revision": head, "path": str(self.root / "app/artifact"), "sha256": digest},
                  "verification": {"revision": head, "technical_checks": "passed"},
                  "decision": {"revision": head, "result": "accepted"}}
        self.assertIn("passed", guard({**record, "acceptance": None}, "change", "--card", "TASK-00000001"))
        self.assertIn("Record out-of-scope", guard({**record, "acceptance": None}, "change", "--card",
                                                   "TASK-00000002", expected=1))
        self.assertIn("passed", guard(record, "publish"))
        strict = {**record, "full_build_files": ["build-app.sh"]}
        self.assertIn("require a successful full build", guard(strict, "publish", expected=1))
        strict["verification"]["full_build"] = "passed"
        self.assertIn("passed", guard(strict, "publish"))

    def test_notification_batch_id_preview(self):
        environment = {**os.environ, "TELEGRAM_CHAT_ID": "42", "TELEGRAM_EVENTS": "delivered"}
        environment.pop("TELEGRAM_BOT_TOKEN", None)
        for identifier in ("Batch-001", "batch-001", "BATCH-001", "bad-id"):
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, str(KIT / "agents/tools/notify-telegram.py"),
                                         "delivered", "--batch", identifier], env=environment,
                                        capture_output=True, text=True)
                if identifier == "bad-id":
                    self.assertNotEqual(result.returncode, 0)
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("Preview:", result.stdout)


if __name__ == "__main__":
    unittest.main()
