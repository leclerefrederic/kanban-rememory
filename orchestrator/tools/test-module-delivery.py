"""Verify module setup, resource isolation and Batch recovery with local Git only."""

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


KIT = Path(__file__).resolve().parents[2]
BATCH = "Batch-001"


class ModuleDeliveryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        self.root = self.base / "control"
        self.root.mkdir()
        self.git(self.root, "init", "-q", "-b", "main")
        self.git(self.base, "init", "-q", "--bare", str(self.base / "origin"))
        self.git(self.root, "remote", "add", "origin", str(self.base / "origin"))
        shutil.copytree(KIT / "orchestrator/tools", self.root / "orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copytree(KIT / "orchestrator/templates", self.root / "orchestrator/templates")
        self.manifest = {
            "schema_version": 1,
            "project": {"id": "fixture", "name": "Fixture"},
            "shared": {"memory": "project/rememory", "sources": ["src"]},
            "modules": {name: {"workspace": f"project/modules/{name}"} for name in ("a", "b")},
            "execution": {"active_deliveries_per_module": 1, "branch_required": True,
                          "worktree_required": True, "concurrent_integrations": 1},
        }
        src = self.root / "src"
        src.mkdir()
        (src / "shared.txt").write_text("shared\n")
        self.workflow = self.base / "workflow.json"
        workflow = json.loads((KIT / "project/settings.json").read_text())["workflow"]
        self.workflow.write_text(json.dumps(workflow))
        self.proposal = self.base / "proposal.json"
        self.proposal.write_text(json.dumps(self.manifest))

    def git(self, cwd, *args):
        return subprocess.check_output(
            ["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", *args],
            cwd=cwd, text=True, stderr=subprocess.PIPE,
        ).strip()

    def run_tool(self, cwd, tool, *args, expected=0):
        result = subprocess.run(
            [sys.executable, f"orchestrator/tools/{tool}.py", *map(str, args)], cwd=cwd,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def setup_modules(self, *args, expected=0):
        return self.run_tool(self.root, "configure-project-modules", self.proposal,
                             "--workflow", self.workflow, *args, expected=expected)

    def control(self, module, *args, expected=0):
        return self.run_tool(self.base / module, "manage-module-delivery",
                             "--module", module, *args, expected=expected)

    def commit(self, cwd, *args):
        self.git(cwd, "add", "--", ".")
        self.git(cwd, "commit", "-qm", args[0], *args[1:])
        return self.git(cwd, "rev-parse", "HEAD")

    def publication_note(self, module, delivery, owner, revision, *, expected=0):
        return self.control(module, "milestone", "published", delivery, "--owner", owner,
                            "--summary", f"Published {delivery} for {module}.",
                            "--revision", revision, "--published", expected=expected)

    def test_setup_batch_option_creates_canonical_and_reuses_legacy(self):
        module_a = self.root / "project/modules/a"
        module_b = self.root / "project/modules/b"
        (module_b / "specs/approved").mkdir(parents=True)
        preview = self.setup_modules("--with-batches")
        self.assertIn("project/modules/a/specifications/resources/active", preview)
        self.assertIn("project/modules/b/specs/resources/active", preview)
        self.assertFalse(module_a.exists())
        self.assertFalse((self.root / "project.json").exists())
        self.setup_modules("--with-batches", "--apply")
        self.assertTrue((module_a / "specifications/draft").is_dir())
        self.assertTrue((module_b / "specs/retired").is_dir())
        self.assertFalse((module_b / "specifications").exists())
        for module in (module_a, module_b):
            self.assertTrue((module / "batches").is_dir())
        self.run_tool(self.root, "manage-kanban-board", "validate")

    def test_activation_refuses_active_work_and_preserves_history(self):
        board = self.root / "project/kanban"
        for stage in ("backlog", "development", "completion", "cancellation"):
            (board / stage).mkdir(parents=True)
        shutil.copy(self.workflow, board)
        closed = board / "completion/card-00000001-history.md"
        closed.write_text("# Historic Card\n")
        digest = sha256(closed.read_bytes()).hexdigest()
        preview = self.setup_modules()
        self.assertIn("Preview only", preview)
        self.assertIn("project/rememory/project", preview)
        self.assertIn("project/rememory/modules/b", preview)
        self.assertFalse((self.root / "project.json").exists())
        self.assertFalse((self.root / "project/modules").exists())
        active = board / "development/card-00000002-active.md"
        active.write_text("# Active Card\n")
        self.assertIn("Close existing active Cards", self.setup_modules("--apply", expected=1))
        active.rename(board / "completion" / active.name)
        pending = board / "backlog/card-00000003-pending.md"
        pending.write_text("# Backlog Card\n")
        self.assertIn("approved migration plan", self.setup_modules("--apply", expected=1))
        pending.unlink()
        self.setup_modules("--apply")
        self.assertEqual(sha256(closed.read_bytes()).hexdigest(), digest)
        for module in ("a", "b"):
            self.assertTrue((self.root / f"project/rememory/modules/{module}").is_dir())
            self.assertFalse((self.root / f"project/modules/{module}/kanban").exists())
        self.assertTrue((board / "workflow.json").is_file())
        self.assertTrue((self.root / "project/rememory/project").is_dir())

    def test_manifest_errors_block_activation(self):
        original = self.proposal.read_text()
        cases = (
            ("{", "Invalid project.json"),
            ('{"schema_version":1,' + original[1:], "Duplicate project.json key"),
            (original.replace('"schema_version": 1', '"schema_version": 2'), "Unsupported"),
            (original.replace('"concurrent_integrations": 1', '"concurrent_integrations": 2'), "Unsupported"),
            (original.replace('project/modules/b', '../outside'), "repository-relative"),
            (original.replace('project/modules/b', 'project/modules/a/child'), "Overlapping"),
        )
        for text, error in cases:
            with self.subTest(text=text):
                self.proposal.write_text(text)
                self.assertIn(error, self.setup_modules("--apply", expected=1))
                self.assertFalse((self.root / "project.json").exists())
        workspaces = self.root / "project/modules"
        (workspaces / "a").mkdir(parents=True)
        (workspaces / "b").symlink_to("a", target_is_directory=True)
        self.proposal.write_text(original)
        self.assertIn("Overlapping", self.setup_modules("--apply", expected=1))

    def test_old_module_board_requires_an_explicit_plan_for_unfinished_cards(self):
        self.setup_modules("--apply")
        legacy = self.root / "project/modules/a/kanban"
        for stage in ("backlog", "completion"):
            (legacy / stage).mkdir(parents=True, exist_ok=True)
        frozen = legacy / "completion/card-00000008-frozen.md"
        frozen.write_text("# Historic closure\n")
        stale = legacy / "backlog/card-00000009-pending.md"
        stale.write_text("# Unfinished task\n")
        original = {path: path.read_bytes() for path in (stale, frozen)}
        refused = self.run_tool(self.root, "manage-kanban-board", "--scope", "a", "new",
                                "Another", "--owner", "Fixture", "--apply", expected=1)
        self.assertIn("approved migration plan", refused)
        self.assertFalse(list((self.root / "project/kanban/backlog").glob("*.md")))
        self.assertIn(str(frozen.relative_to(self.root)), self.run_tool(
            self.root, "manage-kanban-board", "history", "a/CARD-00000008",
        ))
        self.run_tool(self.root, "manage-kanban-board", "history", "a/CARD-00000009", expected=1)
        self.assertEqual({path: path.read_bytes() for path in original}, original)

    def write_batch(self, module, *, numbered=True):
        workspace = self.root / "project/modules" / module
        filename = "spec-001-r1.md" if numbered else "spec-001.md"
        spec = workspace / "specs/approved" / filename
        spec.parent.mkdir(parents=True)
        revision = 'revision: "1"\n' if numbered else ""
        spec.write_text(f'---\ntype: specification\nid: "SPEC-001"\n{revision}---\n')
        (workspace / "specs/retired").mkdir()
        (workspace / "specs/retired/.gitkeep").touch()
        record = workspace / "batches/batch-001"
        record.mkdir(parents=True)
        pins = [{"id": "SPEC-001", "path": spec.relative_to(self.root).as_posix()}]
        if numbered:
            pins[0]["revision"] = "1"
        (record / "description.md").write_text(
            f'---\ntype: batch\nid: "{BATCH}"\nspecifications: {json.dumps(pins)}\nstatus: ready\n---\n',
        )
        for kind in ("report", "tests"):
            (record / f"{kind}.md").write_text(
                f'---\ntype: {kind}\nid: "{BATCH}-{kind.title()}"\nbatch: "{BATCH}"\n---\n',
            )
        return record.relative_to(self.root)

    def initialize_deliveries(self, *, numbered=True):
        self.setup_modules("--apply")
        paths = {module: self.write_batch(module, numbered=numbered) for module in ("a", "b")}
        revision = self.commit(self.root, "Approve fixture batches")
        self.git(self.root, "push", "origin", "main")
        for module in paths:
            worktree = self.base / module
            self.git(self.root, "worktree", "add", "-qb", f"delivery-{module}", str(worktree))
            self.control(module, "claim", BATCH, "--owner", module, "--base", revision, "--approval", revision)
        return revision, paths

    def test_slot_holds_through_wait_rejection_and_resume(self):
        self.setup_modules("--apply")
        batch_paths = {module: self.write_batch(module) for module in ("a", "b")}
        for module in batch_paths:
            self.run_tool(self.root, "manage-kanban-board", "--module", module, "new",
                          "Independent", "--owner", "Fixture", "--apply")
        revision = self.commit(self.root, "Prepare drafts and card")
        self.git(self.root, "push", "origin", "main")
        for module in batch_paths:
            self.git(self.root, "worktree", "add", "-qb", f"delivery-{module}", str(self.base / module))
        card = "CARD-00000001"
        self.control("a", "claim", card, "--owner", "a-card", "--base", revision)
        self.control("b", "claim", "CARD-00000002", "--owner", "b-card", "--base", revision)
        self.assertIn("No matching ownership", self.control(
            "a", "claim", BATCH, "--owner", "a-batch", "--base", revision, "--approval", revision, expected=1,
        ))
        self.run_tool(self.base / "a", "manage-kanban-board", "--module", "a", "move", card, "development",
                      "--owner-token", "a-card")
        stage = self.root / "project/kanban"
        active = next((stage / "development").glob("*.md"))
        active.write_text(active.read_text().replace("## Acceptance criteria\n", "## Acceptance criteria\n\n- [x] Verified.\n"))
        self.run_tool(self.base / "a", "manage-kanban-board", "--module", "a", "move", card, "completion",
                      "--owner-token", "a-card")
        self.control("a", "integration", "begin", card, "--owner", "a-card")
        integration = self.base / "integration-card"
        self.git(self.root, "worktree", "add", "-q", "--detach", str(integration), "main")
        before = next((integration / "project/kanban/backlog").glob("card-00000001-*.md"))
        before.unlink()
        completed = next((stage / "completion").glob("*.md"))
        shutil.copy(completed, integration / completed.relative_to(self.root))
        closed = self.commit(integration, "Close independent A Card")
        self.control("a", "run-check", card, "--owner", "a-card", "--integration-checkout", integration,
                     "--", sys.executable, "-c", "from pathlib import Path; "
                     "assert any(Path('project/kanban/completion').glob('card-00000001-*.md'))")
        self.assertIn("not on published main", self.publication_note("a", card, "a-card", closed, expected=1))
        self.control("a", "publish-card", card, "--owner", "a-card", "--closing", closed)
        self.control("a", "integration", "release", card, "--owner", "a-card")
        self.assertIn("Record the verified project publication milestone", self.control(
            "a", "finish", card, "--owner", "a-card", "--revision", closed, expected=1,
        ))
        self.publication_note("a", card, "a-card", closed)
        self.publication_note("a", card, "a-card", closed)
        self.git(integration, "commit", "-qm", "Unrelated later commit", "--allow-empty")
        later = self.git(integration, "rev-parse", "HEAD")
        self.git(integration, "push", "origin", f"{later}:refs/heads/main")
        self.assertIn("recorded publication revision", self.publication_note(
            "a", card, "a-card", later, expected=1,
        ))
        journal = next((self.root / "project/rememory/project").glob("*.md")).read_text()
        self.assertEqual(journal.count(f"published/{closed}"), 1)
        self.assertIn("kanban/completion/card-00000001-", journal)
        self.assertFalse(list((self.root / "project/rememory/modules/a").glob("*.md")))
        self.control("a", "finish", card, "--owner", "a-card", "--revision", closed)
        self.control("a", "claim", BATCH, "--owner", "a-batch", "--base", revision, "--approval", revision)
        self.control("a", "checkpoint", BATCH, "--owner", "a-batch", "waiting")
        self.assertIn('"checkpoint": "waiting"', self.control(
            "a", "claim", BATCH, "--owner", "a-batch", "--base", revision, "--approval", revision,
        ))
        description = self.root / batch_paths["a"] / "description.md"
        ready = description.read_text()
        for state in ("in-progress", "delivered", "validated", "rejected"):
            description.write_text(ready.replace("status: ready", f"status: {state}"))
            self.assertIn("No matching ownership", self.control(
                "a", "claim", BATCH, "--owner", "takeover", "--base", revision, "--approval", revision, expected=1,
            ))
            self.assertIn('"owner": "b-card"', self.control("b", "status"))
        clone = self.base / "other-clone"
        self.git(self.base, "clone", "-q", "-b", "main", str(self.base / "origin"), str(clone))
        self.assertIn("dedicated worktree", self.run_tool(
            clone, "manage-module-delivery", "--module", "a", "claim", BATCH, "--owner", "foreign",
            "--base", revision, "--approval", revision, expected=1,
        ))

    def test_runtime_resources_are_isolated_and_exit_is_forwarded(self):
        self.initialize_deliveries()
        script = (
            'import os, socket, sqlite3, tempfile; from pathlib import Path; '
            "tmp = Path(tempfile.gettempdir()); runtime = Path(os.environ['KR_RUNTIME_DIR']); "
            "db = sqlite3.connect(tmp / 'test.db'); db.execute('CREATE TABLE items (n INTEGER)'); db.close(); "
            "p = Path(os.environ['KR_ARTIFACT_DIR']) / 'same-name'; p.write_text(os.environ['KR_MODULE']); "
            "assert runtime == tmp.parent; print(p)\n"
            "if os.environ.get('KR_TEST_LOOPBACK') == '1':\n"
            "    with socket.socket() as server:\n"
            "        server.bind(('127.0.0.1', 0)); assert server.getsockname()[1] > 0"

        )

        def execute(module):
            output = self.control(module, "run-check", BATCH, "--owner", module, "--", sys.executable, "-c", script)
            artifact = Path(output.splitlines()[-1])
            self.assertEqual(artifact.read_text(), module)
            return artifact

        with ThreadPoolExecutor(max_workers=2) as executor:
            paths = list(executor.map(execute, ("a", "b")))
        self.assertNotEqual(paths[0].parent, paths[1].parent)
        self.control("a", "run-check", BATCH, "--owner", "a", "--", sys.executable,
                     "-c", "raise SystemExit(7)", expected=7)

    def test_project_slot_is_independent_and_routes_work_notes(self):
        self.setup_modules("--apply")
        board = self.root / "project/kanban"
        for scope, title in (("@project", "Project operation"), ("a", "Module operation"),
                             ("@project", "Second project operation")):
            self.run_tool(self.root, "manage-kanban-board", "--scope", scope, "new",
                          title, "--owner", "Fixture", "--apply")
        revision = self.commit(self.root, "Prepare project and module Cards")
        for scope, branch in (("@project", "project"), ("a", "a")):
            self.git(self.root, "worktree", "add", "-qb", f"delivery-{branch}", str(self.base / scope))
        project_card, module_card, second = ("CARD-00000001", "CARD-00000002", "CARD-00000003")
        self.control("@project", "claim", project_card, "--owner", "p", "--base", revision)
        self.control("a", "claim", module_card, "--owner", "a", "--base", revision)
        self.assertIn("No matching ownership", self.control(
            "@project", "claim", second, "--owner", "other", "--base", revision, expected=1,
        ))

        def note(scope, card, owner):
            target = next((board / "backlog").glob(f"{card.lower()}-*.md")).relative_to(self.root)
            return self.control(scope, "milestone", "resumption", card, "--owner", owner,
                                "--summary", f"Resume {scope}.", "--revision", revision,
                                "--evidence", target)

        note("@project", project_card, "p")
        note("a", module_card, "a")
        project_memory = next((self.root / "project/rememory/project").glob("*.md")).read_text()
        module_memory = next((self.root / "project/rememory/modules/a").glob("*.md")).read_text()
        self.assertIn("Resume @project.", project_memory)
        self.assertNotIn("Resume a.", project_memory)
        self.assertIn("Resume a.", module_memory)

    def test_incompatible_combined_revision_cannot_prepare_closure(self):
        _, paths = self.initialize_deliveries()
        a, b = (self.base / module for module in ("a", "b"))
        (a / "src/shared.txt").write_text("updated")
        writer = self.commit(a, "Update shared data format")
        reader_path = b / "src/reader.py"
        reader_path.write_text("from pathlib import Path\nassert Path(__file__).with_name('shared.txt').read_text() == 'shared\\n'\n")
        reader = self.commit(b, "Read old shared format")
        self.control("a", "run-check", BATCH, "--owner", "a", "--", sys.executable, "-c",
                     "from pathlib import Path; assert Path('src/shared.txt').read_text() == 'updated'")
        self.control("b", "run-check", BATCH, "--owner", "b", "--", sys.executable, "src/reader.py")
        self.control("b", "integration", "begin", BATCH, "--owner", "b")
        integration = self.base / "integration"
        self.git(self.root, "worktree", "add", "-q", "--detach", str(integration), "main")
        self.git(integration, "merge", "--no-ff", "-m", "Merge disjoint changes", writer, reader)
        description = integration / paths["b"] / "description.md"
        description.write_text(description.read_text().replace("status: ready", "status: closed"))
        closing = self.commit(integration, "Combine and verify", "-m", f"Batch-Closure: b/{BATCH}")
        self.control("b", "run-check", BATCH, "--owner", "b", "--integration-checkout", integration,
                     "--", sys.executable, "src/reader.py", expected=1)
        self.assertIn("Verify the exact combined", self.control(
            "b", "closure", "prepare", BATCH, "--owner", "b", "--closing", closing,
            "--candidate", reader, "--result", "accepted", expected=1,
        ))
        self.control("b", "integration", "release", BATCH, "--owner", "b")
        self.control("a", "integration", "begin", BATCH, "--owner", "a")
        self.assertIn('"owner": "b"', self.control("b", "status"))
        self.control("a", "integration", "release", BATCH, "--owner", "a")

    def test_changed_combined_product_requires_new_acceptance_before_closure(self):
        _, paths = self.initialize_deliveries()
        self.git(self.root, "config", "core.hooksPath", "orchestrator/tools/git-hooks")
        a, b = (self.base / module for module in ("a", "b"))
        (a / "src/a.txt").write_text("A candidate")
        initial = self.commit(a, "Accept original A")
        (self.root / "src/intervening.txt").write_text("New shared inputs")
        advanced = self.commit(self.root, "Advance main after original decision")
        self.git(self.root, "push", "origin", "main")

        def assemble(module, label, candidate_to_merge, decision=None):
            checkout = self.base / label
            self.git(self.root, "worktree", "add", "-q", "--detach", str(checkout), "main")
            self.git(checkout, "merge", "--no-ff", "-m", f"Combine {module}", candidate_to_merge)
            combined = self.git(checkout, "rev-parse", "HEAD")
            accepted = combined if decision is None else decision
            description = checkout / paths[module] / "description.md"
            description.write_text(description.read_text().replace("status: ready", "status: closed"))
            with (checkout / paths[module] / "report.md").open("a") as stream:
                stream.write(f"\n## User decision\n\n- Decision: accepted `{accepted}`.\n")
            closing = self.commit(checkout, f"Close {module}", "-m", f"Batch-Closure: {module}/{BATCH}")
            return checkout, combined, accepted, closing

        def check(module, checkout):
            self.control(module, "run-check", BATCH, "--owner", module, "--integration-checkout", checkout,
                         "--", sys.executable, "-B", "-c",
                         f"from pathlib import Path; assert Path('src/intervening.txt').is_file(); "
                         f"assert Path('src/{module}.txt').is_file()")

        def prepare(module, closing, accepted, *, expected=0):
            return self.control(module, "closure", "prepare", BATCH, "--owner", module, "--closing", closing,
                                "--candidate", accepted, "--result", "accepted", expected=expected)

        directory = self.root / ".git/kanban-rememory/projects/fixture"
        pending = directory / "closure-a-batch-001.json"
        self.control("a", "integration", "begin", BATCH, "--owner", "a")
        old_checkout, old_combined, _, stale = assemble("a", "initial-merge", initial, initial)
        self.assertNotEqual(old_combined, initial)
        check("a", old_checkout)
        refused = prepare("a", stale, initial, expected=1)
        self.assertIn("The combined product differs", refused)
        self.assertIn("Integration was released. This module remains occupied.", refused)
        self.assertFalse(pending.exists())
        self.assertIn('"owner": "a"', self.control("a", "status"))
        self.assertNotEqual(self.git(self.root, "ls-remote", "origin", "refs/heads/main").split()[0], stale)

        # An interrupted preparation from the earlier implementation cannot be published on retry.
        pending.write_text(json.dumps({
            "project": "fixture", "delivery": "a/Batch-001", "owner": "a", "closing": stale,
            "candidate": initial, "result": "accepted", "main_revision": advanced,
        }))
        self.control("a", "integration", "begin", BATCH, "--owner", "a")
        check("a", old_checkout)
        refused = self.control("a", "closure", "publish", BATCH, "--owner", "a", expected=1)
        self.assertIn("Integration was released. This module remains occupied.", refused)
        self.assertEqual(self.git(self.root, "ls-remote", "origin", "refs/tags/fixture/a/batch-001"), "")

        # B can publish while A retains its own claim and awaits its updated decision.
        self.git(b, "merge", "--ff-only", advanced)
        (b / "src/b.txt").write_text("B candidate")
        b_revision = self.commit(b, "Independent B delivery")
        self.control("b", "integration", "begin", BATCH, "--owner", "b")
        b_checkout, _, b_accepted, b_closing = assemble("b", "publish-b", b_revision)
        check("b", b_checkout)
        prepare("b", b_closing, b_accepted)
        self.control("b", "closure", "publish", BATCH, "--owner", "b")
        self.control("b", "integration", "release", BATCH, "--owner", "b")
        self.git(self.root, "merge", "--ff-only", b_closing)
        self.assertIn(b_closing, self.control("a", "integration", "begin", BATCH, "--owner", "a"))

        # Preserve the older decision/evidence, then accept and close the new product revision.
        current, _, approved, closing = assemble("a", "accept-updated-a", initial)
        check("a", current)
        self.assertIn("src/b.txt", self.git(current, "diff", "--name-only", initial, approved))
        prepare("a", closing, approved)
        self.control("a", "closure", "publish", BATCH, "--owner", "a")
        self.assertEqual(self.git(self.root, "ls-remote", "origin", "refs/heads/main").split()[0], closing)
        self.assertEqual(self.git(self.root, "ls-remote", "origin", "refs/tags/fixture/a/batch-001").split()[0], approved)
        self.assertTrue((directory / f"closure-a-batch-001-previous-{stale}.json").is_file())
        self.control("a", "integration", "release", BATCH, "--owner", "a")
        with ThreadPoolExecutor(max_workers=2) as executor:
            notes = [executor.submit(self.publication_note, module, BATCH, module, sha)
                     for module, sha in (("a", closing), ("b", b_closing))]
            for note in notes:
                note.result()
        journal = next((self.root / "project/rememory/project").glob("*.md")).read_text()
        self.assertIn(f"a/{BATCH}/published/{closing}", journal)
        self.assertIn(f"b/{BATCH}/published/{b_closing}", journal)
        self.control("a", "finish", BATCH, "--owner", "a", "--revision", closing)
        self.control("b", "finish", BATCH, "--owner", "b", "--revision", b_closing)
        self.assertEqual(self.control("a", "status").strip(), "null")

    def test_simple_batch_retires_without_changing_its_approval_pin(self):
        self.run_tool(self.root, "manage-kanban-board", "init", "--template", "standard",
                      "--with-batches", "--apply")
        workspace = self.root / "project"
        original = workspace / "specifications/approved/spec-001.md"
        retired = workspace / "specifications/retired" / original.name
        original.write_text('---\ntype: specification\nid: "SPEC-001"\n---\n')
        expected = original.read_bytes()
        batch = workspace / "batches/batch-001"
        batch.mkdir()
        description = batch / "description.md"
        pins = [{"id": "SPEC-001", "path": original.relative_to(self.root).as_posix()}]
        source = f'---\ntype: batch\nid: "{BATCH}"\nspecifications: {json.dumps(pins)}\nstatus: ready\n---\n'
        description.write_text(source)
        for kind in ("tests", "report"):
            (batch / f"{kind}.md").write_text(
                f'---\ntype: {kind}\nid: "{BATCH}-{kind.title()}"\nbatch: "{BATCH}"\n---\n',
            )
        approval = self.commit(self.root, "Approve simple project fixture")
        args = (self.root, "manage-kanban-board", "retire-specifications", BATCH, approval)
        self.assertIn("decided Batch", self.run_tool(*args, expected=1))
        description.write_text(source.replace("status: ready", "status: validated"))
        self.run_tool(*args)
        self.assertFalse(original.exists())
        self.assertEqual(retired.read_bytes(), expected)
        description.write_text(source.replace("status: ready", "status: closed"))
        self.run_tool(self.root, "manage-kanban-board", "verify-approval", BATCH, approval)

    def test_interrupt_and_resume_accepted_and_rejected_publication(self):
        revision, paths = self.initialize_deliveries(numbered=False)
        self.git(self.root, "config", "core.hooksPath", "orchestrator/tools/git-hooks")
        candidates = {}
        for module in paths:
            checkout = self.base / module
            (checkout / "src" / f"{module}.txt").write_text(module)
            candidates[module] = self.commit(checkout, f"Candidate {module}")
            self.git(checkout, "push", "origin", f"delivery-{module}")

        def remotely(ref):
            return self.git(self.root, "ls-remote", "origin", ref).split()[0]

        for module, result in (("a", "accepted"), ("b", "rejected")):
            self.control(module, "integration", "begin", BATCH, "--owner", module)
            integration = self.base / f"integration-{module}"
            self.git(self.root, "worktree", "add", "-q", "--detach", str(integration), "main")
            candidate = candidates[module]
            if result == "accepted":
                self.git(integration, "merge", "--no-ff", "-m", "Integrate", candidate)
            description = integration / paths[module] / "description.md"
            status = "validated" if result == "accepted" else "rejected"
            source = description.read_text()
            description.write_text(source.replace("status: ready", f"status: {status}"))
            original = integration / paths[module].parent.parent / "specs/approved/spec-001.md"
            expected = original.read_bytes()
            retired = original.parent.parent / "retired" / original.name
            retire = ("closure", "retire", BATCH, "--owner", module, "--integration-checkout", integration)
            if result == "accepted":
                original.write_bytes(expected + b"Edited\n")
                self.assertIn("exact approved Specification", self.control(module, *retire, expected=1))
                self.assertFalse(retired.exists())
                original.write_bytes(expected)
            self.control(module, *retire)
            self.control(module, *retire)
            self.assertFalse(original.exists())
            self.assertEqual(retired.read_bytes(), expected)
            description.write_text(source.replace("status: ready", "status: closed"))
            with (integration / paths[module] / "report.md").open("a") as stream:
                stream.write(f'\n## User decision\n\n- Decision: {result} `{candidate}`.\n')
            closing = self.commit(integration, f"Close {module}", "-m", f"Batch-Closure: {module}/{BATCH}")
            command = (BATCH, "--owner", module, "--integration-checkout", integration, "--", sys.executable)
            self.control(module, "run-check", *command, "-c", "raise SystemExit(3)", expected=3)
            self.assertIn("Verify the exact combined", self.control(
                module, "closure", "prepare", BATCH, "--owner", module, "--closing", closing,
                "--candidate", candidate, "--result", result, expected=1,
            ))
            self.control(module, "run-check", *command, "-B", "-c",
                         "from pathlib import Path; assert Path('src/a.txt').is_file(); "
                         "assert not Path('src/b.txt').exists()")
            self.control(module, "closure", "prepare", BATCH, "--owner", module, "--closing", closing,
                         "--candidate", candidate, "--result", result)
            recovery = f"refs/heads/batch-recovery/fixture/{module}/batch-001"
            retained = f"refs/tags/fixture/{module}/batch-001" if result == "accepted" else (
                f"refs/heads/batch-archive/fixture/{module}/batch-001"
            )
            # Model interruption at different publication boundaries.
            self.git(integration, "push", "origin", f"{closing}:{recovery}")
            if result == "rejected":
                self.git(integration, "push", "origin", f"{candidate}:{retained}")
            self.assertEqual(remotely("refs/heads/main"), revision)
            self.control(module, "closure", "publish", BATCH, "--owner", module)
            self.control(module, "closure", "publish", BATCH, "--owner", module)
            self.assertEqual(remotely(retained), candidate)
            self.assertEqual(remotely("refs/heads/main"), closing)
            self.assertIn("Release integration", self.control(module, "finish", BATCH, "--owner", module,
                                                             "--revision", closing, expected=1))
            self.control(module, "integration", "release", BATCH, "--owner", module)
            self.publication_note(module, BATCH, module, closing)
            self.control(module, "finish", BATCH, "--owner", module, "--revision", closing)
            self.assertEqual(self.control(module, "status").strip(), "null")
            self.git(self.root, "merge", "--ff-only", closing)
            revision = closing
        self.assertTrue((self.root / "src/a.txt").is_file())
        self.assertFalse((self.root / "src/b.txt").exists())


if __name__ == "__main__":
    unittest.main()
