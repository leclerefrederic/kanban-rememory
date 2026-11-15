"""Verify project setup, Card delivery coordination and check isolation with local Git only."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock


KIT = Path(__file__).resolve().parents[2]
CARD = "CARD-00000001"


class ModuleDeliveryTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        for name in ("KR_CLAUDE_HOME", "KR_CODEX_HOME"):  # never read the real session logs
            patch = unittest.mock.patch.dict(os.environ, {name: str(self.base / name)})
            patch.start()
            self.addCleanup(patch.stop)
        self.root = self.base / "control"
        self.root.mkdir()
        self.git(self.root, "init", "-q", "-b", "main")
        self.git(self.base, "init", "-q", "--bare", str(self.base / "origin"))
        self.git(self.root, "remote", "add", "origin", str(self.base / "origin"))
        shutil.copytree(KIT / "orchestrator/tools", self.root / "orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__", "test-*.py"))
        shutil.copytree(KIT / "orchestrator/templates", self.root / "orchestrator/templates")
        settings = json.loads((KIT / "project/settings.json").read_text())
        settings.update(project={"id": "fixture", "name": "Fixture"}, last_card_id=0,
                        shared={"memory": "project/rememory", "sources": ["src"]},
                        modules={name: {"workspace": f"project/modules/{name}"} for name in ("a", "b", "misc")})
        self.settings = settings
        self.proposal = self.base / "proposal.json"
        self.proposal.write_text(json.dumps(settings))
        (self.root / "src").mkdir()
        (self.root / "src/shared.txt").write_text("shared\n")

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

    def control(self, worktree, module, *args, expected=0):
        return self.run_tool(self.base / worktree, "manage-module-delivery", "--module", module, *args,
                             expected=expected)

    def commit(self, cwd, message):
        self.git(cwd, "add", "--", ".")
        self.git(cwd, "commit", "-qm", message)
        return self.git(cwd, "rev-parse", "HEAD")

    def prepare(self, *modules):
        self.run_tool(self.root, "configure-project-modules", self.proposal, "--apply")
        for module in modules:
            self.run_tool(self.root, "manage-kanban-board", "new", "Delivery", "--owner", "Orchestrator",
                          "--scope", module, "--apply")
        revision = self.commit(self.root, "Prepare the board")
        self.git(self.root, "push", "-q", "origin", "main")
        return revision

    def worktree(self, name):
        self.git(self.root, "worktree", "add", "-qb", name, str(self.base / name))
        return self.base / name

    def test_setup_previews_applies_once_and_checks_the_workflow(self):
        self.assertIn("Preview only", self.run_tool(self.root, "configure-project-modules", self.proposal))
        self.assertFalse((self.root / "project").exists())
        broken = dict(self.settings, workflow=dict(self.settings["workflow"],
                                                   stages=["backlog", "development", "completion"]))
        bad = self.base / "bad.json"
        bad.write_text(json.dumps(broken))
        self.assertIn("Invalid project settings", self.run_tool(
            self.root, "configure-project-modules", bad, expected=1))
        no_misc = dict(self.settings, modules={"a": {"workspace": "project/modules/a"}})
        bad.write_text(json.dumps(no_misc))
        self.assertIn("misc module", self.run_tool(self.root, "configure-project-modules", bad, expected=1))
        self.run_tool(self.root, "configure-project-modules", self.proposal, "--apply")
        self.assertEqual((self.root / "project/settings.json").read_bytes(), self.proposal.read_bytes())
        for stage in (*self.settings["workflow"]["stages"], "resources"):
            self.assertTrue((self.root / "project/modules/a" / stage / ".gitkeep").is_file())
        self.assertTrue((self.root / "project/rememory/.gitkeep").is_file())
        self.assertIn("already exist", self.run_tool(
            self.root, "configure-project-modules", self.proposal, expected=1))
        self.run_tool(self.root, "manage-kanban-board", "validate")

    def test_card_delivery_from_claim_to_finish(self):
        revision = self.prepare("a")
        delivery = self.worktree("delivery-a")
        other = self.worktree("other-a")
        self.assertIn("dedicated worktree", self.run_tool(
            self.root, "manage-module-delivery", "--module", "a", "claim", CARD, "--owner", "x",
            "--base", revision, expected=1))
        self.control("delivery-a", "a", "claim", CARD, "--owner", "session-1", "--base", revision)
        self.assertIn('"checkpoint": "picked up"', self.control(
            "delivery-a", "a", "claim", CARD, "--owner", "session-1", "--base", revision))
        self.assertIn("No matching ownership", self.control(
            "other-a", "a", "claim", CARD, "--owner", "session-2", "--base", revision, expected=1))
        self.assertIn("recorded delivery branch", self.run_tool(
            other, "manage-kanban-board", "move", CARD, "development", "--owner-token", "session-1", expected=1))
        self.run_tool(delivery, "manage-kanban-board", "move", CARD, "development", "--owner-token", "session-1")
        self.control("delivery-a", "a", "checkpoint", CARD, "--owner", "session-1", "implementing")

        (delivery / "src/shared.txt").write_text("changed\n")
        candidate = self.commit(delivery, "Implement the Card")
        card = next((self.root / "project/modules/a/development").glob("card-00000001-*.md"))
        card.write_text(card.read_text().replace("## Acceptance criteria\n", "## Acceptance criteria\n\n- [x] Verified.\n"))
        self.run_tool(delivery, "manage-kanban-board", "move", CARD, "completion", "--owner-token", "session-1")
        completed = next((self.root / "project/modules/a/completion").glob("card-00000001-*.md"))

        self.control("delivery-a", "a", "integration", "begin", CARD, "--owner", "session-1")
        integration = self.base / "integration"
        self.git(self.root, "worktree", "add", "-q", "--detach", str(integration), "main")
        self.git(integration, "merge", "-q", "--ff-only", candidate)
        (integration / "project/modules/a/backlog" / completed.name).unlink()
        shutil.copy(completed, integration / completed.relative_to(self.root))
        closing = self.commit(integration, "Close the Card")
        check = ("from pathlib import Path; assert Path('src/shared.txt').read_text() == 'changed\\n'; "
                 "assert any(Path('project/modules/a/completion').glob('card-00000001-*.md'))")
        self.control("delivery-a", "a", "run-check", CARD, "--owner", "session-1",
                     "--integration-checkout", integration, "--", sys.executable, "-c", check)
        self.assertIn("not on published main", self.control(
            "delivery-a", "a", "milestone", "published", CARD, "--owner", "session-1", "--summary", "Done.",
            "--revision", closing, "--published", expected=1))
        self.control("delivery-a", "a", "publish-card", CARD, "--owner", "session-1", "--closing", closing)
        self.assertEqual(self.git(self.root, "ls-remote", "origin", "refs/heads/main").split()[0], closing)
        self.control("delivery-a", "a", "integration", "release", CARD, "--owner", "session-1")
        self.assertIn("publication milestone", self.control(
            "delivery-a", "a", "finish", CARD, "--owner", "session-1", "--revision", closing, expected=1))
        for _ in range(2):
            self.control("delivery-a", "a", "milestone", "published", CARD, "--owner", "session-1",
                         "--summary", "Done.", "--revision", closing, "--published")
        journal = "".join(path.read_text() for path in (self.root / "project/rememory").glob("????-??-??.md"))
        self.assertEqual(journal.count(f"published/{closing}"), 1)
        self.assertRegex(journal, r"Duration: (<1|\d+) min \(CARD-00000001 (<1|\d+) min\)\. Tokens \(Claude Code\): unavailable")
        self.assertIn(f"](<../modules/a/completion/{completed.name}>)", journal)
        self.control("delivery-a", "a", "finish", CARD, "--owner", "session-1", "--revision", closing)
        self.assertEqual(self.control("delivery-a", "a", "status").strip(), "null")
        self.run_tool(self.root, "manage-kanban-board", "validate")

    def test_phase_delivers_several_cards_with_one_closure(self):
        revision = self.prepare("a", "a")
        first, second = "CARD-00000001", "CARD-00000002"
        delivery = self.worktree("phase-a")
        self.control("phase-a", "a", "claim", first, "--owner", "s", "--base", revision)
        self.assertIn("not yet in the phase", self.control(
            "phase-a", "a", "add-card", first, first, "--owner", "s", expected=1))
        self.control("phase-a", "a", "add-card", first, second, "--owner", "s")
        self.assertIn("No matching ownership", self.run_tool(
            delivery, "manage-kanban-board", "move", second, "development", "--owner-token", "other", expected=1))
        for card in (first, second):
            self.run_tool(delivery, "manage-kanban-board", "move", card, "development", "--owner-token", "s")
            path = next((self.root / "project/modules/a/development").glob(f"card-{card[5:]}-*.md"))
            path.write_text(path.read_text().replace(
                "## Acceptance criteria\n", "## Acceptance criteria\n\n- [x] Verified.\n"))
            self.run_tool(delivery, "manage-kanban-board", "move", card, "completion", "--owner-token", "s")
        self.assertIn(second, self.control("phase-a", "a", "status"))


    def test_report_sums_durations_and_host_tokens_for_the_phase_window(self):
        sys.path.insert(0, str(KIT / "orchestrator/tools"))
        from kanban import report
        start, end = datetime.fromisoformat("2026-11-15T10:00:00+01:00"), datetime.fromisoformat("2026-11-15T11:30:00+01:00")
        history = ("- 2026-11-15T10:05:00+01:00 — Stage moved from `backlog` to `development`.\n"
                   "- 2026-11-15T10:20:00+01:00 — Stage moved from `development` to `completion`.\n")
        self.assertEqual(report.card_duration(history, ["development"], "completion"), "15 min")
        self.assertEqual(report.minutes(start, end), "1 h 30 min")
        work = self.base / "work"
        directory = self.base / "KR_CLAUDE_HOME/projects" / "".join(c if c.isalnum() else "-" for c in str(work))
        directory.mkdir(parents=True)
        usage = lambda n: {"input_tokens": n, "cache_creation_input_tokens": 2 * n,
                           "cache_read_input_tokens": 3 * n, "output_tokens": 4 * n}
        rows = [{"timestamp": "2026-11-15T08:59:59Z", "message": {"id": "old", "usage": usage(100)}},
                {"timestamp": "2026-11-15T09:10:00Z", "message": {"id": "m1", "usage": usage(1)}},
                {"timestamp": "2026-11-15T09:10:01Z", "message": {"id": "m1", "usage": usage(1)}},
                {"timestamp": "2026-11-15T09:20:00Z", "message": {"id": "m2", "usage": usage(2)}},
                {"timestamp": "2026-11-15T12:00:00Z", "message": {"id": "late", "usage": usage(100)}}]
        (directory / "s.jsonl").write_text("\n".join(map(json.dumps, rows)) + "\nnot json\n")
        self.assertEqual(report.claude_tokens({work}, start, end),
                         {"input_tokens": 3, "cache_creation_input_tokens": 6,
                          "cache_read_input_tokens": 9, "output_tokens": 12})
        self.assertIsNone(report.claude_tokens({self.base / "elsewhere"}, start, end))
        rollout = self.base / "KR_CODEX_HOME/sessions/2026/11/15/rollout-x.jsonl"
        rollout.parent.mkdir(parents=True)
        count = lambda at, i, c, o: {"timestamp": at, "type": "event_msg", "payload": {"type": "token_count", "info": {
            "total_token_usage": {"input_tokens": i, "cached_input_tokens": c, "output_tokens": o}}}}
        rows = [{"timestamp": "2026-11-15T08:00:00Z", "type": "session_meta", "payload": {"cwd": str(work)}},
                count("2026-11-15T08:30:00Z", 100, 50, 10), count("2026-11-15T09:30:00Z", 300, 150, 40),
                count("2026-11-15T12:00:00Z", 900, 450, 90)]
        rollout.write_text("\n".join(map(json.dumps, rows)) + "\n")
        self.assertEqual(report.codex_tokens({work}, start, end),
                         {"input_tokens": 200, "cached_input_tokens": 100, "output_tokens": 30})
        text = report.report(start, end, [("CARD-1", history)], ["development"], "completion", {work})
        self.assertIn("Duration: 1 h 30 min (CARD-1 15 min).", text)
        self.assertIn("Tokens (Claude Code): input 3, cache write 6, cache read 9, output 12.", text)
        self.assertIn("Tokens (Codex): input 200, cached input 100, output 30.", text)

    def test_claims_race_and_integration_is_serialized(self):
        revision = self.prepare("a", "b")
        for name in ("a1", "a2", "b1"):
            self.worktree(name)
        cards = {"a": "CARD-00000001", "b": "CARD-00000002"}

        def claim(owner):
            return subprocess.run(
                [sys.executable, "orchestrator/tools/manage-module-delivery.py", "--module", owner[0], "claim",
                 cards[owner[0]], "--owner", owner, "--base", revision],
                cwd=self.base / owner, capture_output=True, text=True,
            ).returncode

        with ThreadPoolExecutor(max_workers=3) as concurrent:
            results = dict(zip(("a1", "a2", "b1"), concurrent.map(claim, ("a1", "a2", "b1"))))
        self.assertEqual(sorted((results["a1"], results["a2"])), [0, 1])
        self.assertEqual(results["b1"], 0)
        winner = "a1" if results["a1"] == 0 else "a2"
        args_a = (cards["a"], "--owner", winner)
        self.control(winner, "a", "integration", "begin", *args_a)
        self.assertIn("Integration is held", self.control(
            "b1", "b", "integration", "begin", cards["b"], "--owner", "b1", expected=1))
        advanced = self.git(self.root, "commit-tree", "HEAD^{tree}", "-p", revision, "-m", "main changed")
        self.git(self.root, "update-ref", "refs/heads/main", advanced, revision)
        self.assertIn("Main advanced", self.control(winner, "a", "integration", "verify", *args_a, expected=1))
        self.control(winner, "a", "integration", "release", *args_a)
        self.control("b1", "b", "integration", "begin", cards["b"], "--owner", "b1")

    def test_checks_get_isolated_runtime_directories(self):
        revision = self.prepare("a", "b")
        for module, card in (("a", "CARD-00000001"), ("b", "CARD-00000002")):
            self.worktree(module)
            self.control(module, module, "claim", card, "--owner", module, "--base", revision)
        script = ("import os, tempfile; from pathlib import Path; "
                  "runtime = Path(os.environ['KR_RUNTIME_DIR']); assert runtime == Path(tempfile.gettempdir()).parent; "
                  "p = Path(os.environ['KR_ARTIFACT_DIR']) / 'same-name'; p.write_text(str(runtime)); print(p)")

        def execute(item):
            module, card = item
            output = self.control(module, module, "run-check", card, "--owner", module, "--",
                                  sys.executable, "-c", script)
            return Path(output.splitlines()[-1])

        with ThreadPoolExecutor(max_workers=2) as executor:
            paths = list(executor.map(execute, (("a", "CARD-00000001"), ("b", "CARD-00000002"))))
        self.assertNotEqual(paths[0].parent, paths[1].parent)
        self.control("a", "a", "run-check", "CARD-00000001", "--owner", "a", "--", sys.executable,
                     "-c", "raise SystemExit(7)", expected=7)


if __name__ == "__main__":
    unittest.main()
