import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
import importlib.util
from hashlib import sha256
from io import StringIO
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


KIT = Path(__file__).resolve().parents[2]
INSTALL_FILES = (
    'documentation/assign-a-task.md',
    'documentation/deliver-a-batch.md',
    'documentation/examples/batch-description.md',
    'documentation/examples/batch-report.md',
    'documentation/examples/batch-tests.md',
    'documentation/examples/card.md',
    'documentation/examples/specification.md',
    'documentation/index.md',
    'documentation/lean-specifications.md',
    'documentation/report-a-defect.md',
    'documentation/resume-work.md',
    'documentation/start-a-project.md',
    'documentation/telegram-setup.md',
    'documentation/test-and-accept-a-batch.md',
    'documentation/understand-the-framework.md',
    'documentation/use-with-chatgpt-and-claude.md',
    'documentation/user-responsibilities.md',
    'agents/index.md',
    'agents/VERSION',
    'agents/guidelines/batches.md',
    'agents/guidelines/kanban.md',
    'agents/guidelines/lean-specifications.md',
    'agents/guidelines/working-rules.md',
    'agents/actions/close-batch.md',
    'agents/actions/coordinate-modules.md',
    'agents/actions/develop-batch.md',
    'agents/actions/maintain-rememory.md',
    'agents/actions/manage-board.md',
    'agents/actions/notify-user.md',
    'agents/actions/orchestrate-work.md',
    'agents/actions/resume-work.md',
    'agents/actions/scheduled-batch-job.md',
    'agents/actions/write-card.md',
    'agents/setup/batches.md',
    'agents/setup/claude-role-check.md',
    'agents/setup/configure-workflow.md',
    'agents/setup/install.md',
    'agents/setup/project-layout.md',
    'agents/setup/project-modules.md',
    'agents/setup/skills.md',
    'agents/setup/telegram.md',
    'agents/templates/batch-description.md',
    'agents/templates/batch-report.md',
    'agents/templates/batch-tests.md',
    'agents/templates/card.md',
    'agents/templates/rememory-day.md',
    'agents/templates/specification.md',
    'agents/roles/orchestrator.md',
    'agents/roles/writer.md',
    'agents/roles/developer.md',
    'agents/roles/tester.md',
    'agents/tools/manage-kanban-board.py',
    'agents/tools/manage-module-delivery.py',
    'agents/tools/notify-telegram.py',
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
            "Read the [shared working instructions](agents/guidelines/working-rules.md) "
            "before adopting the kit or working on cards.\n", encoding="utf-8",
        )
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def run_board(self, *args, expected=0, cwd=None):
        result = subprocess.run(
            [sys.executable, "agents/tools/manage-kanban-board.py", *args],
            cwd=cwd or self.root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def initialize_modules(self):
        manifest = {
            "schema_version": 1,
            "project": {"id": "fixture", "name": "Fixture"},
            "shared": {"memory": "project/rememory", "sources": []},
            "modules": {
                name: {"workspace": f"project/modules/{name}"} for name in ("a", "b")
            },
            "execution": {
                "active_deliveries_per_module": 1,
                "branch_required": True,
                "worktree_required": True,
                "concurrent_integrations": 1,
            },
        }
        (self.root / "project.json").write_text(json.dumps(manifest), encoding="utf-8")
        self.run_board("init", "--template", "short", "--apply")
        for name in manifest["modules"]:
            (self.root / manifest["modules"][name]["workspace"] / "rememory").mkdir(parents=True)
        return tuple(self.root / "project/modules" / name for name in ("a", "b"))

    def commit_fixture(self, message):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "commit", "-qm", message], cwd=self.root, check=True,
        )
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def module_worktree(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        worktree = Path(scratch.name) / "candidate"
        subprocess.run(["git", "worktree", "add", "-qb", "candidate", str(worktree)], cwd=self.root, check=True)
        return worktree

    def test_module_scoped_commands_on_shared_board(self):
        self.initialize_modules()
        self.assertIn("Choose a module scope", self.run_board("new", "Ambiguous", "--owner", "Test", "--apply", expected=1))
        self.run_board("--module", "a", "new", "Twin", "--owner", "Owner A", "--apply")
        self.run_board("new", "Twin", "--owner", "Owner B", "--apply", "--module", "b")
        cards = self.board / "backlog"
        card_a = cards / "card-00000001-twin.md"
        card_b = cards / "card-00000002-twin.md"
        b_content = card_b.read_text()
        self.assertIn('scope: "a"', card_a.read_text())
        self.assertIn('scope: "b"', b_content)
        view = self.run_board("show", "--scope", "a")
        self.assertIn("CARD-00000001", view)
        self.assertNotIn("CARD-00000002", view)
        self.assertIn("CARD-00000002", self.run_board("show"))
        self.assertIn("does not belong", self.run_board("--module", "b", "move", "a/CARD-00000001", "development", expected=2))
        self.assertIn("belongs to scope a", self.run_board("--scope", "b", "move", "CARD-00000001", "development", expected=1))
        self.assertIn("--owner-token", self.run_board("move", "CARD-00000001", "development", expected=1))
        revision = self.commit_fixture("Initialize module fixture")
        worktree = self.module_worktree()
        subprocess.run(
            [sys.executable, "-c",
             "import sys; sys.path.insert(0, 'agents/tools'); "
             "from kanban.coordination import Coordination; "
             "Coordination('.', 'a').claim('owner-a', 'CARD-00000001', sys.argv[1])", revision],
            cwd=worktree, check=True,
        )
        self.assertIn("unclaimed", self.run_board(
            "--scope", "@project", "reassign", "CARD-00000001", "--to-scope", "b", expected=1,
        ))
        self.assertIn("No matching ownership", self.run_board(
            "move", "CARD-00000001", "development", "--owner-token", "wrong-owner", cwd=worktree, expected=1,
        ))
        self.run_board("move", "CARD-00000001", "development", "--owner-token", "owner-a", cwd=worktree)
        self.assertFalse(card_a.exists())
        self.assertTrue((self.board / "development" / card_a.name).is_file())
        self.assertEqual(b_content, card_b.read_text())
        self.run_board("validate")

    def test_scoped_creation_reserves_global_ids_and_preserves_history(self):
        a, _ = self.initialize_modules()
        central_history = self.board / "completion/card-00000010-before-modules.md"
        module_history = a / "kanban/completion/card-00000011-old-module-record.md"
        module_history.parent.mkdir(parents=True)
        central_history.write_bytes(b"# Historical project Card\n")
        module_history.write_bytes(b"# Historical module Card\n")
        with ThreadPoolExecutor(max_workers=3) as concurrent:
            requests = [
                concurrent.submit(self.run_board, "new", scope, "--owner", "Fixture",
                                  "--scope", scope, "--apply")
                for scope in ("a", "b", "@project")
            ]
            for request in requests:
                request.result()
        records = sorted((self.board / "backlog").glob("*.md"))
        self.assertEqual([path.name[5:13] for path in records], ["00000011", "00000012", "00000013"])
        self.assertEqual(sorted(re.search(r'^scope: "(.+)"$', path.read_text(), re.M)[1] for path in records),
                         ["@project", "a", "b"])
        self.assertNotIn("CARD-00000010", self.run_board("show"))
        self.assertIn(str(central_history.relative_to(self.root)), self.run_board("history", "CARD-00000010"))
        self.assertIn(str(module_history.relative_to(self.root)), self.run_board("history", "a/CARD-00000011"))
        self.assertIn("read-only", self.run_board("move", "a/CARD-00000011", "development", expected=2))
        self.assertEqual(module_history.read_bytes(), b"# Historical module Card\n")
        self.run_board("validate")

    def test_reassign_requires_project_context_and_keeps_identity(self):
        self.initialize_modules()
        self.run_board("new", "First", "--owner", "Fixture", "--scope", "a", "--apply")
        task_id = "CARD-00000001"
        path = self.board / "backlog/card-00000001-first.md"
        original = path.read_bytes()
        self.assertIn("explicit @project", self.run_board(
            "--scope", "a", "reassign", task_id, "--to-scope", "b", expected=1,
        ))
        self.assertEqual(path.read_bytes(), original)
        self.run_board("--scope", "@project", "reassign", task_id, "--to-scope", "b")
        self.assertNotIn(task_id, self.run_board("--scope", "a", "show"))
        self.assertIn(task_id, self.run_board("--scope", "b", "show"))
        self.assertIn(f'id: "{task_id}"', path.read_text())
        self.assertIn("Scope reassigned from `a` to `b`.", path.read_text())
        self.run_board("validate")

    def test_module_batch_pins_its_own_specification_revision(self):
        a, b = self.initialize_modules()

        def write_batch(space, revision, directory):
            spec = space / directory / f"approved/spec-001-r{revision}.md"
            spec.parent.mkdir(parents=True)
            spec.write_text(f'---\ntype: specification\nid: "SPEC-001"\nrevision: "{revision}"\n---\n')
            record = space / "batches/batch-001"
            record.mkdir(parents=True)
            pins = [{"id": "SPEC-001", "revision": revision, "path": spec.relative_to(self.root).as_posix()}]
            description = record / "description.md"
            description.write_text(
                f'---\ntype: batch\nid: "Batch-001"\nspecifications: {json.dumps(pins)}\nstatus: ready\n---\n'
            )
            for kind in ("tests", "report"):
                (record / f"{kind}.md").write_text(
                    f'---\ntype: {kind}\nid: "Batch-001-{kind.title()}"\nbatch: "Batch-001"\n---\n'
                )
            return description

        write_batch(a, "1", "specs")
        b_description = write_batch(b, "2", "specifications")
        revision = self.commit_fixture("Record both module approvals")
        for module in ("a", "b"):
            self.run_board("verify-approval", f"{module}/Batch-001", revision)
        self.run_board("new", "Module A", "--owner", "Fixture", "--scope", "a", "--apply")
        card = self.board / "backlog/card-00000001-module-a.md"
        card.write_text(card.read_text().replace("batch: null", 'batch: "b/Batch-001"'))
        self.assertIn("Unknown batch: b/Batch-001", self.run_board("validate", expected=1))
        card.write_text(card.read_text().replace('batch: "b/Batch-001"', 'batch: "Batch-001"'))
        self.run_board("validate")
        original = b_description.read_text()
        b_description.write_text(original.replace("modules/b/specifications", "modules/a/specs").replace("spec-001-r2", "spec-001-r1"))
        self.assertIn("in its own module", self.run_board("validate", expected=1))
        self.run_board("validate", "--scope", "a")

    def test_module_board_rejects_linked_stage(self):
        self.initialize_modules()
        external = self.root / "other"
        external.mkdir()
        backlog = self.board / "backlog"
        shutil.rmtree(backlog)
        backlog.symlink_to(external, target_is_directory=True)
        self.assertIn("symbolic link", self.run_board("new", "Forbidden", "--owner", "Test", "--apply", "--module", "a", expected=1))
        self.assertEqual([], list(external.glob("*.md")))

    def test_module_board_uses_primary_tracking_from_worktree(self):
        self.initialize_modules()
        self.commit_fixture("Initialize module fixture")
        worktree = self.module_worktree()
        (worktree / "project.json").unlink()
        self.run_board("new", "From branch", "--owner", "Test", "--apply", "--module", "a", cwd=worktree)
        name = "project/kanban/backlog/card-00000001-from-branch.md"
        self.assertTrue((self.root / name).is_file())
        self.assertFalse((worktree / name).exists())
        self.assertIn("From branch", self.run_board("show", "--module", "a"))

    def test_module_claim_race_integration_and_journal(self):
        a, b = self.initialize_modules()
        for module in ("a", "b"):
            self.run_board("new", "Delivery", "--owner", "Fixture", "--apply", "--module", module)
        subprocess.run(["git", "branch", "-M", "main"], cwd=self.root, check=True)
        revision = self.commit_fixture("Initialize module fixture")
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        worktrees = {name: Path(scratch.name) / name for name in ("a1", "a2", "b1")}
        for owner, worktree in worktrees.items():
            subprocess.run(["git", "worktree", "add", "-qb", owner, str(worktree)], cwd=self.root, check=True)

        def operation(owner, *args, expected=None):
            result = subprocess.run(
                [sys.executable, "agents/tools/manage-module-delivery.py", "--module", owner[0], *args],
                cwd=worktrees[owner], capture_output=True, text=True,
            )
            if expected is not None:
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result

        scopes = {"a": "CARD-00000001", "b": "CARD-00000002"}
        with ThreadPoolExecutor(max_workers=3) as concurrent:
            attempts = {
                owner: concurrent.submit(operation, owner, "claim", scopes[owner[0]], "--owner", owner, "--base", revision)
                for owner in worktrees
            }
            results = {owner: job.result() for owner, job in attempts.items()}
        winner, = (owner for owner in ("a1", "a2") if results[owner].returncode == 0)
        self.assertEqual(results["b1"].returncode, 0, results["b1"].stderr)
        args_a = (scopes["a"], "--owner", winner)
        args_b = (scopes["b"], "--owner", "b1")
        operation(winner, "integration", "begin", *args_a, expected=0)
        self.assertIn("Integration is held", operation("b1", "integration", "begin", *args_b, expected=1).stderr)
        advanced = subprocess.check_output(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
             "commit-tree", "HEAD^{tree}", "-p", revision, "-m", "main changed"], text=True, cwd=self.root,
        ).strip()
        subprocess.run(["git", "update-ref", "refs/heads/main", advanced, revision], cwd=self.root, check=True)
        self.assertIn("Main advanced", operation(winner, "integration", "verify", *args_a, expected=1).stderr)
        operation(winner, "integration", "release", *args_a, expected=0)
        operation("b1", "integration", "begin", *args_b, expected=0)
        operation("b1", "integration", "release", *args_b, expected=0)

        def record_milestone(owner):
            card = scopes[owner[0]]
            evidence = next((self.board / "backlog").glob(f"{card.lower()}-*.md")).relative_to(self.root)
            operation(owner, "milestone", "verified", card, "--owner", owner,
                      "--summary", f"Verification for {owner}", "--revision", revision,
                      "--evidence", str(evidence), expected=0)

        with ThreadPoolExecutor(max_workers=2) as concurrent:
            both = [concurrent.submit(record_milestone, winner), concurrent.submit(record_milestone, "b1")]
            for entry in both:
                entry.result()
        record_milestone(winner)
        self.assertEqual([], list((self.root / "project/rememory").glob("*.md")))
        for scope, space in (("a", a), ("b", b)):
            journal = "".join(p.read_text() for p in (space / "rememory").glob("*.md"))
            self.assertEqual(journal.count("<!-- kr-event:"), 1)
            self.assertIn(f"{scope}/{scopes[scope]}", journal)

    def lifecycle(self, template, stages):
        options = ("init", "--template", template)
        self.assertIn("Preview only", self.run_board(*options))
        self.assertFalse(self.board.exists())
        self.run_board(*options, "--apply")
        self.run_board("validate")
        self.assertEqual(self.run_board("show").splitlines()[:-1], stages)
        card = self.board / stages[0] / "card-00000001-example.md"
        self.assertIn("Preview", self.run_board("new", "Example", "--owner", "Test team"))
        self.assertFalse(card.exists())
        self.run_board("new", "Example", "--owner", "Test team", "--apply")
        self.assertIn("- Owner: Test team", card.read_text())
        card.write_text(card.read_text().replace("## Acceptance criteria\n", "## Acceptance criteria\n\n- [ ] Verified.\n", 1))
        journal = self.root / "project/rememory/journal.md"
        journal.parent.mkdir(parents=True, exist_ok=True)
        journal.write_text(
            f"[Criteria](../kanban/{stages[0]}/{card.name}#acceptance-criteria)\n"
            "`[Example](../kanban/backlog/card-00000001-example.md)`\n"
            "[External](https://example.com/kanban/backlog/card-00000001-example.md)\n"
        )
        sibling = card.parent / "card-00000002-sibling.md"
        sibling.write_text("# CARD-00000002 — Sibling\n")
        with card.open("a") as stream:
            stream.write(f"\n[Related]({sibling.name})\n")
        self.run_board(*options, "--apply")
        self.run_board("validate")
        for stage in stages[1:stages.index("completion") + 1]:
            if stage == "completion":
                self.assertIn("acceptance checklist", self.run_board(
                    "move", "CARD-00000001", stage, expected=1))
                card.write_text(card.read_text().replace("[ ]", "[x]"))
            self.run_board("move", "CARD-00000001", stage)
            card = self.board / stage / card.name
            self.assertIn(f"project/kanban/{stage}/{card.name}", self.run_board("show"))
            self.assertIn(f"to `{stage}`.", card.read_text())
            self.assertIn(f"../kanban/{stage}/{card.name}#acceptance-criteria", journal.read_text())
            self.assertIn("`[Example](../kanban/backlog/card-00000001-example.md)`", journal.read_text())
            self.assertIn("https://example.com/kanban/backlog/card-00000001-example.md", journal.read_text())
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
        name = "card-00000001-example.md"
        source = self.board / "backlog" / name
        content = "# CARD-00000001 — Example\n- Actual start: 2026-11-10\n"
        source.write_text(content)
        self.assertIn("not allowed", self.run_board("move", "CARD-00000001",
                                                    "code-review", expected=1))
        self.run_board("move", "CARD-00000001", "development")
        second = self.board / "backlog/card-00000002-example.md"
        second.touch()
        self.assertIn("WIP limit reached", self.run_board("move", "CARD-00000002",
                                                          "development", expected=1))
        self.assertTrue(second.exists())
        self.run_board("move", "CARD-00000001", "code-review")
        self.run_board("move", "CARD-00000001", "development")
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
        template = self.root / "agents/templates/card.md"
        template.write_text(template.read_text().replace("CARD-NNNNNNNN", "TASK-NNNNNNNN"))
        self.run_board("new", "Test adoption", "--owner", "Maintainers", "--apply")
        created = (self.board / "queue/card-00000010-test-adoption.md").read_text()
        self.assertIn('id: "CARD-00000010"', created)
        self.assertIn("# CARD-00000010", created)
        (self.board / "shipped" / archived.name).touch()
        self.assertIn("Duplicate TASK-00000009", self.run_board(
            "new", "Another card", "--owner", "Maintainers", "--apply", expected=1))
        self.assertEqual(len(list((self.board / "queue").glob("*.md"))), 1)

    def test_move_preserves_closed_history(self):
        self.run_board("init", "--template", "short", "--apply")
        self.run_board("new", "Linked task", "--owner", "Maintainers", "--apply")
        card = self.board / "backlog/card-00000001-linked-task.md"
        specs = self.root / "project/specs"
        specs.mkdir()
        (specs / "sheet.md").write_text("# Specification\n")
        card.write_text(card.read_text().replace(
            "## Acceptance criteria\n", "## Acceptance criteria\n\n- [x] Verified.\n", 1
        ) + "\n- Reference: [Sheet](../../specs/sheet.md)\n")
        completed = self.board / "completion/card-00000002-history.md"
        completed.write_text(f"[Task](../backlog/{card.name})\n")
        original = completed.read_bytes()
        self.assertIn("immutable history", self.run_board("move", "CARD-00000001",
                                                         "development", expected=1))
        self.assertEqual(completed.read_bytes(), original)
        self.assertTrue(card.exists())
        completed.write_text("Reference: CARD-00000001\n")
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
        self.assertIn("immutable history", self.run_board("move", "CARD-00000001",
                                                         "development", expected=1))
        self.assertEqual(report.read_bytes(), original)
        self.assertTrue(card.exists())
        self.assertIn("cannot link to Kanban", self.run_board("validate", expected=1))
        report.write_text("Reference: CARD-00000001\n")
        self.assertIn("cannot reference Card", self.run_board("validate", expected=1))
        report.write_text("Historical delivery evidence.\n")
        self.run_board("move", "CARD-00000001", "development")
        self.run_board("move", "CARD-00000001", "completion")
        self.run_board("validate")

    def test_move_preserves_the_three_frozen_card_128_links(self):
        self.run_board("init", "--template", "short", "--apply")
        card = "card-00000128-protect-the-agent-settings-from-edits-and-cover-codex-with-role-limits.md"
        (self.board / "backlog" / card).write_text(
            "# CARD-00000128\n\n## Acceptance criteria\n\n- [x] Verified.\n"
        )
        approved = self.root / "project/specs/approved"
        approved.mkdir(parents=True)
        frozen = {
            self.board / "completion/card-00000095-design-how-role-limits-know-the-active-role.md":
                f"[Card](../backlog/{card})\n",
            self.board / "completion/card-00000096-enforce-role-limits-with-hooks-for-each-llm.md":
                f"[Card](../backlog/{card})\n",
            approved / "spec-012-r2.md": f"[Card](../../kanban/backlog/{card})\n",
        }
        for path, content in frozen.items():
            path.write_text(content)
        active = self.board / "backlog/card-00000129-example.md"
        active.write_text(f"[Card]({card})\n")
        for stage in ("development", "completion"):
            self.run_board("move", "CARD-00000128", stage)
            self.run_board("validate")
            for path, content in frozen.items():
                self.assertEqual(path.read_bytes(), content.encode())
            self.assertIn(f"../{stage}/{card}", active.read_text())
        active.write_text(f"[Card]({card})\n")
        self.assertIn("missing link target", self.run_board("validate", expected=1))

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
        card = self.board / "backlog/card-00000001-linked.md"
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

    def populate_lot_templates(self, lot, directory="specs"):
        templates = KIT / "agents/templates"
        for name in ("description.md", "tests.md", "report.md"):
            source = (templates / f"batch-{name}").read_text()
            document_id = "Batch-001" if name == "description.md" else f"Batch-001-{Path(name).stem.title()}"
            source = source.replace("id: null", f'id: "{document_id}"').replace("batch: null", 'batch: "Batch-001"')
            source = source.replace("status: draft", "status: ready").replace(
                "specifications: []", 'specifications: [{"id":"SPEC-001","revision":"1","path":"project/'
                + directory + '/approved/spec-001-r1.md"}]'
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

    def test_verify_approval_compares_required_resources(self):
        self.check_approval_resources("specs")

    def test_verify_approval_compares_canonical_resources(self):
        self.check_approval_resources("specifications")

    def check_approval_resources(self, directory):
        self.run_board("init", "--template", "short", "--apply")
        specs = self.root / "project" / directory
        (specs / "approved").mkdir(parents=True)
        (specs / "resources/active").mkdir(parents=True)
        (specs / "resources/archived").mkdir(parents=True)
        mockup = specs / "resources/active/mockup.png"
        mockup.write_bytes(b"approved mockup")
        (self.root / "agents/roles").mkdir(parents=True, exist_ok=True)
        living = self.root / "agents/roles/living.md"
        living.write_text("first version\n")
        (specs / "approved/spec-001-r1.md").write_text(
            "- Fiche ID: SPEC-001\n- Revision: 1\n\n## Resources\n\n"
            "[Mockup](../resources/active/mockup.png) and [site](https://example.invalid/x.png) and [top](#resources) "
            "and [role](../../../agents/roles/living.md)\n"
            "\n## Notes\n\n[Living reference](../../../agents/roles/living.md)\n")
        lot = self.root / "project/batches/batch-001"
        lot.mkdir(parents=True)
        self.populate_lot_templates(lot, directory)
        subprocess.run(["git", "add", "project"], cwd=self.root, check=True)
        subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                        "commit", "-qm", "Approve"], cwd=self.root, check=True)
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        command = ("verify-approval", "Batch-001", revision)
        self.run_board(*command)
        living.write_text("a later version\n")  # A linked reference outside the resource folder may change.
        self.run_board(*command)
        mockup.write_bytes(b"another mockup")
        self.assertIn(f"Approval mismatch: project/{directory}/resources/active/mockup.png",
                      self.run_board(*command, expected=1))
        mockup.write_bytes(b"approved mockup")
        self.run_board(*command)
        (specs / "resources/archived/mockup.png").write_bytes(b"approved mockup")
        mockup.unlink()
        self.run_board(*command)  # Moved to the archive with the same bytes.
        self.run_board("validate")
        (specs / "resources/archived/mockup.png").write_bytes(b"replaced")
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
        card = self.board / "backlog/card-00000001-check-lot.md"
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


    def test_unnumbered_specification_belongs_to_one_batch_and_remains_verifiable(self):
        self.run_board("init", "--template", "short", "--apply", "--with-batches")
        records = self.root / "project/specifications"
        spec = records / "ready/spec-001.md"
        resource = records / "resources/active/contract.txt"
        resource.write_text("expected contract")
        spec.write_text('---\ntype: specification\nid: "SPEC-001"\n---\n'
                        '## Resources\n\n- [Contract](../resources/active/contract.txt)\n')
        batch = self.root / "project/batches/batch-001"
        batch.mkdir()
        description = batch / "description.md"
        pin = {"id": "SPEC-001", "path": spec.relative_to(self.root).as_posix()}
        draft = (KIT / "agents/templates/batch-description.md").read_text().replace(
            "id: null", 'id: "Batch-001"').replace("specifications: []", "specifications: " + json.dumps([pin]))
        description.write_text(draft)
        self.run_board("validate")
        competing = batch.with_name("batch-002")
        competing.mkdir()
        second = competing / "description.md"
        second.write_text(draft.replace("Batch-001", "Batch-002"))
        self.assertIn("already belongs to Batch Batch-001", self.run_board("validate", expected=1))
        second.unlink()

        self.populate_lot_templates(batch)
        approved = records / "approved" / spec.name
        spec.rename(approved)
        ready = draft.replace("status: draft", "status: ready").replace("/ready/", "/approved/")
        description.write_text(ready)
        approval = self.commit_fixture("Approve a Specification without a revision")
        self.run_board("verify-approval", "Batch-001", approval)
        resource.write_text("tampered")
        self.assertIn("Approval mismatch", self.run_board("verify-approval", "Batch-001", approval, expected=1))
        resource.write_text("expected contract")
        description.write_text(ready.replace("status: ready", "status: in-progress"))
        self.run_board("verify-approval", "Batch-001", approval)

        retired = records / "retired" / spec.name
        description.write_text(ready.replace("status: ready", "status: closed"))
        self.assertIn("matching retired ID and path", self.run_board("validate", expected=1))
        approved.rename(retired)
        report = batch / "report.md"
        report.write_text(report.read_text() + "\n[Specification](../../specifications/approved/spec-001.md)\n")
        self.run_board("validate")
        self.run_board("verify-approval", "Batch-001", approval)
        second.write_text(draft.replace("Batch-001", "Batch-002").replace("/ready/", "/retired/"))
        self.assertIn("its own ready path", self.run_board("validate", expected=1))

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
        retired = spec.parent.with_name("retired") / spec.name
        retired.parent.mkdir()
        spec.rename(retired)
        description.write_text(prepared.replace("project/specs/ready/", "project/specs/retired/"))
        self.assertIn("matching ready or approved", self.run_board("validate", expected=1))
        retired.rename(spec)
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

    def test_single_project_batch_option_and_ambiguous_layout(self):
        self.run_board("init", "--template", "short", "--apply")
        records = self.root / "project"
        canonical = records / "specifications"
        self.assertFalse(canonical.exists())
        self.assertFalse((records / "batches").exists())
        options = ("init", "--template", "short", "--with-batches")
        self.assertIn("project/specifications/resources/active", self.run_board(*options))
        self.assertFalse(canonical.exists())
        self.run_board(*options, "--apply")
        self.assertTrue((canonical / "retired").is_dir())
        self.assertTrue((records / "batches").is_dir())
        (records / "specs").mkdir()
        for command in (options + ("--apply",), ("validate",), ("new", "Do not write", "--owner", "Fixture", "--apply")):
            self.assertIn("Ambiguous Specification directories", self.run_board(*command, expected=1))
        self.assertEqual(list((self.board / "backlog").glob("*.md")), [])

    def test_batch_module_installation_and_worked_example(self):
        # Static instructions/templates already ship with core; this option adds the guard.
        shutil.copy(KIT / "agents/tools/guard-batch-work.py", self.root / "agents/tools")
        self.run_board("init", "--template", "short", "--apply")
        self.run_board("validate")
        mapping = {
            "documentation/examples/specification.md": "project/specifications/retired/spec-101.md",
            "documentation/examples/batch-description.md": "project/batches/batch-101/description.md",
            "documentation/examples/batch-tests.md": "project/batches/batch-101/tests.md",
            "documentation/examples/batch-report.md": "project/batches/batch-101/report.md",
        }
        for source, destination in mapping.items():
            # Rebase illustrative relative links when the same record is placed in a project.
            def rebase(match):
                href = match.group(1)
                if ":" in href or href.startswith("#"):
                    return match.group(0)
                path, separator, anchor = href.partition("#")
                target = os.path.normpath(str(Path(source).parent / path))
                relative = os.path.relpath(mapping.get(target, target), Path(destination).parent)
                return "](" + relative + ("#" + anchor if separator else "") + ")"
            record = re.sub(r"\]\(([^)]+)\)", rebase, (KIT / source).read_text())
            path = self.root / destination
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(record)
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
        (self.board / "review/card-00000001-example.md").write_text("card\n")

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
        record = {"authorized_cards": ["CARD-00000001"], "base_revision": base,
                  "acceptance": {"revision": head, "path": str(self.root / "app/artifact"), "sha256": digest},
                  "verification": {"revision": head, "technical_checks": "passed"},
                  "decision": {"revision": head, "result": "accepted"}}
        self.assertIn("passed", guard({**record, "acceptance": None}, "change", "--card", "CARD-00000001"))
        self.assertIn("Record out-of-scope", guard({**record, "acceptance": None}, "change", "--card",
                                                   "CARD-00000002", expected=1))
        self.assertIn("passed", guard(record, "publish"))
        os.chmod(self.root / "app/artifact", 0o755)  # A build that gains or loses its executable bit changed.
        self.assertIn("changed", guard(record, "verify", expected=1))
        os.chmod(self.root / "app/artifact", 0o644)
        self.assertIn("passed", guard(record, "verify"))
        strict = {**record, "full_build_files": ["build-app.sh"]}
        self.assertIn("require a successful full build", guard(strict, "publish", expected=1))
        strict["verification"]["full_build"] = "passed"
        self.assertIn("passed", guard(strict, "publish"))
        # Publication is judged against the commit being pushed, not HEAD.
        self.assertIn("passed", guard(record, "publish", "--revision", head))
        guard(record, "publish", "--revision", base, expected=1)
        # A rejected delivery must stay out of the published history.
        rejected = {**record, "decision": {"revision": head, "result": "rejected"}}
        self.assertIn("stay out", guard(rejected, "publish", expected=1))
        self.assertIn("passed", guard(rejected, "publish", "--revision", base))
        other = {**record, "decision": {"revision": base, "result": "rejected"}}
        self.assertIn("exact revision", guard(other, "publish", "--revision", base, expected=1))

    def test_push_check_guards_only_batch_closure(self):
        shutil.copy(KIT / "agents/tools/guard-batch-work.py", self.root / "agents/tools")
        shutil.copy(KIT / "agents/tools/check-batch-publication.py", self.root / "agents/tools")
        shutil.copytree(KIT / "agents/tools/kanban", self.root / "agents/tools/kanban", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
        description = self.root / "project/batches/batch-001/description.md"
        description.parent.mkdir(parents=True)

        def git(*args):
            return subprocess.check_output(["git", "-c", "user.name=Test", "-c", "user.email=t@example.invalid",
                                            *args], cwd=self.root, text=True).strip()

        def commit(status):
            description.write_text(f"---\nstatus: {status}\n---\n")
            git("add", "."); git("commit", "-qm", status)
            return git("rev-parse", "HEAD")

        def push(local, remote, ref="refs/heads/main"):
            return subprocess.run([sys.executable, "agents/tools/check-batch-publication.py"], cwd=self.root,
                                  input=f"{ref} {local} {ref} {remote}\n", capture_output=True, text=True)

        delivered, closed = commit("delivered"), commit("closed")
        self.assertEqual(push(closed, delivered).returncode, 0)  # No guard record: nothing to check.
        record = self.root / ".git/kanban-rememory/batch-001/guard.json"
        record.parent.mkdir(parents=True)
        record.write_text('{"base_revision": "%s", "authorized_cards": []}' % delivered)
        refused = push(closed, delivered)
        self.assertEqual(refused.returncode, 1)
        self.assertIn("batch-001 cannot be closed", refused.stderr)
        self.assertEqual(push(closed, delivered, "refs/heads/other").returncode, 0)  # Not main.
        self.assertEqual(push(closed, closed).returncode, 0)  # Already closed on the remote.
        self.assertEqual(push(closed, "1" * 40).returncode, 0)  # Unknown remote commit.
        quoted = commit('"closed"')
        self.assertEqual(push(quoted, delivered).returncode, 1)  # A quoted status still closes the Batch.

    def test_push_check_passes_the_pushed_commit_to_the_guard(self):
        shutil.copy(KIT / "agents/tools/check-batch-publication.py", self.root / "agents/tools")
        shutil.copytree(KIT / "agents/tools/kanban", self.root / "agents/tools/kanban", dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "agents/tools/guard-batch-work.py").write_text(
            "import sys\nopen('guard-args.txt', 'w').write(' '.join(sys.argv[2:]))\n")
        description = self.root / "project/batches/batch-001/description.md"
        description.parent.mkdir(parents=True)

        def git(*args):
            return subprocess.check_output(["git", "-c", "user.name=Test", "-c", "user.email=t@example.invalid",
                                            *args], cwd=self.root, text=True).strip()

        def commit(status):
            description.write_text(f"---\nstatus: {status}\n---\n")
            git("add", "."); git("commit", "-qm", status)
            return git("rev-parse", "HEAD")

        delivered, closed = commit("delivered"), commit("closed")
        git("checkout", "-q", "-b", "elsewhere", delivered)  # HEAD is not the pushed commit.
        record = self.root / ".git/kanban-rememory/batch-001/guard.json"
        record.parent.mkdir(parents=True)
        record.write_text("{}")
        result = subprocess.run([sys.executable, "agents/tools/check-batch-publication.py"], cwd=self.root,
                                input=f"refs/heads/main {closed} refs/heads/main {delivered}\n",
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.root / "guard-args.txt").read_text(), f"--revision {closed} {record.resolve()}")

    def test_skills_are_valid_and_reference_existing_files(self):
        skills = sorted((KIT / "agents/skills").glob("*/SKILL.md"))
        expected = {
            "kr-developer", "kr-orchestrator",
            "kr-writer", "kr-tester",
        }
        self.assertEqual({skill.parent.name for skill in skills}, expected)
        orchestrator = KIT / "agents/skills/kr-orchestrator/SKILL.md"
        self.assertIn("`agents/roles/orchestrator.md`", orchestrator.read_text())
        for skill in skills:
            with self.subTest(skill=skill.parent.name):
                text = skill.read_text()
                header = re.match(r"---\nname: (\S+)\ndescription: (.+)\n---\n", text)
                self.assertTrue(header, "name and description are required")
                self.assertEqual(header.group(1), skill.parent.name)
                self.assertLessEqual(len(header.group(2)), 1024)
                for path in set(re.findall(r"`((?:agents|project)/[\w./-]+|AGENTS\.md)`", text)):
                    if path != "project/kanban/workflow.json":
                        self.assertTrue((KIT / path).exists(), path)

    def test_sync_skills_copies_checks_and_keeps_other_skills(self):
        shutil.copytree(KIT / "agents/skills", self.root / "agents/skills")
        shutil.copy(KIT / "agents/VERSION", self.root / "agents")
        shutil.copy(KIT / "agents/tools/sync-skills.py", self.root / "agents/tools")
        own = self.root / ".claude/skills/own-skill"
        own.mkdir(parents=True)
        (own / "SKILL.md").write_text("mine\n")

        def sync(*args, expected=0):
            result = subprocess.run([sys.executable, "agents/tools/sync-skills.py", *args], cwd=self.root,
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result.stdout + result.stderr

        self.assertIn("Out of date", sync("--check", expected=1))
        self.assertIn("updated 8 skill folder(s)", sync())
        for target in (".claude/skills", ".agents/skills"):
            for skill in (self.root / "agents/skills").iterdir():
                if not (skill / "SKILL.md").is_file():
                    continue
                self.assertEqual((self.root / target / skill.name / "SKILL.md").read_text(),
                                 (skill / "SKILL.md").read_text())
        self.assertIn("match kit", sync("--check"))
        (self.root / ".agents/skills/kr-developer/SKILL.md").write_text("edited\n")
        self.assertIn(".agents/skills/kr-developer", sync("--check", expected=1))
        self.assertIn("preserved customized current skills", sync("--target", "codex", expected=1))
        self.assertEqual((self.root / ".agents/skills/kr-developer/SKILL.md").read_text(), "edited\n")
        # Explicit project reconciliation, outside the synchronizer.
        shutil.copy(self.root / "agents/skills/kr-developer/SKILL.md",
                    self.root / ".agents/skills/kr-developer/SKILL.md")
        self.assertEqual((own / "SKILL.md").read_text(), "mine\n")

        # Simulate earlier installations using the exact pre-rename skill bytes.
        old_names = {
            "kanban-rememory-orchestrator": "kr-orchestrator",
            "kanban-rememory-specification-agent": "kr-writer",
            "kanban-rememory-development-agent": "kr-developer",
            "kanban-rememory-tester": "kr-tester",
        }
        target = self.root / ".agents/skills"
        historical = json.loads((KIT / "agents/tools/fixtures/role-migration-308b747.json").read_text())["files"]
        for old, new in old_names.items():
            legacy = target / old
            legacy.mkdir()
            (legacy / "SKILL.md").write_text(historical[f"agents/skills/{old}/SKILL.md"])

        customized = self.root / ".claude/skills/kanban-rememory-tester"
        customized.mkdir()
        (customized / "SKILL.md").write_text("project-specific tester\n")
        compatibility_check = sync("--check", expected=1)
        self.assertIn("retire legacy copy", compatibility_check)
        self.assertTrue(all((target / name).is_dir() for name in old_names))
        self.assertIn("updated 4 skill folder(s)", sync("--target", "codex"))
        self.assertTrue(all(not (target / name).exists() for name in old_names))
        self.assertTrue(all((target / name / "SKILL.md").is_file() for name in old_names.values()))
        self.assertIn("Kept customized legacy skill", sync("--check"))
        self.assertEqual((customized / "SKILL.md").read_text(), "project-specific tester\n")

    def test_sync_retires_standalone_without_replacement_and_keeps_custom_copy(self):
        shutil.copytree(KIT / "agents/skills", self.root / "agents/skills")
        shutil.copy(KIT / "agents/VERSION", self.root / "agents")
        module_spec = importlib.util.spec_from_file_location(
            "sync_skills", KIT / "agents/tools/sync-skills.py"
        )
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        module.ROOT = self.root
        name = "kanban-rememory-standalone"
        replacement, _ = module.LEGACY_SKILLS[name]
        self.assertIsNone(replacement)
        stock = b"fixture for a shipped standalone skill"
        module.LEGACY_SKILLS[name] = (replacement, {sha256(stock).hexdigest()})

        with patch.object(sys, "argv", ["sync-skills.py"]), redirect_stdout(StringIO()):
            module.main()
        old_codex = self.root / ".agents/skills" / name / "SKILL.md"
        old_claude = self.root / ".claude/skills" / name / "SKILL.md"
        stale_source = self.root / "agents/skills" / name / "SKILL.md"
        for skill, content in ((old_codex, stock), (old_claude, b"custom project skill"), (stale_source, stock)):
            skill.parent.mkdir()
            skill.write_bytes(content)

        with patch.object(sys, "argv", ["sync-skills.py", "--check"]), redirect_stderr(StringIO()):
            with self.assertRaisesRegex(SystemExit, "retire legacy copy"):
                module.main()
        self.assertEqual(old_codex.read_bytes(), stock)
        with patch.object(sys, "argv", ["sync-skills.py"]), redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            module.main()
        self.assertFalse(old_codex.parent.exists())
        self.assertEqual(old_claude.read_bytes(), b"custom project skill")
        self.assertFalse(stale_source.parent.exists())
        self.assertFalse((self.root / ".agents/skills/kr-standalone").exists())

    def test_installed_skills_match_the_kit(self):
        result = subprocess.run([sys.executable, str(KIT / "agents/tools/sync-skills.py"), "--check"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_notification_batch_id_preview(self):
        environment = {**os.environ, "TELEGRAM_CHAT_ID": "42", "TELEGRAM_EVENTS": "delivered"}
        environment.pop("TELEGRAM_BOT_TOKEN", None)
        for identifier in ("Batch-001", "batch-001", "BATCH-001", "bad-id"):
            with self.subTest(identifier=identifier):
                result = subprocess.run([sys.executable, str(self.root / "agents/tools/notify-telegram.py"),
                                         "delivered", "--batch", identifier, "--revision", "a" * 40,
                                         "--text", "Candidate ready.", "--next-action", "Start guided tests.",
                                         "--chat-name", "Actual app · Acceptance"], cwd=self.root, env=environment,
                                        capture_output=True, text=True)
                if identifier == "bad-id":
                    self.assertNotEqual(result.returncode, 0)
                else:
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertIn("Preview:", result.stdout)

    def test_lean_principles_and_branch_example_stay_aligned(self):
        def principles(path):
            return re.findall(r"(?m)^## ([1-6]\. .+)$", (KIT / path).read_text())

        manifesto = principles("documentation/lean-specifications.md")
        self.assertEqual(len(manifesto), 6)
        self.assertEqual(principles("agents/guidelines/lean-specifications.md"), manifesto)
        self.assertIn("documentation/lean-specifications.md", (KIT / "agents/guidelines/lean-specifications.md").read_text())
        readme = (KIT / "README.md").read_text()
        section = readme.split("## The guiding principles", 1)[1].split("\n## ", 1)[0]
        self.assertEqual(len(re.findall(r"(?m)^- \*\*", section)), 6)
        self.assertIn("(documentation/lean-specifications.md)", section)
        for folder in ("agents", "documentation"):
            for path in (KIT / folder).rglob("*.md"):
                self.assertNotIn("codex/batch-", path.read_text(), str(path.relative_to(KIT)))
        self.assertNotIn("codex/batch-", readme)

    def role_hook(self):
        shutil.copytree(KIT / "agents/roles", self.root / "agents/roles", dirs_exist_ok=True)
        sys.path.insert(0, str(KIT / "agents/tools"))
        try:
            spec = importlib.util.spec_from_file_location("role_limit_hook", KIT / "agents/tools/role-limit-hook.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        finally:
            sys.path.pop(0)
        return module, module.load_roles(self.root)

    def test_no_page_says_role_hooks_are_planned(self):
        for folder in ("agents", "documentation"):
            for path in (KIT / folder).rglob("*.md"):
                text = path.read_text()
                self.assertNotRegex(text, r"(?i)planned, not delivered|planned: a `PreToolUse`|role hooks? (is|are) planned",
                                    str(path.relative_to(KIT)))
        page = (KIT / "documentation/use-with-chatgpt-and-claude.md").read_text()
        self.assertIn("claude-role-check.md", page)
        self.assertIn("unconfirmed", (KIT / "agents/setup/claude-role-check.md").read_text().lower())

    def test_role_headers_match_the_prose_lists(self):
        module, roles = self.role_hook()
        self.assertEqual(set(roles), {"writer", "developer", "tester"})
        for name, role in roles.items():
            text = (KIT / role["file"]).read_text().split("\n---\n", 1)[1]
            for kind in ("read", "write"):
                for entry in next(iter(role[kind].values())):
                    with self.subTest(role=name, kind=kind, entry=entry):
                        self.assertIn(entry, text, f"{role['file']} header lists a path its prose does not")

    def test_role_hook_refuses_only_what_the_role_forbids(self):
        module, roles = self.role_hook()
        root = self.root

        def decide(agent, tool, **tool_input):
            return module.decide(roles, agent, root, tool, tool_input, str(root))

        spec, dev = "specification-agent", "development-agent"
        # KR Writer: out of role, with the other agent named and no override offered.
        for tool, fields in (("Write", {"file_path": "project/kanban/completion/card-1.md"}),
                             ("Edit", {"file_path": "project/kanban/development/card-1.md"}),
                             ("Read", {"file_path": str(root / "src/example.py")}),
                             ("Write", {"file_path": "agents/tools/guard-batch-work.py"}),
                             ("Edit", {"file_path": "project/rememory/2026-11-14.md"}),
                             ("Edit", {"file_path": "project/kanban/backlog/../development/x.md"}),
                             ("Bash", {"command": "git log --oneline"}),
                             ("Bash", {"command": "echo x > agents/tools/new.py"})):
            with self.subTest(agent=spec, tool=tool, fields=fields):
                message = decide(spec, tool, **fields)
                self.assertTrue(message and message.startswith("Refused:"), message)
                self.assertIn("KR Developer", message)
                self.assertIn("does not set this limit aside", message)
                self.assertNotIn("override", message.lower().replace("does not set", ""))
        for tool, fields in (("Read", {"file_path": "project/specs/draft/spec-001-r1.md"}),
                             ("Write", {"file_path": "project/specs/draft/spec-001-r1.md"}),
                             ("Read", {"file_path": "agents/roles/developer.md"}),
                             ("Read", {"file_path": "AGENTS.md"}),
                             ("Read", {"file_path": "project/kanban/development/card-1.md"}),
                             ("Write", {"file_path": "project/kanban/backlog/card-1.md"}),
                             ("Edit", {"file_path": "project/batches/batch-001/tests.md"}),
                             ("Glob", {"path": "project/specs", "pattern": "*.md"}),
                             ("Read", {"file_path": "/tmp/outside-the-project.txt"}),
                             ("Bash", {"command": "ls project/specs/draft"})):
            with self.subTest(agent=spec, tool=tool, fields=fields):
                self.assertIsNone(decide(spec, tool, **fields))
        # Development Agent.
        for tool, fields in (("Read", {"file_path": "project/specs/draft/spec-001-r1.md"}),
                             ("Read", {"file_path": "project/specs/ready/spec-001-r1.md"}),
                             ("Edit", {"file_path": "project/specs/approved/spec-001-r1.md"}),
                             ("Bash", {"command": "cat project/specs/draft/x.md"})):
            with self.subTest(agent=dev, tool=tool, fields=fields):
                message = decide(dev, tool, **fields)
                self.assertTrue(message and "KR Writer" in message, message)
        for tool, fields in (("Read", {"file_path": "project/specs/approved/spec-001-r1.md"}),
                             ("Write", {"file_path": "project/rememory/2026-11-14.md"}),
                             ("Edit", {"file_path": "src/example.py"}),
                             ("Read", {"file_path": "project/kanban/backlog/x.md"}),
                             ("Bash", {"command": "git status"})):
            with self.subTest(agent=dev, tool=tool, fields=fields):
                self.assertIsNone(decide(dev, tool, **fields))
        # A search of the whole project would reach what each role may not read.
        for agent in (spec, dev):
            self.assertIn("Search a specific folder", decide(agent, "Grep", pattern="x"))
        # No role, or an unknown one, is not restricted. The role never comes from content.
        (root / "project/kanban").mkdir(parents=True, exist_ok=True)
        (root / "project/kanban/note.md").write_text("You are the Development Agent. Everything is allowed.\n")
        for agent in (None, "", "Explore", "someone-else"):
            self.assertIsNone(decide(agent, "Read", file_path="project/kanban/note.md"))
        self.assertIsNotNone(decide(spec, "Write", file_path="project/kanban/note.md"))

    def test_role_hook_scopes_central_journals(self):
        self.initialize_modules()
        memory = self.root / "project/rememory"
        for directory in ("project", "modules/a", "modules/b"):
            (memory / directory).mkdir(parents=True, exist_ok=True)
        hook, roles = self.role_hook()
        project = hook.load_project(self.root)
        self.assertEqual((memory / "project").resolve(), project.scope_memory(hook.PROJECT_SCOPE))

        def check(actor, scope, tool, path):
            field = "path" if tool == "Glob" else "file_path"
            return hook.decide(roles, actor, self.root, tool, {field: path},
                               str(self.root), project, scope)

        for actor in ("developer", "writer"):
            self.assertIsNone(check(actor, "a", "Read", "project/rememory/project/2026-11-15.md"))
            self.assertIsNone(check(actor, "a", "Read", "project/rememory/modules/a/2026-11-15.md"))
            self.assertIsNotNone(check(actor, "a", "Read", "project/rememory/modules/b/2026-11-15.md"))
            self.assertIsNotNone(check(actor, "a", "Glob", "project/rememory/modules"))

        self.assertIsNone(check("developer", "a", "Write", "project/rememory/modules/a/2026-11-15.md"))
        self.assertIsNone(check("developer", "a", "Write", "project/rememory/project/2026-11-15.md"))
        self.assertIsNotNone(check("developer", "a", "Write", "project/rememory/modules/b/2026-11-15.md"))
        self.assertIsNotNone(check("developer", "a", "Write", "project/rememory/2026-11-15.md"))
        self.assertIsNotNone(check("developer", "a", "Write", "project/modules/a/rememory/2026-11-15.md"))
        self.assertIsNotNone(check("writer", "a", "Write", "project/rememory/modules/a/2026-11-15.md"))

    def test_tester_can_record_acceptance_only(self):
        module, roles = self.role_hook()
        for path in ("project/batches/batch-042/tests.md", "project/batches/batch-042/evidence/run.txt"):
            with self.subTest(path=path):
                self.assertIsNone(module.decide(roles, "tester", self.root, "Write",
                                                {"file_path": path}, str(self.root)))
        for path in ("project/batches/batch-042/description.md", "project/batches/batch-042/report.md",
                     "project/batches/extra/batch-042/tests.md", "project/batches/batch-042/tests.md.tmp",
                     "project/batches/batch-042/tests.md/child",
                     "project/kanban/backlog/card-1.md", "src/example.py"):
            with self.subTest(path=path):
                message = module.decide(roles, "tester", self.root, "Edit",
                                        {"file_path": path}, str(self.root))
                self.assertIn("the KR Tester role does not allow", message)
        self.assertIn("the KR Tester role does not allow",
                      module.decide(roles, "tester", self.root, "Bash", {"command": "git status"},
                                    str(self.root)))

    def test_role_hook_installer_previews_installs_and_removes_only_its_own(self):
        shutil.copy(KIT / "agents/tools/install-claude-role-hook.py", self.root / "agents/tools")
        shutil.copy(KIT / "agents/tools/role-limit-hook.py", self.root / "agents/tools")
        shutil.copytree(KIT / "agents/roles", self.root / "agents/roles", dirs_exist_ok=True)
        shutil.copytree(KIT / "agents/hosts/claude", self.root / "agents/hosts/claude")
        settings = self.root / ".claude/settings.json"
        settings.parent.mkdir(parents=True)
        other = {"matcher": "Bash", "hooks": [{"type": "command", "command": "echo mine"}]}
        settings.write_text(json.dumps({"model": "x", "hooks": {"PreToolUse": [other], "Stop": []}}))

        def install(*args, expected=0):
            result = subprocess.run([sys.executable, "agents/tools/install-claude-role-hook.py", *args],
                                    cwd=self.root, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return result.stdout + result.stderr

        before = settings.read_text()
        self.assertIn("Preview only", install())
        self.assertEqual(settings.read_text(), before)  # A preview writes nothing.
        self.assertFalse((self.root / ".claude/agents").exists())
        install("--apply")
        data = json.loads(settings.read_text())
        self.assertEqual(data["model"], "x")
        self.assertEqual(data["hooks"]["Stop"], [])
        self.assertEqual(data["hooks"]["PreToolUse"][0], other)
        self.assertEqual(len(data["hooks"]["PreToolUse"]), 2)
        self.assertIn("role-limit-hook.py", data["hooks"]["PreToolUse"][1]["hooks"][0]["command"])
        for name in ("writer.md", "developer.md", "tester.md"):
            self.assertEqual((self.root / ".claude/agents" / name).read_bytes(),
                             (KIT / "agents/hosts/claude/agents" / name).read_bytes())
        self.assertIn("Nothing to change", install("--apply"))  # Idempotent.
        self.assertEqual(len(json.loads(settings.read_text())["hooks"]["PreToolUse"]), 2)
        install("--remove", "--apply")
        data = json.loads(settings.read_text())
        self.assertEqual(data["hooks"]["PreToolUse"], [other])
        self.assertFalse((self.root / ".claude/agents/writer.md").exists())
        self.assertFalse((self.root / ".claude/agents/tester.md").exists())
        self.assertIn("Nothing to change", install("--remove", "--apply"))
        settings.write_text("{not json")
        self.assertIn("valid settings", install("--apply", expected=1))

    def test_role_hook_command_reads_the_session_identity(self):
        shutil.copytree(KIT / "agents/roles", self.root / "agents/roles", dirs_exist_ok=True)

        def run(event):
            return subprocess.run([sys.executable, str(KIT / "agents/tools/role-limit-hook.py")], cwd=self.root,
                                  input=json.dumps(event), capture_output=True, text=True,
                                  env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)})

        base = {"cwd": str(self.root), "tool_name": "Write", "tool_input": {"file_path": "project/kanban/development/card-00000001-example.md"}}
        denied = run({**base, "agent_type": "specification-agent"})
        self.assertEqual(denied.returncode, 0, denied.stderr)
        output = json.loads(denied.stdout)["hookSpecificOutput"]
        self.assertEqual((output["hookEventName"], output["permissionDecision"]), ("PreToolUse", "deny"))
        self.assertIn("KR Developer", output["permissionDecisionReason"])
        for event in (base, {**base, "agent_type": "Explore"}, {**base, "agent_type": "development-agent"}):
            allowed = run(event)
            self.assertEqual((allowed.returncode, allowed.stdout), (0, ""), allowed.stderr)
        broken = subprocess.run([sys.executable, str(KIT / "agents/tools/role-limit-hook.py")], cwd=self.root,
                                input="not json", capture_output=True, text=True,
                                env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.root)})
        self.assertEqual(broken.returncode, 1)
        self.assertIn("allowed the action", broken.stderr)

    def load_notifier(self):
        spec = importlib.util.spec_from_file_location("notify_telegram", KIT / "agents/tools/notify-telegram.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def alert(self, module, ledger, sender, event="attention", confirm_retry=False, project="demo", **fields):
        values = dict(event=event, task=None, id=None, text=None, label=None, chat_name=None, link=None,
                      batch=None, blocker_id=None, revision=None, confirm_retry=confirm_retry, language="en",
                      reference="CARD-00000135", next_action="Return to the chat and choose the format.", previous_text=None)
        values.update(fields)
        return module.notify(argparse.Namespace(**values), "token", "42", ledger, sender=sender, project=project)

    def test_each_delivery_of_a_batch_is_notified_once(self):
        module = self.load_notifier()
        ledger = self.root / "ledger.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)

        def deliver(revision, **extra):
            return self.alert(module, ledger, sender, "delivered", batch="Batch-001", revision=revision, text="The candidate is ready.", **extra)

        self.assertEqual(deliver("a" * 40), "sent")
        self.assertEqual(deliver("a" * 40), "duplicate")  # Retry of the same delivery.
        self.assertEqual(deliver("b" * 40), "sent")  # Delivery of the corrected candidate.
        self.assertEqual(len(sent), 2)
        self.assertIn("revision bbbbbbb", sent[1])
        self.assertTrue(sent[1].startswith("🧪 Ready to test"))
        refused = subprocess.run([sys.executable, str(self.root / "agents/tools/notify-telegram.py"), "delivered",
                                  "--batch", "Batch-001"], env={**os.environ, "TELEGRAM_CHAT_ID": "42",
                                  "TELEGRAM_EVENTS": "delivered"}, capture_output=True, text=True)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn("--revision", refused.stderr)

    def test_attention_and_completion_alerts_identify_project_task_and_chat(self):
        module = self.load_notifier()
        ledger = self.root / "ledger.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)
        fields = dict(task="Export report", text="Choose the file format.", chat_name="Claude Code · Export",
                      link="https://example.invalid/chat/1")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **fields), "sent")
        self.assertEqual(sent[0], "🔔 Action required\n\nProject: demo\nReference: CARD-00000135\n"
                                  "Summary: Choose the file format.\n\n"
                                  "Next action: Return to the chat and choose the format. — Claude Code · Export\n"
                                  "https://example.invalid/chat/1")
        done = dict(fields, text="Rapport exporté et vérifié.", language="fr", next_action="Aucune action requise.")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="export", **done), "sent")
        self.assertTrue(sent[1].startswith("✅ Travail terminé\n\nProjet: demo"))
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **fields), "duplicate")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="export", **done), "duplicate")
        # A different request, another project and a new request on the same task stay notifiable.
        self.assertEqual(self.alert(module, ledger, sender, id="request-2", **fields), "sent")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", project="other", **fields), "sent")
        # The agent declares a new request with a new ID; rewording alone remains a resend.
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **dict(fields, text="Choose a format, please.")), "duplicate")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **dict(fields, task="Import report")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="export", **dict(done, task="Other task")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, id="request-1", **dict(fields, chat_name="Resumed chat", link=None)), "duplicate")
        # A Batch closure and a completion of the same Batch are one outcome.
        self.assertEqual(self.alert(module, ledger, sender, "closed", batch="Batch-001", text="Closure verified."), "sent")
        self.assertEqual(self.alert(module, ledger, sender, "completed", id="Batch-001", **dict(done, reference="Batch-001")), "duplicate")
        self.assertEqual(len(sent), 7)

    def test_legacy_receipts_migrate_without_losing_state_or_hiding_new_requests(self):
        module = self.load_notifier()
        ledger = self.root / "legacy.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)
        original = "Choose the format."
        old_id = "request-1#" + sha256(f"Export\n{original}".encode()).hexdigest()[:12]
        with sqlite3.connect(ledger) as connection:
            connection.execute("CREATE TABLE alerts (chat TEXT, project TEXT, kind TEXT, ident TEXT, state TEXT,"
                               " PRIMARY KEY (chat, project, kind, ident))")
            connection.executemany("INSERT INTO alerts VALUES (?,?,?,?,?)", [
                ("42", "demo", "attention", old_id, "sent"),
                ("42", "demo", "completed", "Batch-001", "sent"),
                ("42", "uncertain", "attention", old_id, "unconfirmed")])
        fields = dict(task="Export", id="request-1", text=original, chat_name="Codex · Export")
        self.assertEqual(self.alert(module, ledger, sender, **fields), "duplicate")
        self.assertEqual(self.alert(module, ledger, sender, **dict(fields, text="Pick a format.")), "duplicate")
        # A separate old receipt can be proved with original wording before any v2 receipt exists.
        self.assertEqual(self.alert(module, ledger, sender, project="uncertain", previous_text=original,
                                    **dict(fields, text="Pick a format.")), "unconfirmed")
        self.assertEqual(self.alert(module, ledger, sender, project="uncertain", confirm_retry=True,
                                    previous_text=original, **dict(fields, text="Pick a format.")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, **dict(fields, task="Import")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, **dict(fields, id="request-2")), "sent")
        self.assertEqual(self.alert(module, ledger, sender, "closed", batch="Batch-001",
                                    text="Closure verified."), "duplicate")
        with sqlite3.connect(ledger) as connection:
            self.assertEqual(connection.execute("SELECT state FROM alerts WHERE ident=? AND project='demo'", (old_id,)).fetchone(), ("sent",))
        self.assertEqual(len(sent), 3)

    def test_localized_structure_and_host_are_supplied_by_the_conversation(self):
        module = self.load_notifier()
        ledger = self.root / "languages.sqlite3"
        sent = []
        sender = lambda token, chat, text: sent.append(text)
        self.alert(module, ledger, sender, "delivered", batch="Batch-010", revision="a" * 40,
                   language="fr", text="Le candidat est prêt.", next_action="Commence les tests guidés.",
                   chat_name="Claude Code · Recette")
        self.assertIn("🧪 Prêt à tester\n\nProjet: demo\nRéférence: Batch-010", sent[-1])
        self.assertIn("Résumé: Le candidat est prêt. (révision aaaaaaa)", sent[-1])
        self.assertIn("Prochaine action: Commence les tests guidés. — Claude Code · Recette", sent[-1])
        self.assertNotIn("Codex", sent[-1])
        self.alert(module, ledger, sender, "completed", task="Export", id="done", text="Export verified.",
                   next_action="No action required.")
        self.assertIn("✅ Work completed", sent[-1])
        self.assertIn("Next action: No action required.", sent[-1])
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
            return subprocess.run([sys.executable, str(self.root / "agents/tools/notify-telegram.py"), *args],
                                  cwd=self.root, env={**{k: v for k, v in os.environ.items() if not k.startswith("TELEGRAM_")},
                                       **environment}, capture_output=True, text=True)

        full = ("attention", "--task", "Task", "--id", "r1", "--text", "Need you.", "--chat-name", "Chat",
                "--reference", "CARD-00000135", "--next-action", "Choose the format in the chat.")
        disabled = run(*full, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="completed")
        self.assertEqual(disabled.returncode, 0)
        self.assertIn("disabled; nothing was sent", disabled.stdout)
        missing = run(*full, TELEGRAM_EVENTS="attention")
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("Nothing was sent", missing.stderr)
        preview = run(*full, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="attention")
        self.assertIn("Preview:", preview.stdout)
        for bad in (("attention", "--task", "Task", "--id", "r1", "--text", "x"),  # No chat name.
                    (*full, "--reference", "Task-135"),
                    (*full, "--next-action", " "),
                    (*full, "--language", "es"),  # A known language needs translated labels.
                    ("attention", *full[1:], "--link", "not a link"),
                    ("attention", *full[1:], "--revision", "a" * 40)):
            self.assertNotEqual(run(*bad, TELEGRAM_CHAT_ID="42", TELEGRAM_EVENTS="attention").returncode, 0)

if __name__ == "__main__":
    unittest.main()
