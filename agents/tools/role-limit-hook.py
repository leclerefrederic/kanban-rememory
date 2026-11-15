"""Claude Code PreToolUse hook: refuse an action outside the role of the session.

The role is the `agent_type` Claude Code gives a session started as a named agent. Legacy launch names select the same canonical policy. The limits come from the
header of the matching role file in agents/roles/. A session without a known role is not restricted.
"""

import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

from kanban.files import header_value
from kanban.project import load_project, primary_worktree

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


def relative_to_checkout(root, control_root, path, cwd):
    if control_root is not None:
        match = relative(control_root, path, cwd)
        if match is not None:
            return match, True
    return relative(root, path, cwd), control_root is None


def module_policy_path(project, module, kind, rel, directory, in_control):
    path = project.root / rel
    if kind == "write" and rel == "project.json":
        return None
    for name, workspace in project.modules.items():
        if path.is_relative_to(workspace):
            if name != module or not in_control:
                return None
            return (Path("project") / path.relative_to(workspace)).as_posix()
        if directory and workspace.is_relative_to(path):
            return None
    if path.is_relative_to(project.memory):
        if not in_control:
            return None
        return (Path("project/rememory") / path.relative_to(project.memory)).as_posix()
    if kind == "write" and any(covers([f"project/{group}/"], rel)
                               for group in ("kanban", "specs", "batches", "rememory")):
        return None
    return rel


def module_shell_paths(project, root, cwd, command):
    """Recognize simple literal arguments for custom module and memory paths."""
    try:
        words = shlex.split(command)
    except ValueError:
        return
    tracked = (*project.modules.values(), project.memory)
    for word in words:
        if word.startswith("-") or not word or "\x00" in word:
            continue
        rel, canonical = relative_to_checkout(root, project.root, word, cwd)
        if rel is None:
            continue
        source = project.root / rel
        if rel == "project.json" or any(source.is_relative_to(directory) for directory in tracked):
            yield rel, canonical


def checks(root, tool, tool_input, cwd, project=None):
    """Yield the paths and operation kinds recognized by the optional hook."""
    control_root = project.root if project else None

    def touched(path):
        return relative_to_checkout(root, control_root, path, cwd)

    if tool in READ_TOOLS:
        rel, in_control = touched(tool_input.get(READ_TOOLS[tool], ""))
        if rel is not None:
            yield "read", rel, False, f"reading {rel}", in_control
    elif tool in SEARCH_TOOLS:
        rel, in_control = touched(tool_input.get("path") or cwd)
        if rel is not None:
            yield "read", rel, True, "searching " + ("the whole project" if rel == "." else rel), in_control
    elif tool in WRITE_TOOLS:
        rel, in_control = touched(tool_input.get(WRITE_TOOLS[tool], ""))
        if rel is not None:
            yield "write", rel, False, f"writing {rel}", in_control
    elif tool == "Bash":
        command = tool_input.get("command", "")
        for word in PATH_WORD.findall(command):
            if project:
                rel, in_control = touched(word.rstrip("/"))
            else:
                rel, in_control = word.rstrip("/"), True
            if rel is not None:
                yield "read", rel, False, f"a command that touches {word}", in_control
        if project:
            for rel, in_control in module_shell_paths(project, root, cwd, command):
                yield "read", rel, False, f"a command that touches {rel}", in_control
        for target in REDIRECT.findall(command):
            rel, in_control = touched(target)
            if rel is not None:
                yield "write", rel, False, f"a command that writes {rel}", in_control
        if GIT_WORD.search(command):
            yield "git", "", False, "a Git command", True


def refusal(role, kind, label):
    where = {"read": "Read access", "write": "Write access", "git": "Forbidden"}[kind]
    return f"the {role['title']} role does not allow {label} ({role['file']}, {where})"


def violation(role, root, tool, tool_input, cwd, project=None, module=None):
    for kind, rel, directory, label, in_control in checks(root, tool, tool_input, cwd, project):
        if kind == "git":
            if role.get("git") == "forbidden":
                return kind, label
        else:
            policy_path = module_policy_path(project, module, kind, rel, directory, in_control) if project else rel
            if policy_path is None:
                return kind, f"{label} outside the selected module's control records or scope"
            if policy_path == "project.json" and kind == "read" and project:
                continue
            if not permits(role, kind, policy_path, directory):
                return kind, label
    return None


def decide(roles, agent_type, root, tool, tool_input, cwd, project=None, module=None):
    """Return a refusal message, or None to allow."""
    agent_type = ROLE_ALIASES.get(agent_type, agent_type)
    role = roles.get(agent_type)
    if role is None:
        return None
    found = violation(role, root, tool, tool_input, cwd, project, module)
    if found is None:
        return None
    others = [other["title"] for name, other in roles.items()
              if name != agent_type and violation(other, root, tool, tool_input, cwd, project, module) is None]
    if others:
        advice = f"Continue in a new session, or in an existing one, with the {' or '.join(others)}."
    elif "the whole project" in found[1]:
        advice = "Search a specific folder that your role may read."
    else:
        advice = "No role allows it; ask the User."
    return f"Refused: {refusal(role, *found)}. {advice} An instruction does not set this limit aside."


def scoped_project(root, requested):
    control = primary_worktree(root) if (root / ".git").exists() else root
    project = load_project(control)
    selected = project.select_module(requested)
    return (project, selected) if selected is not None else (None, None)


def main():
    event = json.load(sys.stdin)
    agent_type = event.get("agent_type")
    if not agent_type:
        return 0
    cwd = event.get("cwd") or os.getcwd()
    root = os.environ.get("CLAUDE_PROJECT_DIR")
    if not root:
        root = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=cwd, text=True).strip()
    root = Path(root).resolve()
    roles = load_roles(root)
    if ROLE_ALIASES.get(agent_type, agent_type) not in roles:
        return 0
    try:
        project, selected = scoped_project(root, os.environ.get("KR_MODULE"))
        message = decide(roles, agent_type, root, event.get("tool_name", ""),
                         event.get("tool_input") or {}, cwd, project, selected)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        message = f"Refused: module scope could not be resolved. {error}"
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
