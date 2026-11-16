"""init.py: preview, refusals, the written boards, and that kr accepts what the installer wrote."""

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("init", HERE / "init.py")
INIT = importlib.util.module_from_spec(spec)
spec.loader.exec_module(INIT)
WORKFLOW = {"stages": ["backlog", "development", "completion", "cancellation"], "active": ["development"],
            "completed": "completion", "wip_limit": 1, "timezone": "Europe/Paris",
            "transitions": {"backlog": ["development", "cancellation"], "development": ["completion", "cancellation"]}}


class InitTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        self.root = self.base / "repo"
        self.root.mkdir()
        self.settings = {"name": "Fixture", "directory": "work", "modules": ["a", "misc"], "workflow": WORKFLOW,
                         "version": "0.0.0", "kit": "0.1.0"}
        self.proposal = self.base / "proposal.json"
        self.proposal.write_text(json.dumps(self.settings))

    def init(self, *args, expected=0):
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output):
            code = INIT.main([str(arg) for arg in args], self.root)
        self.assertEqual(code, expected, output.getvalue())
        return output.getvalue()

    def test_preview_writes_nothing_and_apply_creates_the_boards_once(self):
        self.assertIn("Preview only", self.init(self.proposal))
        self.assertEqual(list(self.root.iterdir()), [])
        self.init(self.proposal, "--apply")
        self.assertEqual((self.root / "kanban-rememory.json").read_bytes(), self.proposal.read_bytes())
        self.assertTrue((self.root / "work/modules/a/resources/.gitkeep").is_file())
        self.assertTrue((self.root / "work/rememory/.gitkeep").is_file())
        self.assertIn("already exists", self.init(self.proposal, "--apply", expected=1))

    def test_refuses_proposals_the_tools_would_reject(self):
        bad = self.base / "bad.json"
        for change, message in (({"workflow": dict(WORKFLOW, stages=["backlog", "development", "completion"])}, "stages"),
                                ({"modules": ["a"]}, "include misc"), ({"directory": "kanban-rememory"}, "directory"),
                                ({"directory": "../x"}, "directory"), ({"kit": "x"}, "kit"), ({"other": 1}, "must contain"),
                                ({"workflow": dict(WORKFLOW, timezone="Mars/Base")}, "time zone"),
                                ({"workflow": dict(WORKFLOW, active=["backlog"])}, "active")):
            bad.write_text(json.dumps(dict(self.settings, **change)))
            self.assertIn(message, self.init(bad, expected=1))
        bad.write_text('{"name": "a", "name": "b"}')
        self.assertIn("Duplicate key", self.init(bad, expected=1))
        self.assertEqual(list(self.root.iterdir()), [])

    def test_kr_accepts_what_the_installer_wrote(self):
        shutil.copytree(HERE.parents[1] / "kanban-rememory/orchestrator/tools", self.root / "kanban-rememory/orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__", "test-*.py"))
        self.init(self.proposal, "--apply")
        subprocess.check_call(["git", "init", "-q", "-b", "main"], cwd=self.root)
        result = subprocess.run(["python3", "kanban-rememory/orchestrator/tools/kr.py", "validate"], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
