"""Enable or disable the optional Claude Code role-limit hook in this project."""

import argparse
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
COMMAND = 'python3 "$CLAUDE_PROJECT_DIR/agents/tools/role-limit-hook.py"'
MATCHER = "Read|Glob|Grep|Edit|Write|MultiEdit|NotebookEdit|Bash"
SOURCES = sorted((ROOT / "agents/claude/agents").glob("*.md"))
SETTINGS = ROOT / ".claude/settings.json"


def ours(group):
    return any(hook.get("command") == COMMAND for hook in group.get("hooks", []))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--remove", action="store_true", help="remove the hook and its named agents")
    parser.add_argument("--apply", action="store_true", help="write the changes; the default is a preview")
    args = parser.parse_args()
    try:
        settings = json.loads(SETTINGS.read_text()) if SETTINGS.exists() else {}
    except json.JSONDecodeError:
        sys.exit(f"{SETTINGS.relative_to(ROOT)} is not valid JSON. Fix it first; nothing was changed.")
    groups = settings.get("hooks", {}).get("PreToolUse", [])
    others = [group for group in groups if not ours(group)]
    plan = []
    if args.remove:
        if len(others) != len(groups):
            plan.append(f"remove the role-limit hook from {SETTINGS.relative_to(ROOT)}")
        plan += [f"remove .claude/agents/{path.name}" for path in SOURCES if (ROOT / ".claude/agents" / path.name).exists()]
        new_groups = others
    else:
        if len(others) == len(groups):
            plan.append(f"add the role-limit hook to {SETTINGS.relative_to(ROOT)}")
        plan += [f"copy {path.name} to .claude/agents/" for path in SOURCES
                 if not (ROOT / ".claude/agents" / path.name).exists()
                 or (ROOT / ".claude/agents" / path.name).read_bytes() != path.read_bytes()]
        new_groups = others + [{"matcher": MATCHER, "hooks": [{"type": "command", "command": COMMAND}]}]
        if len(others) != len(groups):
            new_groups = groups  # The hook is already there: keep its current place.
    if not plan:
        print("Nothing to change: the role-limit hook is already " + ("absent." if args.remove else "installed."))
        return 0
    print("\n".join(("Will " if not args.apply else "Done: ") + item for item in plan))
    if not args.apply:
        print("Preview only. Rerun with --apply to make these changes.")
        return 0
    hooks = settings.setdefault("hooks", {})
    if new_groups:
        hooks["PreToolUse"] = new_groups
    else:
        hooks.pop("PreToolUse", None)
        if not hooks:
            settings.pop("hooks")
    if settings or SETTINGS.exists():
        SETTINGS.parent.mkdir(parents=True, exist_ok=True)
        SETTINGS.write_text(json.dumps(settings, indent=2) + "\n")
    for path in SOURCES:
        target = ROOT / ".claude/agents" / path.name
        if args.remove:
            target.unlink(missing_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
