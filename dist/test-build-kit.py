"""build-kit.py: the ZIP holds the committed kit under kanban-rememory/ and nothing else."""

import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location("build_kit", Path(__file__).with_name("build-kit.py"))
build_kit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_kit)


class BuildKitTests(unittest.TestCase):
    def test_zip_holds_the_committed_kit_files_under_kanban_rememory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            files = {"kanban-rememory.json": json.dumps({"version": "1.2.3"}), "GUARDRAILS.md": "rules\n",
                     "AGENTS.md": "agents\n", "notes.md": "not in the kit\n",
                     "kanban-rememory/orchestrator/tools/kr.py": "print()\n"}
            for name, text in files.items():
                (root / name).parent.mkdir(parents=True, exist_ok=True)
                (root / name).write_text(text)
            for args in (["init", "-q", "-b", "main"], ["add", "-A"],
                         ["-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "-qm", "kit"]):
                subprocess.check_call(["git", *args], cwd=root)
            archive = build_kit.build(root)
            self.assertEqual(archive, root / "dist/kanban-rememory-kit-1.2.3.zip")
            with zipfile.ZipFile(archive) as kit:
                names = set(kit.namelist())
                version = kit.read("kanban-rememory-kit-1.2.3/kanban-rememory/VERSION").decode()
        prefix = "kanban-rememory-kit-1.2.3/"
        self.assertTrue(all(name.startswith(prefix + "kanban-rememory/") for name in names - {prefix}))
        self.assertEqual(version, "1.2.3\n")
        self.assertIn(prefix + "kanban-rememory/orchestrator/templates/GUARDRAILS.md", names)
        self.assertIn(prefix + "kanban-rememory/orchestrator/tools/kr.py", names)


if __name__ == "__main__":
    unittest.main()
