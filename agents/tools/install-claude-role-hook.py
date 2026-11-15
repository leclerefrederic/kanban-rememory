"""Enable or disable the optional Claude Code role-limit hook in this project."""

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
COMMAND = 'python3 "$CLAUDE_PROJECT_DIR/agents/tools/role-limit-hook.py"'
MATCHER = "Read|Glob|Grep|Edit|Write|MultiEdit|NotebookEdit|Bash"
NAMES = ("developer.md", "writer.md", "tester.md")
SETTINGS = ROOT / ".claude/settings.json"
# Exact distributed adapters, before the canonical role rename (9e2c86a and 7b2e8b4).
LEGACY_AGENTS = {
    "development-agent.md": ("developer.md", {
        "079460649c351f3b13f8bccd6a6193e6516464153f3b440649edba452c1aae3b",
        "8119b464c889ac78deeb6ca2455f4d5578ec24430d87beffe9fdf63189464a6c",
    }),
    "specification-agent.md": ("writer.md", {
        "e2bc777770e66578affda24c9b1436b0ec230bbc077b4ff023bdd924dd115d20",
        "28c92356d300eca3dbe036cf358aa5ad36c5215f44ebb1b35b299e24f8798b59",
    }),
    "tester.md": ("tester.md", {
        "d1999f6f3189b2d174d4da57bddadabdd649bb3dac6430535a2b14a4776b8378",
    }),
}


def local_path(path):
    """Do not read through or mutate a linked destination or one of its parents."""
    if path.is_symlink():
        return False
    for parent in path.parents:
        if parent == ROOT:
            return True
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            return False
    return False


def recognized(path, digests):
    return local_path(path) and path.is_file() and sha256(path.read_bytes()).hexdigest() in digests


def kept(path):
    print(f"Kept customized or linked adapter {path.relative_to(ROOT)}. Review it before replacing or removing.",
          file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remove", action="store_true", help="remove the hook and unchanged installed agents")
    parser.add_argument("--apply", action="store_true", help="write the changes; the default is a preview")
    args = parser.parse_args()
    source_dir = ROOT / "agents/hosts/claude/agents"
    sources = {name: source_dir / name for name in NAMES}
    # Preflight the complete source set and settings before planning any mutation.
    if any(not local_path(path) or not path.is_file() for path in sources.values()):
        parser.exit(1, "Missing or linked adapter sources in agents/hosts/claude/agents/. Nothing was changed.\n")
    hook_path = ROOT / "agents/tools/role-limit-hook.py"
    policy_paths = [ROOT / "agents/roles" / name for name in NAMES]
    required = [hook_path, ROOT / "agents/tools/kanban/files.py", *policy_paths]
    if any(not local_path(path) or not path.is_file() for path in required):
        parser.exit(1, "Missing or linked canonical role policies or hook dependencies. Nothing was changed.\n")
    try:
        spec = importlib.util.spec_from_file_location("role_limit_hook", hook_path)
        hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook)
        roles = hook.load_roles(ROOT)
        if any(hook.header_value(source.read_text(), "name") != Path(name).stem
               for name, source in sources.items()):
            raise ValueError
        if any(roles.get(Path(name).stem, {}).get("file") != f"agents/roles/{name}" for name in NAMES):
            raise ValueError
    except (ImportError, OSError, TypeError, ValueError):
        parser.exit(1, "Invalid or duplicate canonical role policies or adapter names. Nothing was changed.\n")
    if not local_path(SETTINGS):
        parser.exit(1, "Linked .claude settings path. Nothing was changed.\n")
    try:
        settings = json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}
        if not isinstance(settings, dict) or not isinstance(settings.get("hooks", {}), dict):
            raise ValueError
        groups = settings.get("hooks", {}).get("PreToolUse", [])
        if (not isinstance(groups, list) or any(not isinstance(group, dict)
                or not isinstance(group.get("hooks", []), list)
                or any(not isinstance(hook, dict) for hook in group.get("hooks", [])) for group in groups)):
            raise ValueError
    except (OSError, ValueError):
        parser.exit(1, ".claude/settings.json must contain valid settings and hook groups. Nothing was changed.\n")
    present = any(hook.get("command") == COMMAND for group in groups for hook in group.get("hooks", []))
    new_groups = groups
    if args.remove:
        new_groups = []
        for group in groups:
            remaining = [hook for hook in group.get("hooks", []) if hook.get("command") != COMMAND]
            if remaining == group.get("hooks", []):
                new_groups.append(group)
            elif remaining:
                new_groups.append({**group, "hooks": remaining})
    elif not present:
        new_groups = groups + [{"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND}]}]

    copies, removals, conflicts = [], [], []
    ready = set()
    for name, source in sources.items():
        target = ROOT / ".claude/agents" / name
        old_digests = set().union(*(digests for new, digests in LEGACY_AGENTS.values() if new == name))
        digests = old_digests | {sha256(source.read_bytes()).hexdigest()}
        if not local_path(target):
            kept(target)
            conflicts.append(target)
        elif not target.exists():
            if not args.remove:
                copies.append((source, target))
                ready.add(name)
        elif recognized(target, digests):
            if args.remove:
                removals.append(target)
            else:
                ready.add(name)
                if target.read_bytes() != source.read_bytes():
                    copies.append((source, target))
        else:
            kept(target)
            conflicts.append(target)

    for old, (new, digests) in LEGACY_AGENTS.items():
        paths = [] if old == new else [ROOT / ".claude/agents" / old]
        if not args.remove:
            paths.append(ROOT / "agents/claude/agents" / old)
        for path in paths:
            if not local_path(path):
                kept(path)
            elif path.exists():
                if not recognized(path, digests):
                    kept(path)
                elif args.remove or new in ready or path.is_relative_to(ROOT / "agents"):
                    removals.append(path)
                else:
                    print(f"Kept {path.relative_to(ROOT)} until {new} is reconciled.", file=sys.stderr)

    plan = []
    if new_groups != groups:
        plan.append(("remove" if args.remove else "add") + " the role-limit hook in .claude/settings.json")
    plan += [f"copy {source.relative_to(ROOT)} to {target.relative_to(ROOT)}" for source, target in copies]
    plan += [f"remove unchanged {path.relative_to(ROOT)}" for path in removals]
    if not plan:
        print("Nothing to change." if not conflicts else "Customized adapters require review; nothing was changed.")
        return int(bool(conflicts))
    if not args.apply:
        print("\n".join("Will " + item for item in plan))
        print("Preview only. Rerun with --apply to make these changes.")
        return int(bool(conflicts))
    if new_groups != groups:
        hooks = settings.setdefault("hooks", {})
        if new_groups:
            hooks["PreToolUse"] = new_groups
        else:
            hooks.pop("PreToolUse", None)
            if not hooks:
                settings.pop("hooks")
        SETTINGS.parent.mkdir(parents=True, exist_ok=True)
        SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")
    for source, target in copies:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    for path in removals:
        path.unlink()
    print("\n".join("Done: " + item for item in plan))
    if conflicts:
        print("Installation is incomplete: reconcile the preserved customized adapters.", file=sys.stderr)
    return int(bool(conflicts))


if __name__ == "__main__":
    raise SystemExit(main())
