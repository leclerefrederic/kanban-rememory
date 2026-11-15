"""Resolve a declared project and its module workspaces."""

from dataclasses import dataclass
import json
from pathlib import Path, PureWindowsPath
import re
from typing import Dict, Optional


IDENTIFIER = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
EXECUTION = {
    "active_deliveries_per_module": 1,
    "branch_required": True,
    "worktree_required": True,
    "concurrent_integrations": 1,
}


@dataclass(frozen=True)
class Project:
    root: Path
    id: str
    name: str
    memory: Path
    sources: tuple
    modules: Dict[str, Path]

    def select_module(self, module: Optional[str] = None) -> Optional[str]:
        if not self.modules:
            if module is not None:
                raise ValueError("Module selection requires an active project.json.")
            return None
        if module is None:
            if len(self.modules) == 1:
                return next(iter(self.modules))
            choices = ", ".join(sorted(self.modules))
            raise ValueError(f"Choose a module explicitly: {choices}.")
        if module not in self.modules:
            raise ValueError(f"Unknown module: {module}.")
        return module

    def workspace(self, module: Optional[str] = None) -> Path:
        selected = self.select_module(module)
        return self.root / "project" if selected is None else self.modules[selected]


def unique_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate project.json key: {key}.")
        result[key] = value
    return result


def object_fields(value, expected, label):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f"{label} must contain: {', '.join(expected)}.")
    return value


def identifier(value, label):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f"{label} must be a lowercase identifier.")
    return value


def repo_path(root, value, label):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError(f"{label} must be a nonempty repository-relative path.")
    path = Path(value)
    windows = PureWindowsPath(value)
    if path.is_absolute() or windows.drive or ".." in path.parts:
        raise ValueError(f"{label} must be a repository-relative path without '..'.")
    resolved = (root / path).resolve()
    if (resolved == root or not resolved.is_relative_to(root)
            or (root / ".git") in (resolved, *resolved.parents)):
        raise ValueError(f"{label} resolves outside an allowed project directory.")
    return resolved


def overlaps(first, second):
    return first.is_relative_to(second) or second.is_relative_to(first)


def load_project(root):
    root = Path(root).resolve()
    manifest = root / "project.json"
    if not manifest.exists() and not manifest.is_symlink():
        return Project(root, root.name, root.name, root / "project/rememory", (), {})
    return read_manifest(root, manifest)


def read_manifest(root, manifest):
    try:
        if manifest.is_symlink() or not manifest.is_file():
            raise ValueError("The manifest must be a regular file.")
        data = json.loads(manifest.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
        object_fields(data, ("schema_version", "project", "shared", "modules", "execution"), "Manifest")
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise ValueError("Unsupported project manifest schema_version; expected 1.")
        project = object_fields(data["project"], ("id", "name"), "project")
        project_id = identifier(project["id"], "project.id")
        if not isinstance(project["name"], str) or not project["name"].strip():
            raise ValueError("project.name must be a nonempty display name.")
        shared = object_fields(data["shared"], ("memory", "sources"), "shared")
        memory = repo_path(root, shared["memory"], "shared.memory")
        if not isinstance(shared["sources"], list):
            raise ValueError("shared.sources must be a list.")
        sources = tuple(repo_path(root, path, "shared.sources") for path in shared["sources"])
        execution = object_fields(data["execution"], EXECUTION, "execution")
        for name, expected in EXECUTION.items():
            actual = execution[name]
            if type(actual) is not type(expected) or actual != expected:
                raise ValueError(f"Unsupported execution.{name}; expected {json.dumps(expected)}.")
        modules = {}
        if not isinstance(data["modules"], dict) or not data["modules"]:
            raise ValueError("modules must define at least one module.")
        for name, value in data["modules"].items():
            identifier(name, "Module ID")
            definition = object_fields(value, ("workspace",), f"modules.{name}")
            workspace = repo_path(root, definition["workspace"], f"modules.{name}.workspace")
            if overlaps(workspace, memory) or any(overlaps(workspace, other) for other in modules.values()):
                raise ValueError(f"Overlapping workspace or memory directory: modules.{name}.")
            modules[name] = workspace
        return Project(root, project_id, project["name"], memory, sources, modules)
    except (OSError, ValueError, RuntimeError) as error:
        raise ValueError(f"Invalid project.json: {error}") from error


def primary_worktree(root):
    """Locate the primary checkout for this local Git clone."""
    import os
    import subprocess

    output = subprocess.check_output(
        ["git", "worktree", "list", "--porcelain", "-z"], cwd=root,
    )
    record = output.split(b"\0", 1)[0]
    if not record.startswith(b"worktree "):
        raise ValueError("Could not locate the primary worktree.")
    primary = Path(os.fsdecode(record[len(b"worktree "):])).resolve()
    if not primary.is_dir() or not (primary / ".git").exists():
        raise ValueError("Module coordination requires a primary worktree in this clone.")
    return primary


def control_workspace(project, module=None):
    """Return the authoritative control checkout and its selected workspace."""
    primary = primary_worktree(project.root)
    canonical = project if primary == project.root else load_project(primary)
    if canonical.modules:
        return primary, canonical.workspace(module)
    if project.modules:
        raise ValueError("Activate modules from the primary worktree before using module tools.")
    return project.root, project.workspace(module)
