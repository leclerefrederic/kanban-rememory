"""Isolated role-identity and discovery migration checks; no native host or network calls."""

from contextlib import redirect_stderr
from hashlib import sha256
import importlib.util
from io import StringIO
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[2]
FROZEN = json.loads((KIT / "agents/tools/fixtures/role-migration-308b747.json").read_text())["files"]


def module(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), KIT / "agents/tools" / f"{name}.py")
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


class MigrationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for name in ("install-claude-role-hook.py", "sync-skills.py", "role-limit-hook.py"):
            self.write("agents/tools/" + name, (KIT / "agents/tools" / name).read_text())
        shutil.copytree(KIT / "agents/roles", self.root / "agents/roles")
        shutil.copytree(KIT / "agents/tools/kanban", self.root / "agents/tools/kanban",
                        ignore=shutil.ignore_patterns("__pycache__"))
        self.write("agents/VERSION", "fixture\n")
        self.sources = "agents/hosts/claude/agents"
        shutil.copytree(KIT / self.sources, self.root / self.sources)
        shutil.copytree(KIT / "agents/skills", self.root / "agents/skills")

    def write(self, path, text):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def run_tool(self, name, *args, expected=0):
        result = subprocess.run([sys.executable, str(self.root / "agents/tools" / name), *args],
                                cwd=self.root, text=True, capture_output=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result.stdout + result.stderr

    def snapshot(self):
        return {str(path.relative_to(self.root)): ("link:" + os.readlink(path) if path.is_symlink()
                else path.read_bytes()) for path in self.root.rglob("*") if path.is_symlink() or path.is_file()}

    def install(self, *args, expected=0):
        return self.run_tool("install-claude-role-hook.py", *args, expected=expected)

    def sync(self, *args, expected=0):
        return self.run_tool("sync-skills.py", *args, expected=expected)

    def test_frozen_bytes_are_actual_recognized_copies(self):
        installer = module("install-claude-role-hook")
        sync = module("sync-skills")
        for path, text in FROZEN.items():
            digest = sha256(text.encode()).hexdigest()
            if path.startswith("agents/claude/agents/"):
                self.assertIn(digest, installer.LEGACY_AGENTS[Path(path).name][1])
            elif Path(path).parent.name in sync.LEGACY_SKILLS:
                self.assertIn(digest, sync.LEGACY_SKILLS[Path(path).parent.name][1])
            else:
                self.assertIn(digest, sync.SHIPPED_SKILLS[Path(path).parent.name])

    def test_fresh_preview_install_and_remove_are_idempotent(self):
        before = self.snapshot()
        self.assertIn("Preview only", self.install())
        self.assertEqual(before, self.snapshot())
        self.install("--apply")
        for name in ("developer.md", "writer.md", "tester.md"):
            self.assertEqual((self.root / ".claude/agents" / name).read_bytes(),
                             (self.root / self.sources / name).read_bytes())
        installed = self.snapshot()
        self.assertIn("Nothing to change", self.install("--apply"))
        self.assertEqual(installed, self.snapshot())
        self.install("--remove", "--apply")
        self.assertEqual(list((self.root / ".claude/agents").iterdir()), [])
        removed = self.snapshot()
        self.assertIn("Nothing to change", self.install("--remove", "--apply"))
        self.assertEqual(removed, self.snapshot())

    def test_upgrade_retires_real_legacy_sources_and_preserves_shared_hooks(self):
        installer = module("install-claude-role-hook")
        other = {"type": "command", "command": "echo project"}
        group = {"matcher": "Bash", "hooks": [other, {"type": "command", "command": installer.COMMAND}]}
        settings = self.write(".claude/settings.json", json.dumps({"model": "project-model",
                              "hooks": {"PreToolUse": [group], "Stop": []}}))
        for path, text in FROZEN.items():
            if path.startswith("agents/claude/agents/"):
                self.write(path, text)
                self.write(".claude/agents/" + Path(path).name, text)
        extra = self.write("agents/claude/agents/notes.txt", "project-owned\n")
        before = self.snapshot()
        self.install()
        self.assertEqual(before, self.snapshot())
        self.install("--apply")
        self.assertEqual(json.loads(settings.read_text())["hooks"]["PreToolUse"], [group])
        for name in ("development-agent.md", "specification-agent.md"):
            self.assertFalse((self.root / ".claude/agents" / name).exists())
        self.assertEqual(list((self.root / "agents/claude/agents").iterdir()), [extra])
        self.assertIn("Nothing to change", self.install("--apply"))
        self.install("--remove", "--apply")
        self.assertEqual(json.loads(settings.read_text()), {"model": "project-model", "hooks": {
            "PreToolUse": [{"matcher": "Bash", "hooks": [other]}], "Stop": []}})
        self.assertEqual(extra.read_text(), "project-owned\n")

    def test_missing_or_linked_sources_and_invalid_settings_write_nothing(self):
        source = self.root / self.sources / "tester.md"
        content = source.read_bytes()
        source.unlink()
        before = self.snapshot()
        self.assertIn("Nothing was changed", self.install("--apply", expected=1))
        self.assertEqual(before, self.snapshot())
        outside = self.write("outside.md", content.decode())
        source.symlink_to(outside)
        before = self.snapshot()
        self.install("--apply", expected=1)
        self.assertEqual(before, self.snapshot())
        source.unlink()
        source.write_bytes(content)
        self.write(".claude/settings.json", '{"hooks": {"PreToolUse": "not a list"}}')
        before = self.snapshot()
        self.install("--apply", expected=1)
        self.assertEqual(before, self.snapshot())

    def test_duplicate_policy_is_reported_before_installation_changes_anything(self):
        self.write("agents/roles/duplicate.md", (self.root / "agents/roles/writer.md").read_text())
        before = self.snapshot()
        self.assertIn("duplicate canonical role policies", self.install("--apply", expected=1))
        self.assertEqual(before, self.snapshot())

    def test_custom_current_legacy_and_source_adapters_survive_install_and_remove(self):
        current = self.write(".claude/agents/developer.md", "project developer\n")
        old = self.write(".claude/agents/specification-agent.md", "project writer\n")
        source = self.write("agents/claude/agents/development-agent.md", "project source\n")
        recognized = self.write(".claude/agents/development-agent.md",
                               FROZEN["agents/claude/agents/development-agent.md"])
        output = self.install("--apply", expected=1)
        self.assertIn("customized", output.lower())
        self.assertIn("until developer.md is reconciled", output)
        self.assertEqual(current.read_text(), "project developer\n")
        self.assertTrue(recognized.exists())
        self.install("--remove", "--apply", expected=1)
        self.assertEqual(current.read_text(), "project developer\n")
        self.assertEqual(old.read_text(), "project writer\n")
        self.assertEqual(source.read_text(), "project source\n")
        self.assertFalse(recognized.exists())

    def test_linked_destination_parent_is_not_traversed(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = self.write("outside/developer.md", "outside content\n")
        (self.root / ".claude").mkdir()
        (self.root / ".claude/agents").symlink_to(outside, target_is_directory=True)
        self.install("--apply", expected=1)
        self.assertEqual(list(outside.iterdir()), [marker])
        self.assertEqual(marker.read_text(), "outside content\n")
        self.install("--remove", "--apply", expected=1)
        self.assertTrue((self.root / ".claude/agents").is_symlink())

    def test_sync_upgrades_real_current_and_legacy_bytes_without_changing_other_skills(self):
        own = self.write(".agents/skills/own/SKILL.md", "own\n")
        for path, text in FROZEN.items():
            if path.startswith("agents/skills/"):
                self.write(".agents/skills/" + Path(path).parent.name + "/SKILL.md", text)
                if "kanban-rememory-" in path:
                    self.write(path, text)
        before = self.snapshot()
        self.assertIn("retire legacy copy", self.sync("--check", "--target", "codex", expected=1))
        self.assertEqual(before, self.snapshot())
        self.sync("--target", "codex")
        for source in (self.root / "agents/skills").iterdir():
            self.assertFalse(source.name.startswith("kanban-rememory-"))
            self.assertEqual((self.root / ".agents/skills" / source.name / "SKILL.md").read_bytes(),
                             (source / "SKILL.md").read_bytes())
        self.assertFalse((self.root / ".claude/skills").exists())
        self.assertEqual(own.read_text(), "own\n")
        self.assertIn("updated 0", self.sync("--target", "codex"))
        self.assertIn("match kit", self.sync("--check", "--target", "codex"))

    def test_sync_preserves_modified_current_augmented_legacy_and_sources(self):
        current = self.write(".agents/skills/kr-developer/SKILL.md", "project developer\n")
        extra = self.write(".agents/skills/kr-writer/extra.txt", "project resource\n")
        self.write(".agents/skills/kr-writer/SKILL.md", FROZEN["agents/skills/kr-writer/SKILL.md"])
        old = self.write(".agents/skills/kanban-rememory-tester/SKILL.md", "project tester\n")
        source = self.write("agents/skills/kanban-rememory-tester/SKILL.md", "project source\n")
        legacy_dev = self.write(".agents/skills/kanban-rememory-development-agent/SKILL.md",
                               FROZEN["agents/skills/kanban-rememory-development-agent/SKILL.md"])
        self.sync("--target", "codex", expected=1)
        self.assertEqual(current.read_text(), "project developer\n")
        self.assertEqual(extra.read_text(), "project resource\n")
        self.assertEqual(old.read_text(), "project tester\n")
        self.assertEqual(source.read_text(), "project source\n")
        self.assertTrue(legacy_dev.exists())  # No replacement was installed for the customized Developer.
        self.assertFalse((self.root / ".agents/skills/kanban-rememory-tester/extra.txt").exists())
        self.assertIn("customized; review required", self.sync("--check", "--target", "codex", expected=1))

    def test_sync_missing_marker_or_linked_source_does_not_partially_update(self):
        (self.root / "agents/VERSION").unlink()
        before = self.snapshot()
        self.sync(expected=1)
        self.assertEqual(before, self.snapshot())
        self.write("agents/VERSION", "fixture\n")
        source = self.root / "agents/skills/kr-writer/SKILL.md"
        source.unlink()
        source.symlink_to(self.root / "agents/skills/kr-developer/SKILL.md")
        before = self.snapshot()
        self.sync(expected=1)
        self.assertEqual(before, self.snapshot())

    def test_sync_keeps_linked_destinations_and_does_not_follow_parent_links(self):
        outside = self.root / "outside"
        outside.mkdir()
        marker = self.write("outside/marker", "private\n")
        (self.root / ".agents").mkdir()
        (self.root / ".agents/skills").symlink_to(outside, target_is_directory=True)
        self.sync("--target", "codex", expected=1)
        self.assertEqual(list(outside.iterdir()), [marker])
        self.assertEqual(marker.read_text(), "private\n")

    def role_hook(self):
        sys.path.insert(0, str(KIT / "agents/tools"))
        try:
            hook = module("role-limit-hook")
        finally:
            sys.path.pop(0)
        return hook

    def test_old_and_new_sessions_have_the_same_policy_and_unknowns_stay_unrestricted(self):
        hook = self.role_hook()
        roles = hook.load_roles(self.root)
        self.assertIn("developer", roles)
        self.assertIn("writer", roles)
        for old, new in hook.ROLE_ALIASES.items():
            cases = [("Read", {"file_path": "project/specs/draft/x.md"}),
                     ("Read", {"file_path": "src/x.py"}),
                     ("Write", {"file_path": "src/x.py"}),
                     ("Write", {"file_path": "project/kanban/backlog/card-1.md"}),
                     ("Write", {"file_path": "project/kanban/development/card-1.md"}),
                     ("Bash", {"command": "git status"})]
            decisions = []
            for tool, fields in cases:
                canonical = hook.decide(roles, new, self.root, tool, fields, str(self.root))
                self.assertEqual(canonical, hook.decide(roles, old, self.root, tool, fields, str(self.root)))
                decisions.append(canonical)
            self.assertTrue(any(result is None for result in decisions))
            self.assertTrue(any(result is not None for result in decisions))
        for name in (None, "", "Explore", "unrelated-agent"):
            self.assertIsNone(hook.decide(roles, name, self.root, "Write", {"file_path": "src/x.py"}, str(self.root)))

    def test_hook_command_reads_old_and_new_session_ids(self):
        self.role_hook()
        outputs = []
        for identity in ("writer", "specification-agent"):
            event = {"agent_type": identity, "cwd": str(self.root), "tool_name": "Bash",
                     "tool_input": {"command": "git status"}}
            result = subprocess.run([sys.executable, str(KIT / "agents/tools/role-limit-hook.py")],
                                    input=json.dumps(event), cwd=self.root, text=True, capture_output=True,
                                    env={**os.environ, "CLAUDE_PROJECT_DIR": str(self.root),
                                         "PYTHONDONTWRITEBYTECODE": "1"})
            self.assertEqual(result.returncode, 0, result.stderr)
            output = json.loads(result.stdout)["hookSpecificOutput"]
            self.assertEqual(output["permissionDecision"], "deny")
            outputs.append(output)
        self.assertEqual(outputs[0], outputs[1])

    def module_manifest(self, two=True):
        modules = {"a": {"workspace": "tracking/a"}}
        if two:
            modules["b"] = {"workspace": "tracking/b"}
        self.write("project.json", json.dumps({
            "schema_version": 1, "project": {"id": "fixture", "name": "Fixture"},
            "shared": {"memory": "tracking/global", "sources": ["src"]}, "modules": modules,
            "execution": {"active_deliveries_per_module": 1, "branch_required": True,
                          "worktree_required": True, "concurrent_integrations": 1},
        }))

    def test_scoped_role_paths_use_existing_permissions(self):
        hook = self.role_hook()
        self.module_manifest()
        roles = hook.load_roles(self.root)
        scope, chosen = hook.scoped_project(self.root, "a")

        def allowed(role, verb, path):
            return hook.decide(roles, role, self.root, verb, {"file_path": path},
                               str(self.root), scope, chosen) is None

        for role in ("writer", "tester", "developer"):
            self.assertTrue(allowed(role, "Read", "project.json"))
            self.assertTrue(allowed(role, "Read", "tracking/global/2026-11-15.md"))
            self.assertFalse(allowed(role, "Write", "tracking/b/kanban/backlog/card-1.md"))
            self.assertFalse(allowed(role, "Write", "project/kanban/backlog/card-1.md"))
            self.assertFalse(allowed(role, "Write", "project.json"))
        self.assertTrue(allowed("writer", "Write", "tracking/a/specs/draft/spec.md"))
        self.assertTrue(allowed("writer", "Write", "tracking/a/kanban/backlog/card-1.md"))
        self.assertFalse(allowed("writer", "Write", "tracking/a/kanban/development/card-1.md"))
        self.assertFalse(allowed("writer", "Write", "src/shared.py"))
        self.assertTrue(allowed("developer", "Write", "src/shared.py"))
        self.assertTrue(allowed("developer", "Write", "tracking/global/2026-11-15.md"))
        self.assertTrue(allowed("developer", "Read", "tracking/a/specs/approved/spec.md"))
        self.assertFalse(allowed("developer", "Read", "tracking/a/specs/draft/spec.md"))
        self.assertFalse(allowed("developer", "Write", "tracking/a/specs/approved/spec.md"))
        self.assertTrue(allowed("tester", "Write", "tracking/a/batches/batch-001/tests.md"))
        self.assertFalse(allowed("tester", "Write", "tracking/a/batches/batch-001/description.md"))
        self.assertFalse(allowed("tester", "Read", "tracking/a/specs/ready/spec.md"))
        self.assertIsNotNone(hook.decide(roles, "developer", self.root, "Bash",
                                        {"command": "cat tracking/a/specs/draft/spec.md"},
                                        str(self.root), scope, chosen))
        self.assertIsNotNone(hook.decide(roles, "developer", self.root, "Grep", {"path": "tracking"},
                                        str(self.root), scope, chosen))

    def test_hook_checks_normal_module_invocation(self):
        self.module_manifest()
        event = {"agent_type": "writer", "cwd": str(self.root), "tool_name": "Write",
                 "tool_input": {"file_path": "tracking/a/kanban/backlog/card-1.md"}}
        environment = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.root), "PYTHONDONTWRITEBYTECODE": "1"}
        environment.pop("KR_MODULE", None)

        def run(**overrides):
            result = subprocess.run([sys.executable, str(self.root / "agents/tools/role-limit-hook.py")],
                                    input=json.dumps(event), cwd=self.root, text=True, capture_output=True,
                                    env={**environment, **overrides})
            self.assertEqual(result.returncode, 0, result.stderr)
            return result.stdout

        self.assertIn("Choose a module explicitly", run())
        self.assertIn("Unknown module", run(KR_MODULE="unknown"))
        self.assertIn("permissionDecision", run(KR_MODULE="b"))
        self.assertEqual(run(KR_MODULE="a"), "")
        self.module_manifest(two=False)
        self.assertEqual(run(), "")

    def test_module_records_use_control_worktree(self):
        hook = self.role_hook()
        self.module_manifest()
        roles = hook.load_roles(self.root)
        project, chosen = hook.scoped_project(self.root, "a")
        local = self.root.parent / "separate-candidate-worktree"
        record = "tracking/a/kanban/backlog/card-1.md"
        allowed = hook.decide(roles, "writer", local, "Write",
                              {"file_path": str(self.root / record)}, str(local), project, chosen)
        stale = hook.decide(roles, "writer", local, "Write",
                            {"file_path": record}, str(local), project, chosen)
        self.assertIsNone(allowed)
        self.assertIsNotNone(stale)

    def test_legacy_only_upgrade_uses_aliases_and_canonical_policy_wins_when_present(self):
        hook = self.role_hook()
        writer = self.root / "agents/roles/writer.md"
        canonical = writer.read_text()
        writer.unlink()
        old = self.write("agents/roles/specification-agent.md",
                         canonical.replace('role: "writer"', 'role: "specification-agent"', 1))
        roles = hook.load_roles(self.root)
        self.assertIsNotNone(hook.decide(roles, "specification-agent", self.root, "Bash",
                                        {"command": "git status"}, str(self.root)))
        writer.write_text(canonical)
        old.write_text(old.read_text().replace('git: "forbidden"', 'git: "allowed"'))
        before = old.read_bytes()
        output = StringIO()
        with redirect_stderr(output):
            roles = hook.load_roles(self.root)
        self.assertIn("canonical policy", output.getvalue())
        self.assertEqual(old.read_bytes(), before)
        self.assertIsNotNone(hook.decide(roles, "specification-agent", self.root, "Bash",
                                        {"command": "git status"}, str(self.root)))
        self.write("agents/roles/duplicate.md", canonical)
        with self.assertRaisesRegex(ValueError, "Duplicate role writer"):
            hook.load_roles(self.root)


if __name__ == "__main__":
    unittest.main()
