"""Run with Python 3.9+: tests of the KRR session signal command."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("krr_signal", Path(__file__).with_name("krr-signal.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SignalTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.env = {"KRR_SESSION_DIR": self.directory.name}
        self.file = Path(self.directory.name) / "signals.jsonl"

    def tearDown(self):
        self.directory.cleanup()

    def lines(self):
        return [json.loads(line) for line in self.file.read_text().splitlines()]

    def test_waiting_and_resumed_are_recorded(self):
        self.assertEqual(m.main(["waiting", "--id", "format-1"], self.env), 0)
        self.assertEqual(m.main(["resumed"], self.env), 0)
        waiting, resumed = self.lines()
        self.assertEqual((waiting["event"], waiting["id"]), ("waiting", "format-1"))
        self.assertEqual(resumed["event"], "resumed")
        self.assertNotIn("id", resumed)

    def test_a_repeated_call_succeeds_and_appends(self):
        for _ in range(2):
            self.assertEqual(m.main(["waiting", "--id", "q1"], self.env), 0)
        self.assertEqual(len(self.lines()), 2)

    def test_outside_a_session_nothing_is_written(self):
        self.assertEqual(m.main(["waiting", "--id", "q1"], {}), 1)
        self.assertEqual(m.main(["resumed"], {"KRR_SESSION_DIR": self.directory.name + "/missing"}), 1)
        self.assertFalse(self.file.exists())

    def test_invalid_arguments_are_refused(self):
        for argv in (["waiting"], ["waiting", "--id", "a b"], ["waiting", "--id", "x" * 81],
                     ["resumed", "--id", "q1"]):
            with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
                m.main(argv, self.env)
        self.assertFalse(self.file.exists())


if __name__ == "__main__":
    unittest.main()
