"""Exercise the pre-push check against committed module records."""

from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


TOOLS = Path(__file__).resolve().parent


class ModulePublicationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        tools = self.root / "orchestrator/tools"
        tools.mkdir(parents=True)
        for name in ("check-batch-publication.py", "guard-batch-work.py"):
            shutil.copy(TOOLS / name, tools)
        shutil.copytree(TOOLS / "kanban", tools / "kanban", ignore=shutil.ignore_patterns("__pycache__"))
        self.git("init", "-q")
        self.manifest = self.root / "project.json"
        self.manifest.write_text(json.dumps({
            "schema_version": 1,
            "project": {"id": "fixture", "name": "Fixture"},
            "shared": {"memory": "project/rememory", "sources": ["README.md"]},
            "modules": {name: {"workspace": f"work/{name}"} for name in ("a", "b")},
            "execution": {
                "active_deliveries_per_module": 1,
                "branch_required": True,
                "worktree_required": True,
                "concurrent_integrations": 1,
            },
        }))
        (self.root / "README.md").write_text("# Fixture\n")
        self.directory = self.root / ".git/kanban-rememory/projects/fixture"
        for module in ("a", "b"):
            self.write_status(module, "delivered")
        self.previous = self.commit("Delivered both module batches")

    def git(self, *args):
        return subprocess.check_output(
            ["git", "-c", "user.name=Test", "-c", "user.email=t@example.invalid", *args],
            cwd=self.root, text=True,
        ).strip()

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")

    def write_status(self, module, status):
        record = self.root / f"work/{module}/batches/batch-001/description.md"
        record.parent.mkdir(parents=True, exist_ok=True)
        record.write_text(f"---\nid: Batch-001\nstatus: {status}\n---\n")

    def was_pushed(self, closing):
        return subprocess.run(
            [sys.executable, "orchestrator/tools/check-batch-publication.py"],
            cwd=self.root, input=f"refs/heads/main {closing} refs/heads/main {self.previous}\n",
            text=True, capture_output=True,
        )

    def record_closure(self, module, closing, *, main=None, candidate=None):
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / f"closure-{module}-batch-001.json").write_text(json.dumps({
            "project": "fixture", "delivery": f"{module}/Batch-001", "owner": "developer",
            "closing": closing, "candidate": candidate or self.previous, "result": "accepted",
            "main_revision": main or self.previous,
        }))
        (self.directory / "integration.json").write_text(json.dumps({
            "owner": "developer", "module": module, "delivery": "Batch-001",
            "worktree": str(self.root / "candidate"), "main_revision": self.previous, "verified_revision": closing,
        }))

    def test_same_batch_id_in_two_modules_needs_exact_qualified_evidence(self):
        self.write_status("a", "closed")
        closing = self.commit("Close A\n\nBatch-Closure: a/Batch-001")
        self.record_closure("b", closing)
        result = self.was_pushed(closing)
        self.assertEqual(result.returncode, 1)
        self.assertIn("closure-a-batch-001.json", result.stderr)

        self.record_closure("a", closing, main=closing)
        result = self.was_pushed(closing)
        self.assertEqual(result.returncode, 1)
        self.assertIn("pushed revisions", result.stderr)

        self.record_closure("a", closing)
        other_guard = self.directory / "modules/b/batch-001/guard.json"
        other_guard.parent.mkdir(parents=True)
        other_guard.write_text("{}")
        self.manifest.write_text("broken working tree manifest")
        result = self.was_pushed(closing)
        self.assertEqual(result.returncode, 0, result.stderr)

        guard = self.directory / "modules/a/batch-001/guard.json"
        guard.parent.mkdir(parents=True)
        guard.write_text("{}")
        result = self.was_pushed(closing)
        self.assertEqual(result.returncode, 1)
        self.assertIn("a/batch-001 cannot be closed", result.stderr)
        self.assertIn("acceptance artifact", result.stderr)

    def test_closing_product_must_match_the_accepted_candidate(self):
        product = self.root / "README.md"
        product.write_text("# Accepted product\n")
        candidate = self.commit("Deliver initial product")

        def check_closure(accepted):
            self.write_status("a", "closed")
            closing = self.commit("Close A\n\nBatch-Closure: a/Batch-001")
            self.record_closure("a", closing, candidate=accepted)
            return self.was_pushed(closing)

        records_only = check_closure(candidate)
        self.assertEqual(records_only.returncode, 0, records_only.stderr)

        for change in ("contents", "mode", "deletion"):
            with self.subTest(change=change):
                self.git("checkout", "-q", "--detach", candidate)
                if change == "contents":
                    product.write_text("# Changed product\n")
                elif change == "mode":
                    self.git("update-index", "--chmod=+x", "README.md")
                    product.chmod(0o755)
                else:
                    product.unlink()
                refused = check_closure(candidate)
                self.assertEqual(refused.returncode, 1, refused.stdout + refused.stderr)
                self.assertIn("README.md", refused.stderr)

        self.git("checkout", "-q", "--detach", candidate)
        product.write_text("# Changed product\n")
        approved_replacement = self.commit("Deliver changed product for new acceptance")
        published = check_closure(approved_replacement)
        self.assertEqual(published.returncode, 0, published.stderr)

    def test_artifact_guard_uses_the_module_and_batch_of_active_card(self):
        name = "CARD-00000001"
        board = self.root / "project/kanban"
        stage = board / "development"
        stage.mkdir(parents=True)
        (board / "completion").mkdir()
        (board / "workflow.json").write_text(json.dumps({
            "stages": ["development", "completion"], "active": ["development"],
            "completed": "completion", "wip_limit": 1, "timezone": "UTC",
        }))
        (stage / f"{name.lower()}-example.md").write_text('---\nscope: "a"\nbatch: "Batch-001"\n---\n')
        (stage / "card-00000002-other.md").write_text('---\nscope: "b"\nbatch: "Batch-002"\n---\n')

        def invoke(selected, record):
            return subprocess.run(
                [sys.executable, "orchestrator/tools/guard-batch-work.py", "change", str(record),
                 "--module", selected, "--card", name],
                cwd=self.root, capture_output=True, text=True,
            )

        a_guard = self.directory / "modules/a/batch-001/guard.json"
        b_guard = self.directory / "modules/b/batch-001/guard.json"
        for record in (a_guard, b_guard):
            record.parent.mkdir(parents=True)
            record.write_text(json.dumps({"authorized_cards": [name]}))
        passed = invoke("a", a_guard)
        self.assertEqual(passed.returncode, 0, passed.stderr)
        refused = invoke("a", b_guard)
        self.assertEqual(refused.returncode, 1)
        self.assertIn("Expected a local guard", refused.stderr)
        refused = invoke("b", b_guard)
        self.assertEqual(refused.returncode, 1)
        self.assertIn("out-of-scope", refused.stderr)

    def test_module_artifact_guard_rejects_new_product_with_unchanged_frozen_artifact(self):
        artifact = self.root / ".git/fixture-artifact"
        payload = b"accepted artifact"
        artifact.write_bytes(payload)
        guard = self.directory / "modules/a/batch-001/guard.json"
        guard.parent.mkdir(parents=True)
        digest = sha256(artifact.name.encode() + b"\0-" + payload).hexdigest()
        guard.write_text(json.dumps({
            "base_revision": self.previous,
            "acceptance": {"path": str(artifact), "sha256": digest, "revision": self.previous},
            "verification": {"revision": self.previous, "technical_checks": "passed"},
            "decision": {"result": "accepted", "revision": self.previous},
        }))

        def verify(closing):
            return subprocess.run(
                [sys.executable, "orchestrator/tools/guard-batch-work.py", "publish",
                 str(guard), "--revision", closing], cwd=self.root, capture_output=True, text=True,
            )

        self.write_status("a", "closed")
        specs = self.root / "work/a/specifications"
        approved = specs / "approved/spec-001-r1.md"
        approved.parent.mkdir(parents=True)
        approved.write_text("# Specification\n")
        records_only = self.commit("Close records")
        unchanged = verify(records_only)
        self.assertEqual(unchanged.returncode, 0, unchanged.stderr)
        resource = specs / "resources/active/mockup.md"
        resource.parent.mkdir(parents=True)
        resource.write_text("Product requirement attachment\n")
        resource_changed = verify(self.commit("Change Specification resource"))
        self.assertEqual(resource_changed.returncode, 1)
        self.assertIn("specifications/resources/active/mockup.md", resource_changed.stderr)
        resource.unlink()
        (self.root / "README.md").write_text("Combined product changed")
        changed = verify(self.commit("Change product"))
        self.assertEqual(changed.returncode, 1)
        self.assertIn("The combined product differs", changed.stderr)

    def test_invalid_committed_manifest_does_not_fall_back_to_legacy(self):
        original = self.manifest.read_text()
        self.manifest.write_text('{"schema_version": 99}')
        invalid = self.commit("Invalid committed manifest")
        self.manifest.write_text(original)
        result = self.was_pushed(invalid)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Invalid project.json", result.stderr)

    def test_committed_symlink_is_rejected_even_with_regular_checkout(self):
        self.manifest.unlink()
        self.manifest.symlink_to("README.md")
        invalid = self.commit("Commit a symlink as the manifest")
        self.manifest.unlink()
        self.manifest.write_text("{}")
        result = self.was_pushed(invalid)
        self.assertEqual(result.returncode, 1)
        self.assertIn("regular file: project.json", result.stderr)


if __name__ == "__main__":
    unittest.main()
