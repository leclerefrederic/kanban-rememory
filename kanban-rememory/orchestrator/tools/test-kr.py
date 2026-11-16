"""Risky behavior of kr.py: Card IDs, moves, validation, one phase from start to publish, the report, setup."""

from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

KIT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KIT / "kanban-rememory/orchestrator/tools"))
from kanban import report  # noqa: E402

spec = importlib.util.spec_from_file_location("kr", KIT / "kanban-rememory/orchestrator/tools/kr.py")
KR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(KR)
WORKFLOW = json.loads((KIT / "kanban-rememory.json").read_text())["workflow"]


class KrTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.base = Path(directory.name).resolve()
        # Never read the real session logs, never reach the real Telegram configuration.
        environment = {name: str(self.base / name) for name in ("KR_CLAUDE_HOME", "KR_CODEX_HOME", "HOME", "LOCALAPPDATA")}
        environment.update(GIT_AUTHOR_NAME="Fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                           GIT_COMMITTER_NAME="Fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
        patcher = mock.patch.dict(os.environ, environment)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.settings = {"name": "Fixture", "modules": ["a", "b", "misc"],
                         "workflow": WORKFLOW, "version": "0.0.0", "directory": "project"}
        self.proposal = self.base / "proposal.json"
        self.proposal.write_text(json.dumps(self.settings))
        self.root = self.repository("repo")
        self.kr(self.root, "init", self.proposal, "--apply")
        self.git(self.base, "init", "-q", "--bare", "origin.git")
        self.git(self.root, "remote", "add", "origin", self.base / "origin.git")
        self.commit(self.root, "Initialize")
        self.git(self.root, "push", "-q", "origin", "main")

    def repository(self, name):
        root = self.base / name
        shutil.copytree(KIT / "kanban-rememory/orchestrator/tools", root / "kanban-rememory/orchestrator/tools",
                        ignore=shutil.ignore_patterns("__pycache__", "test-*.py"))
        (root / ".gitignore").write_text("__pycache__/\n")
        self.git(root, "init", "-q", "-b", "main")
        return root

    def git(self, cwd, *args):
        return subprocess.check_output(["git", "-c", "commit.gpgsign=false", *map(str, args)], cwd=cwd, text=True,
                                       stderr=subprocess.PIPE).strip()

    def kr(self, root, *args, expected=0, stdin=""):
        output = io.StringIO()
        with redirect_stdout(output), redirect_stderr(output), mock.patch.object(sys, "stdin", io.StringIO(stdin)):
            try:
                code = KR.main([str(arg) for arg in args], root)
            except SystemExit as exit:
                code = exit.code
        self.assertEqual(code or 0, expected, output.getvalue())
        return output.getvalue()

    def commit(self, cwd, message):
        self.git(cwd, "add", "-A")
        self.git(cwd, "commit", "-qm", message)
        return self.git(cwd, "rev-parse", "HEAD")

    def board(self, module, root=None):
        return (root or self.root) / "project/modules" / module

    def card(self, root, task_id):
        return root / self.kr(root, "path", task_id).strip()

    def test_new_allocates_project_wide_ids_once(self):
        self.kr(self.root, "new", "First", "--module", "a")
        first = self.board("a") / "backlog/card-00000001-first.md"
        self.assertIn('id: "CARD-00000001"\nmodule: "a"\n---\n\n# CARD-00000001 — First\n', first.read_text())
        self.kr(self.root, "new", "Default", "--body", stdin="- Dependencies: None.\n\n## Acceptance criteria\n")
        self.assertTrue((self.board("misc") / "backlog/card-00000002-default.md").read_text().endswith(
            "# CARD-00000002 — Default\n\n- Dependencies: None.\n\n## Acceptance criteria\n"))
        self.assertIn("empty Card body", self.kr(self.root, "new", "Empty", "--body", expected=1))
        (self.root / "kanban-rememory.json").write_text(json.dumps(dict(self.settings, last_card_id=40)))
        self.assertIn("must contain", self.kr(self.root, "new", "Refused", expected=1))
        (self.root / "kanban-rememory.json").write_text(json.dumps(self.settings))
        self.kr(self.root, "new", "Later", "--module", "b")
        self.assertTrue((self.board("b") / "backlog/card-00000003-later.md").is_file())
        shutil.copy(first, self.board("b") / "backlog" / first.name)
        self.assertIn("Duplicate CARD-00000001", self.kr(self.root, "new", "Collision", expected=1))
        self.assertIn("Unknown module", self.kr(self.root, "new", "Elsewhere", "--module", "z", expected=1))

    def test_moves_follow_the_workflow_and_keep_history(self):
        self.kr(self.root, "new", "Example", "--module", "a")
        self.assertIn("not allowed", self.kr(self.root, "move", "CARD-00000001", "completion", expected=1))
        self.assertIn("start CARD-00000001", self.kr(self.root, "move", "CARD-00000001", "development", expected=1))
        self.kr(self.root, "move", "CARD-00000001", "cancellation")
        moved = self.board("a") / "cancellation/card-00000001-example.md"
        self.assertRegex(moved.read_text(), r"## History\n\n- \S+ — Stage moved from `backlog` to `cancellation`\.\n$")
        self.assertIn("history", self.kr(self.root, "move", "CARD-00000001", "backlog", expected=1))

    def test_validate_reports_each_record_and_document_problem(self):
        self.kr(self.root, "new", "Example", "--module", "a")
        self.kr(self.root, "new", "Shared")
        self.kr(self.root, "validate")
        card = self.board("a") / "backlog/card-00000001-example.md"
        card.write_text(card.read_text().replace('module: "a"', 'module: "b"')
                        + "\n## Resources\n\n- [Spec](../resources/other.png)\n")
        (self.board("a") / "resources/other.png").write_text("image")
        shared = self.board("misc") / "backlog/card-00000002-shared.md"
        shared.write_text(shared.read_text().replace('module: "misc"', 'module: "misc"\naffected_modules: ["misc"]'))
        (self.board("a") / "backlog/notes.md").write_text("x\n")
        (self.board("b") / "completion/card-00000009-done.md").write_text(
            '---\nid: "CARD-00000009"\nmodule: "b"\n---\n\n## Acceptance criteria\n\n- [ ] Open.\n\n'
            "[Old link](gone.md)\n")
        shutil.copy(card, self.board("b") / "cancellation" / card.name)
        (self.root / "project/modules/z").mkdir()
        guide = self.root / "kanban-rememory/documentation/guide.md"
        guide.parent.mkdir()
        guide.write_text("[Missing](missing.md) [Anchor](#nowhere) `kanban-rememory/orchestrator/tools/gone.py`\n")
        os.symlink(self.root, self.board("a") / "resources/link")
        output = self.kr(self.root, "validate", expected=1)
        for finding in ("needs exactly one module field set to a", "attachment ../resources/other.png",
                        "affected_modules must list", "notes.md: expected card-NNNNNNNN",
                        "duplicate CARD-00000001", "project/modules/z: module missing", "missing link target missing.md",
                        "missing heading anchor #nowhere", "missing tool kanban-rememory/orchestrator/tools/gone.py", "symbolic link"):
            self.assertIn(finding, output)
        self.assertNotIn("gone.md", output)  # completed Cards keep the links of their time

    def test_phase_from_start_to_publish(self):
        for title, module in (("Alpha", "a"), ("Beta", "a"), ("Other", "b"), ("Dropped", "a")):
            self.kr(self.root, "new", title, "--module", module)
        self.commit(self.root, "Add Cards")
        root = self.root
        self.assertIn("Choose where to work", self.kr(root, "start", "CARD-00000001", expected=1))
        self.assertIn("dedicated branch", self.kr(root, "start", "CARD-00000001", "--release", expected=1))
        self.git(root, "switch", "-qc", "claude/phase-1")
        self.assertIn("from main", self.kr(root, "start", "CARD-00000001", "--main", expected=1))
        self.kr(root, "start", "CARD-00000001", "--release", "--bump", "minor")
        self.commit(root, "Start")
        self.git(root, "switch", "-qc", "other", "main")
        self.assertIn("runs on claude/phase-1", self.kr(root, "start", "CARD-00000003", expected=1))
        self.assertIn("runs on claude/phase-1", self.kr(root, "new", "Late", expected=1))
        self.git(root, "switch", "-q", "claude/phase-1")
        self.assertIn("belongs to b", self.kr(root, "start", "CARD-00000003", expected=1))
        self.assertIn("WIP limit", self.kr(root, "start", "CARD-00000002", expected=1))
        self.kr(root, "move", "CARD-00000001", "completion")
        self.kr(root, "start", "CARD-00000004")
        self.kr(root, "move", "CARD-00000004", "cancellation")  # abandoned inside the phase: skipped at closure
        self.kr(root, "start", "CARD-00000002")
        (root / "src.txt").write_text("change\n")
        self.assertIn("local changes", self.kr(root, "check", expected=1))
        self.commit(root, "Implement")
        moved = self.git(root, "commit-tree", "origin/main^{tree}", "-p", "origin/main", "-m", "Advance main")
        self.git(root, "push", "-q", "origin", f"{moved}:refs/heads/main")
        self.assertIn("Merge origin/main", self.kr(root, "check", expected=1))
        self.git(root, "merge", "-q", "--no-edit", "origin/main")
        self.kr(root, "check", "--", sys.executable, "-c", "pass", "--", sys.executable, "-c", "raise SystemExit(3)",
                expected=3)
        self.assertIn("verified: no", self.kr(root, "show"))
        (root / "src.txt").write_text("fixed\n")
        candidate = self.commit(root, "Fix\n\nCo-Authored-By: Fixture Agent <agent@example.invalid>")
        self.assertIn("is not verified", self.kr(root, "publish", "--summary", "S.", "--approval", "Yes", expected=1))
        self.assertIn(f"Verified revision: {candidate}", self.kr(root, "check", "--", sys.executable, "-c", "pass"))
        (root / "src.txt").write_text("unapproved\n")
        self.commit(root, "Change after approval")
        self.assertIn("only Cards and the journal: src.txt", self.kr(root, "publish", expected=1))
        self.git(root, "reset", "-q", "--hard", candidate)
        hook = self.base / "origin.git/hooks/pre-receive"
        hook.write_text("#!/bin/sh\nexit 1\n")
        hook.chmod(0o755)
        self.kr(root, "publish", "--summary", "Alpha and Beta.", "--approval", "Oui, fusionne", expected=1)
        hook.unlink()  # the push failed after the closing commit: publishing again must not close twice
        closing = self.git(root, "rev-parse", "HEAD")
        self.assertIn("Co-Authored-By: Fixture Agent <agent@example.invalid>", self.git(root, "log", "-1", "--format=%B"))
        output = self.kr(root, "publish", "--summary", "Alpha and Beta.", "--notify", "Chat", "--language", "fr")
        self.assertIn(f"Published {closing} on origin/main as v0.1.0", output)
        self.assertEqual(json.loads((root / "kanban-rememory.json").read_text())["version"], "0.1.0")
        self.assertEqual(self.git(root, "rev-parse", "v0.1.0^{commit}"), closing)
        self.assertEqual(self.git(root, "ls-remote", "origin", "refs/tags/v0.1.0").split()[0], self.git(root, "rev-parse", "v0.1.0"))
        self.assertIn("nothing was sent", output)  # no Telegram configuration in this HOME: the publication stands
        for task_id in ("CARD-00000001", "CARD-00000002"):
            self.assertEqual(self.card(root, task_id).read_text().count(
                f"verified candidate `{candidate}`: “Oui, fusionne”"), 1)
        self.assertNotIn("Merge approved", self.card(root, "CARD-00000004").read_text())
        journal = "".join(day.read_text() for day in (root / "project/rememory").glob("*.md"))
        self.assertEqual(journal.count("## a/CARD-00000001"), 1)
        self.assertRegex(journal, r"## a/CARD-00000001\n\nAlpha and Beta\.\n\nPhase Cards: CARD-00000001, "
                                  r"CARD-00000004, CARD-00000002\.\n\nDuration: .+ Tokens \(Claude Code\): unavailable\.")
        self.assertIn(f"Verified revision: `{candidate}`. [Card](<../modules/a/completion/", journal)
        self.assertEqual(self.git(root, "ls-remote", "origin", "refs/heads/main").split()[0], closing)
        self.assertEqual((self.git(root, "branch", "--show-current"), self.git(root, "rev-parse", "HEAD")),
                         ("main", closing))
        self.assertNotIn("claude/phase-1", self.git(root, "branch", "--list"))
        self.assertIn("Phase: none", self.kr(root, "show"))
        self.assertRegex(self.kr(root, "versions"), r"Current version: 0\.1\.0\nv0\.1\.0 \| \d{4}-\d\d-\d\d \| Close ")

    def test_phase_on_main_commits_there_and_publishes_without_a_tag(self):
        self.kr(self.root, "new", "Direct", "--module", "a")
        self.commit(self.root, "Add Card")
        root = self.root
        self.assertNotIn("Next:", self.kr(root, "show"))
        self.kr(root, "start", "CARD-00000001", "--main")
        self.assertIn("Next: commit the changes", self.kr(root, "show"))
        (root / "src.txt").write_text("change\n")
        candidate = self.commit(root, "Implement on main")
        self.assertIn("Next: run check", self.kr(root, "show"))
        self.kr(root, "check")
        self.assertIn("Next: ask for approval, then publish", self.kr(root, "show"))
        output = self.kr(root, "publish", "--summary", "Direct.", "--approval", "Oui")
        self.assertNotIn(" as v", output)
        self.assertEqual(self.git(root, "tag", "--list"), "")
        self.assertEqual(json.loads((root / "kanban-rememory.json").read_text())["version"], "0.0.0")
        self.assertEqual(self.git(root, "ls-remote", "origin", "refs/heads/main").split()[0],
                         self.git(root, "rev-parse", "HEAD"))
        self.assertEqual(self.git(root, "rev-parse", "HEAD~1"), candidate)
        self.assertIn("Phase: none", self.kr(root, "show"))

    def test_check_and_publish_refuse_unsafe_states(self):
        root = self.root
        self.kr(root, "new", "Direct", "--module", "a")
        self.commit(root, "Add Card")
        self.kr(root, "start", "CARD-00000001", "--main")
        (root / "project/modules/a/backlog/notes.md").write_text("x\n")
        self.commit(root, "Invalid record")
        self.kr(root, "check", expected=1)  # validate fails: nothing is verified
        self.assertIn("run check", self.kr(root, "show"))
        (root / "project/modules/a/backlog/notes.md").unlink()
        self.commit(root, "Fix record")
        self.kr(root, "check")
        self.assertIn("nonempty single lines", self.kr(root, "publish", "--summary", "a\nb", "--approval", "Oui", expected=1))
        self.assertIn("alert needs --summary", self.kr(root, "publish", "--notify", "Chat", expected=1))
        self.assertIn("Give --summary and --approval", self.kr(root, "publish", expected=1))
        configuration = self.base / "HOME/.config/kanban-rememory/telegram.json"
        configuration.parent.mkdir(parents=True)
        configuration.write_text("{}")  # configured Telegram: the delivery alert is automatic, so the summary is required
        self.assertIn("alert needs --summary", self.kr(root, "publish", "--approval", "Oui", expected=1))
        configuration.unlink()
        self.card(root, "CARD-00000001").open("a").write("Note.\n")
        self.commit(root, "Note")
        self.assertIn("lacks its closure", self.kr(root, "publish", "--summary", "S", "--approval", "Oui", expected=1))
        self.kr(root, "check")
        self.git(self.base, "clone", "-q", "-b", "main", "origin.git", "other")
        other = self.base / "other"
        (other / "elsewhere.txt").write_text("moved\n")
        self.commit(other, "Move origin")
        self.git(other, "push", "-q", "origin", "main")
        self.assertIn("origin/main moved", self.kr(root, "publish", "--summary", "S", "--approval", "Oui", expected=1))
        self.assertIn("Merge origin/main", self.kr(root, "check", expected=1))
        self.assertEqual(self.git(root, "ls-remote", "origin", "refs/heads/main").split()[0], self.git(other, "rev-parse", "HEAD"))

    def test_report_sums_durations_and_host_tokens_of_the_phase(self):
        start = datetime.fromisoformat("2026-11-15T10:00:00+01:00")
        end = datetime.fromisoformat("2026-11-15T11:30:00+01:00")
        history = ("- 2026-11-15T10:05:00+01:00 — Stage moved from `backlog` to `development`.\n"
                   "- 2026-11-15T10:20:00+01:00 — Stage moved from `development` to `completion`.\n")
        self.assertEqual(report.card_duration(history, ["development"], "completion"), "15 min")
        self.assertEqual(report.minutes(start, end), "1 h 30 min")
        work = self.base / "work"
        logs = self.base / "KR_CLAUDE_HOME/projects" / "".join(c if c.isalnum() else "-" for c in str(work))
        logs.mkdir(parents=True)
        usage = lambda n: {"input_tokens": n, "cache_creation_input_tokens": 2 * n,
                           "cache_read_input_tokens": 3 * n, "output_tokens": 4 * n}
        rows = [{"timestamp": "2026-11-15T08:59:59Z", "message": {"id": "old", "usage": usage(100)}},
                {"timestamp": "2026-11-15T09:10:00Z", "message": {"id": "m1", "usage": usage(1)}},
                {"timestamp": "2026-11-15T09:10:01Z", "message": {"id": "m1", "usage": usage(1)}},
                {"timestamp": "2026-11-15T09:20:00Z", "message": {"id": "m2", "usage": usage(2)}},
                {"timestamp": "2026-11-15T12:00:00Z", "message": {"id": "late", "usage": usage(100)}}]
        (logs / "s.jsonl").write_text("\n".join(map(json.dumps, rows)) + "\nnot json\n")
        rollout = self.base / "KR_CODEX_HOME/sessions/2026/11/15/rollout-x.jsonl"
        rollout.parent.mkdir(parents=True)
        count = lambda at, i, c, o: {"timestamp": at, "type": "event_msg", "payload": {"type": "token_count", "info": {
            "total_token_usage": {"input_tokens": i, "cached_input_tokens": c, "output_tokens": o}}}}
        rows = [{"timestamp": "2026-11-15T08:00:00Z", "type": "session_meta", "payload": {"cwd": str(work)}},
                count("2026-11-15T08:30:00Z", 100, 50, 10), count("2026-11-15T09:30:00Z", 300, 150, 40),
                count("2026-11-15T12:00:00Z", 900, 450, 90)]
        rollout.write_text("\n".join(map(json.dumps, rows)) + "\n")
        text = report.report(start, end, [("CARD-1", history)], ["development"], "completion", {work})
        self.assertIn("Duration: 1 h 30 min (CARD-1 15 min).", text)
        self.assertIn("Tokens (Claude Code): input 3, cache write 6, cache read 9, output 12.", text)
        self.assertIn("Tokens (Codex): input 200, cached input 100, output 30.", text)
        self.assertIn("Tokens (Claude Code): unavailable.", report.report(start, end, [], [], "", {self.base}))

    def test_build_kit_zips_the_committed_kit_files(self):
        spec = importlib.util.spec_from_file_location("build_kit", KIT / "kanban-rememory/orchestrator/tools/build-kit.py")
        build_kit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_kit)
        for name in ("AGENTS.md", "CLAUDE.md", "GUARDRAILS.md"):
            (self.root / name).write_text("kit\n")
        (self.root / "notes.md").write_text("not in the kit\n")
        self.commit(self.root, "Add kit files")
        archive = build_kit.build(self.root)
        self.assertEqual(archive, self.root / "dist/kanban-rememory-kit-0.0.0.zip")
        with zipfile.ZipFile(archive) as kit:
            names = set(kit.namelist())
        prefix = "kanban-rememory-kit-0.0.0/"
        self.assertIn(prefix + "AGENTS.md", names)
        self.assertIn(prefix + "kanban-rememory.json", names)
        self.assertIn(prefix + "kanban-rememory/orchestrator/tools/kr.py", names)
        self.assertFalse(any(name.endswith("notes.md") or "project/" in name for name in names))

    def test_init_previews_then_creates_the_boards_once(self):
        fresh = self.repository("fresh")
        self.assertIn("Preview only", self.kr(fresh, "init", self.proposal))
        self.assertFalse((fresh / "project").exists())
        bad = self.base / "bad.json"
        for change, message in (({"workflow": dict(WORKFLOW, stages=["backlog", "development", "completion"])},
                                 "stages"), ({"modules": ["a"]}, "include misc")):
            bad.write_text(json.dumps(dict(self.settings, **change)))
            self.assertIn(message, self.kr(fresh, "init", bad, expected=1))
        self.kr(fresh, "init", self.proposal, "--apply")
        self.assertEqual((fresh / "kanban-rememory.json").read_bytes(), self.proposal.read_bytes())
        self.assertTrue((self.board("a", fresh) / "resources/.gitkeep").is_file())
        self.assertIn("already exist", self.kr(fresh, "init", self.proposal, "--apply", expected=1))

    def test_config_file_holds_the_settings_and_picks_the_working_folder(self):
        fresh = self.repository("fresh")
        work = self.base / "work.json"
        work.write_text(json.dumps(dict(self.settings, directory="work", kit="0.3.0")))
        self.kr(fresh, "init", work, "--apply")
        self.assertEqual((fresh / "kanban-rememory.json").read_bytes(), work.read_bytes())
        self.assertTrue((fresh / "work/rememory").is_dir())
        self.assertFalse((fresh / "project").exists())
        self.assertIn("Kanban validation passed", self.kr(fresh, "validate"))
        for change in ({"directory": "../x"}, {"directory": "kanban-rememory"}, {"directory": ".git"}, {"directory": ""},
                       {"kit": "x"}, {"other": 1}):
            (fresh / "kanban-rememory.json").write_text(json.dumps(dict(self.settings, **change)))
            self.assertIn("Invalid kanban-rememory.json", self.kr(fresh, "validate", expected=1))
        (fresh / "kanban-rememory.json").write_text("[]")
        self.assertIn("Invalid kanban-rememory.json", self.kr(fresh, "validate", expected=1))


if __name__ == "__main__":
    unittest.main()
