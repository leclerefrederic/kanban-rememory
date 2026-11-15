"""Focused regression tests for the Rememory cutover."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from kanban import memory_migration as migration


class MemoryMigrationTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        self.write("project.json", json.dumps({
            "schema_version": 1,
            "project": {"id": "fixture", "name": "Fixture"},
            "shared": {"memory": "project/rememory", "sources": []},
            "modules": {"a": {"workspace": "project/modules/a"}},
            "execution": {
                "active_deliveries_per_module": 1, "branch_required": True,
                "worktree_required": True, "concurrent_integrations": 1,
            },
        }))

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def migrate(self, apply=False):
        with redirect_stdout(StringIO()) as output:
            migration.migrate(self.root, apply)
        return output.getvalue()

    def test_preview_move_links_and_repeat(self):
        old = self.write("project/rememory/2026-11-15.md",
                         "# 2026-11-15\n\n## Milestone\n\n[Guide](../../README.md)\n")
        module = self.write("project/modules/a/rememory/2026-11-16.md",
                            "# 2026-11-16\n\n[Milestone](../../../rememory/2026-11-15.md#milestone)\n")
        readme = self.write("README.md", "[Memory](project/rememory/2026-11-15.md)\n")
        completed = self.write("project/kanban/completion/card-00000001-history.md",
                               "[Milestone](../../rememory/2026-11-15.md#milestone)\n")
        before = {p: p.read_bytes() for p in (old, module, readme, completed)}
        self.assertIn("Preview only", self.migrate())
        self.assertEqual(before, {p: p.read_bytes() for p in before})
        self.assertFalse((self.root / "project/rememory/project").exists())

        self.assertIn("journals migrated", self.migrate(apply=True))
        project = self.root / "project/rememory/project/2026-11-15.md"
        scoped = self.root / "project/rememory/modules/a/2026-11-16.md"
        self.assertIn("[Guide](../../../README.md)", project.read_text())
        self.assertIn("[Milestone](../../project/2026-11-15.md#milestone)", scoped.read_text())
        self.assertIn("[Memory](project/rememory/project/2026-11-15.md)", readme.read_text())
        self.assertEqual(completed.read_bytes(), before[completed])
        self.assertIn(migration.FORWARD, old.read_text())
        self.assertIn("## Milestone", old.read_text())
        self.assertNotIn("[Guide]", old.read_text())
        self.assertFalse(module.exists())
        self.assertIn("already use", self.migrate(apply=True))

    def test_collision_leaves_existing_journals_untouched(self):
        old = self.write("project/rememory/2026-11-15.md", "# Original\n")
        new = self.write("project/rememory/project/2026-11-15.md", "# Existing\n")
        for apply in (False, True):
            with self.assertRaisesRegex(ValueError, "Journal collision"):
                self.migrate(apply)
        self.assertEqual(old.read_text(), "# Original\n")
        self.assertEqual(new.read_text(), "# Existing\n")

    def test_resume_after_interruption(self):
        old = self.write("project/rememory/2026-11-15.md", "# Journal\n\nOne entry\n")
        destination = self.root / "project/rememory/project/2026-11-15.md"
        replace = migration.replace

        def interrupt(path, data, mode):
            if path == old:
                raise OSError("simulated interruption")
            return replace(path, data, mode)

        with patch.object(migration, "replace", side_effect=interrupt):
            with self.assertRaisesRegex(OSError, "simulated interruption"):
                self.migrate(apply=True)
        self.assertEqual(destination.read_bytes(), old.read_bytes())
        self.assertIn("journals migrated", self.migrate(apply=True))
        self.assertFalse(old.exists())
        self.assertEqual(destination.read_text().count("One entry"), 1)
        self.assertIn("already use", self.migrate(apply=True))


if __name__ == "__main__":
    unittest.main()
