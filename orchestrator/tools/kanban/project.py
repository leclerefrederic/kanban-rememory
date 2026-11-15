"""Resolve the project settings and its module workspaces."""

from dataclasses import dataclass
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
from typing import Dict

from .files import header_value


IDENTIFIER = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
MISC = "misc"
SETTINGS = Path("project/settings.json")
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
    workflow: dict
    last_card_id: int = 0

    def validate_scope(self, scope: str) -> str:
        if scope not in self.modules:
            raise ValueError(f"Unknown module: {scope!r}.")
        return scope

    def workspace(self, scope: str) -> Path:
        return self.modules[self.validate_scope(scope)]

    def resources(self, scope: str, task_id: str) -> Path:
        return self.workspace(scope) / "resources" / task_id.lower()

    def journal(self) -> Path:
        return local_directory(self.root, self.memory)

    def card_scope(self, path: Path) -> str:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Not a regular Card record: {path}.")
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        declared = (sum(line.partition(":")[0] == "module" for line in lines[1:lines.index("---", 1)])
                    if lines[:1] == ["---"] and "---" in lines[1:] else 0)
        if declared != 1:
            raise ValueError(f"Expected one module field in Card: {path}.")
        return self.validate_scope(header_value(source, "module"))

    def check_boards(self) -> None:
        for workspace in self.modules.values():
            for stage in (*self.workflow["stages"], "resources"):
                directory = local_directory(self.root, workspace / stage)
                if directory.is_symlink() or any(path.is_symlink() for path in directory.rglob("*")):
                    raise ValueError(f"Module Card record contains a symbolic link: {directory}.")

    def select_module(self, module=None) -> str:
        if module is None:
            if len(self.modules) == 1:
                return next(iter(self.modules))
            raise ValueError(f"Choose a module explicitly: {', '.join(sorted(self.modules))}.")
        return self.validate_scope(module)


def local_directory(root, path):
    if (not path.is_relative_to(root) or path.resolve() != path
            or (path.exists() and not path.is_dir())):
        raise ValueError(f"Not a local record directory: {path}.")
    return path


def unique_object(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"Duplicate settings key: {key}.")
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
    settings = root / SETTINGS
    try:
        if settings.is_symlink() or not settings.is_file():
            raise ValueError("Create project/settings.json with the module setup first.")
        source = settings.read_bytes()
    except OSError as error:
        raise ValueError(f"Invalid project settings: {error}") from error
    return parse_settings(root, source)


def parse_settings(root, source):
    """Validate settings bytes from a checkout or a proposed file."""
    from .workflow import check_workflow

    try:
        data = json.loads(source.decode("utf-8"), object_pairs_hook=unique_object)
        object_fields(data, ("schema_version", "board_layout", "project", "shared", "modules",
                             "execution", "workflow", "last_card_id"), "Settings")
        if data["board_layout"] != "module":
            raise ValueError("board_layout must be module.")
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise ValueError("Unsupported schema_version; expected 1.")
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
        if MISC not in modules:
            raise ValueError(f"Settings require a {MISC} module.")
        floor = data["last_card_id"]
        if type(floor) is not int or not 0 <= floor <= 99999999:
            raise ValueError("last_card_id must be an integer from 0 to 99999999.")
        return Project(root, project_id, project["name"], memory, sources, modules,
                       check_workflow(data["workflow"]), floor)
    except (OSError, ValueError, RuntimeError) as error:
        raise ValueError(f"Invalid project settings: {error}") from error


def primary_worktree(root):
    """Locate the primary checkout for this local Git clone."""
    output = subprocess.check_output(
        ["git", "worktree", "list", "--porcelain", "-z"], cwd=root,
    )
    record = output.split(b"\0", 1)[0]
    if not record.startswith(b"worktree "):
        raise ValueError("Could not locate the primary worktree.")
    primary = Path(os.fsdecode(record[len(b"worktree "):])).resolve()
    if not primary.is_dir() or not (primary / ".git").exists():
        raise ValueError("Board tools require a primary worktree in this clone.")
    return primary


def coordination_root(root):
    common = subprocess.check_output(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=root, text=True,
    ).strip()
    return Path(common) / "kanban-rememory"
