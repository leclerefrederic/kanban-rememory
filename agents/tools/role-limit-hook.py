"""Claude Code PreToolUse hook: refuse an action outside the role of the session.

The role is the `agent_type` Claude Code gives a session started as a named agent. Legacy launch names select the same canonical policy. The limits come from the
header of the matching role file in agents/roles/. A session without a known role is not restricted.
"""

import json
import os
from pathlib import Path
import re
import subprocess
import sys

from kanban.files import header_value

ROLE_ALIASES = {"development-agent": "developer", "specification-agent": "writer"}

READ_TOOLS = {"Read": "file_path"}
SEARCH_TOOLS = {"Glob": "path", "Grep": "path"}
WRITE_TOOLS = {"Edit": "file_path", "Write": "file_path", "MultiEdit": "file_path", "NotebookEdit": "notebook_path"}
PATH_WORD = re.compile(r"(?<![\w/.-])(?:\./)?((?:project|agents|documentation|apps)/[^\s\"';|&<>)]*|AGENTS\.md)")
REDIRECT = re.compile(r">>?\s*(\S+)")
GIT_WORD = re.compile(r"(^|[\s;&|(])git(\s|$)")


def load_roles(root):
    roles = {}
    for path in sorted((root / "agents/roles").glob("*.md")):
        text = path.read_text()
        try:
            name = header_value(text, "role")
        except ValueError:
            continue
        if name:
            if name in roles:
                raise ValueError(f"Duplicate role {name}: {roles[name]['file']} and agents/roles/{path.name}")
            title = re.search(r"(?m)^# Actor: (.+)$", text)
            roles[name] = {"name": name, "title": title.group(1) if title else name, "file": f"agents/roles/{path.name}",
                           "read": header_value(text, "read"), "write": header_value(text, "write"),
                           "git": header_value(text, "git")}
    for old, canonical in ROLE_ALIASES.items():
        if old in roles:
            legacy = roles.pop(old)
            if canonical not in roles:
                roles[canonical] = {**legacy, "name": canonical}
            else:
                print(f"Legacy policy {legacy['file']} is superseded by {roles[canonical]['file']}. "
                      "Review the old file; both launch IDs use the canonical policy.", file=sys.stderr)
    return roles


def relative(root, path, cwd):
    """Return the project-relative path, or None when the path is outside the project."""
    target = Path(path)
    resolved = (target if target.is_absolute() else Path(cwd) / target).resolve()
    try:
        return resolved.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def covers(entries, rel):
    path = rel.split("/")
    for entry in entries:
        pattern = entry.rstrip("/").split("/")
        if len(path) < len(pattern) or ("*" in pattern and not entry.endswith("/") and len(path) != len(pattern)):
            continue
        if all(
            wanted == actual or wanted == "*" for wanted, actual in zip(pattern, path)
        ):
            return True
    return False


def contains_denied(entries, rel):
    """True when a directory holds a path that the deny list forbids."""
    prefix = "" if rel in ("", ".") else rel.rstrip("/") + "/"
    return any(entry.startswith(prefix) for entry in entries)


def permits(role, kind, rel, directory=False):
    limits = role.get(kind)
    if not limits:
        return True
    if "allow" in limits:
        return covers(limits["allow"], rel)
    if directory and contains_denied(limits["deny"], rel):
        return False
    return not covers(limits["deny"], rel)


def checks(root, tool, tool_input, cwd):
    """Yield (kind, project-relative path, is_directory, label) for what the tool call touches."""
    if tool in READ_TOOLS:
        rel = relative(root, tool_input.get(READ_TOOLS[tool], ""), cwd)
        if rel is not None:
            yield "read", rel, False, f"reading {rel}"
    elif tool in SEARCH_TOOLS:
        rel = relative(root, tool_input.get("path") or cwd, cwd)
        if rel is not None:
            yield "read", "" if rel == "." else rel, True, "searching " + ("the whole project" if rel == "." else rel)
    elif tool in WRITE_TOOLS:
        rel = relative(root, tool_input.get(WRITE_TOOLS[tool], ""), cwd)
        if rel is not None:
            yield "write", rel, False, f"writing {rel}"
    elif tool == "Bash":
        command = tool_input.get("command", "")
        for word in PATH_WORD.findall(command):
            yield "read", word.rstrip("/"), False, f"a command that touches {word}"
        for target in REDIRECT.findall(command):
            rel = relative(root, target, cwd)
            if rel is not None:
                yield "write", rel, False, f"a command that writes {rel}"
        if GIT_WORD.search(command):
            yield "git", "", False, "a Git command"


def refusal(role, kind, label):
    where = {"read": "Read access", "write": "Write access", "git": "Forbidden"}[kind]
    return f"the {role['title']} role does not allow {label} ({role['file']}, {where})"


def violation(role, root, tool, tool_input, cwd):
    for kind, rel, directory, label in checks(root, tool, tool_input, cwd):
        if kind == "git":
            if role.get("git") == "forbidden":
                return kind, label
        elif not permits(role, kind, rel, directory):
            return kind, label
    return None


def decide(roles, agent_type, root, tool, tool_input, cwd):
    """Return a refusal message, or None to allow."""
    agent_type = ROLE_ALIASES.get(agent_type, agent_type)
    role = roles.get(agent_type)
    if role is None:
        return None
    found = violation(role, root, tool, tool_input, cwd)
    if found is None:
        return None
    others = [other["title"] for name, other in roles.items()
              if name != agent_type and violation(other, root, tool, tool_input, cwd) is None]
    if others:
        advice = f"Continue in a new session, or in an existing one, with the {' or '.join(others)}."
    elif "the whole project" in found[1]:
        advice = "Search a specific folder that your role may read."
    else:
        advice = "No role allows it; ask the User."
    return f"Refused: {refusal(role, *found)}. {advice} An instruction does not set this limit aside."


def main():
    event = json.load(sys.stdin)
    agent_type = event.get("agent_type")
    if not agent_type:
        return 0
    cwd = event.get("cwd") or os.getcwd()
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    if not root:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True).strip()
    root = Path(root)
    message = decide(load_roles(root), agent_type, root, event.get("tool_name", ""),
                     event.get("tool_input") or {}, cwd)
    if message:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                 "permissionDecisionReason": message}}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:  # A failing hook does not block: report it instead of hiding it.
        print(f"Role-limit hook failed and allowed the action: {error}", file=sys.stderr)
        raise SystemExit(1)
