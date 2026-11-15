"""Resolve a declared project and its module workspaces."""

from dataclasses import dataclass
import json
import os
from pathlib import Path, PureWindowsPath
import re
import subprocess
from typing import Dict, Optional

from .files import CARD_ID, header_value


IDENTIFIER = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
PROJECT_SCOPE = "@project"
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

    @property
    def board(self) -> Path:
        return self.root / "project"

    def validate_scope(self, scope: str) -> str:
        if not isinstance(scope, str) or (scope != PROJECT_SCOPE and scope not in self.modules):
            raise ValueError(f"Unknown Card scope: {scope!r}.")
        return scope

    def scope_workspace(self, scope: str) -> Path:
        self.validate_scope(scope)
        return self.board if scope == PROJECT_SCOPE else self.modules[scope]

    def legacy_memory(self, scope: str) -> Path:
        workspace = self.scope_workspace(scope)
        return self.memory if scope == PROJECT_SCOPE else workspace / "rememory"

    def central_memory(self, scope: str) -> Path:
        self.validate_scope(scope)
        return self.memory / "project" if scope == PROJECT_SCOPE else self.memory / "modules" / scope

    def scope_memory(self, scope: str) -> Path:
        central_project = self.central_memory(PROJECT_SCOPE)
        if central_project.exists() or central_project.is_symlink():
            local_directory(self.root, central_project)
            return local_directory(self.root, self.central_memory(scope))
        return local_directory(self.root, self.legacy_memory(scope))

    def setup_memory(self) -> tuple:
        scopes = (PROJECT_SCOPE, *self.modules)
        legacy = [self.legacy_memory(scope) for scope in scopes]
        for path in legacy:
            local_directory(self.root, path)
        central = self.central_memory(PROJECT_SCOPE)
        if not central.exists() and any(
            any(path.glob("*.md")) for path in legacy
        ):
            return tuple(legacy)
        return tuple(local_directory(self.root, self.central_memory(scope)) for scope in scopes)

    def card_scope(self, path: Path, *, allow_legacy=False) -> Optional[str]:
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Not a regular Card record: {path}.")
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        declared = (sum(line.partition(":")[0] == "scope"
                        for line in lines[1:lines.index("---", 1)])
                    if lines[:1] == ["---"] and "---" in lines[1:] else 0)
        if declared > 1:
            raise ValueError(f"Duplicate Card scope: {path}.")
        scope = header_value(source, "scope")
        if not declared:
            if allow_legacy:
                return None
            if not self.modules:
                return PROJECT_SCOPE
        return self.validate_scope(scope)

    def archived_stages(self, workspace: Path) -> set:
        from .workflow import check_workflow

        config = workspace / "kanban/workflow.json"
        if config.is_symlink():
            raise ValueError(f"Historical workflow must be a local record: {config}.")
        completed = (check_workflow(json.loads(config.read_text(encoding="utf-8")))["completed"]
                     if config.exists() else "completion")
        return {completed, "cancellation"}

    def check_legacy_boards(self) -> None:
        for module, workspace in self.modules.items():
            board = workspace / "kanban"
            if board.is_symlink():
                raise ValueError(f"Historical board must be a local record: {board}.")
            archived = self.archived_stages(workspace)
            for path in board.glob("*/*.md"):
                if path.parent.name not in archived and CARD_ID.match(path.stem):
                    raise ValueError(f"Module {module} has unfinished Cards on an earlier board. "
                                     "Use an approved migration plan for those Cards.")

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


def local_directory(root, path):
    if (not path.is_relative_to(root) or path.resolve() != path
            or (path.exists() and not path.is_dir())):
        raise ValueError(f"Not a local journal directory: {path}.")
    return path


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


def repo_path(root, value, label, *, resolve_paths=True):
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError(f"{label} must be a nonempty repository-relative path.")
    path = Path(value)
    windows = PureWindowsPath(value)
    if path.is_absolute() or windows.drive or ".." in path.parts:
        raise ValueError(f"{label} must be a repository-relative path without '..'.")
    resolved = root / path
    if resolve_paths:
        resolved = resolved.resolve()
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
        source = manifest.read_bytes()
    except (OSError, ValueError) as error:
        raise ValueError(f"Invalid project.json: {error}") from error
    return parse_manifest(root, source)


def parse_manifest(root, source, *, resolve_paths=True):
    """Validate manifest bytes from a checkout or a committed Git blob."""
    try:
        data = json.loads(source.decode("utf-8"), object_pairs_hook=unique_object)
        object_fields(data, ("schema_version", "project", "shared", "modules", "execution"), "Manifest")
        if type(data["schema_version"]) is not int or data["schema_version"] != 1:
            raise ValueError("Unsupported project manifest schema_version; expected 1.")
        project = object_fields(data["project"], ("id", "name"), "project")
        project_id = identifier(project["id"], "project.id")
        if not isinstance(project["name"], str) or not project["name"].strip():
            raise ValueError("project.name must be a nonempty display name.")
        shared = object_fields(data["shared"], ("memory", "sources"), "shared")
        memory = repo_path(root, shared["memory"], "shared.memory", resolve_paths=resolve_paths)
        if overlaps(memory, root / "project/kanban"):
            raise ValueError("Shared memory overlaps the project board.")
        if not isinstance(shared["sources"], list):
            raise ValueError("shared.sources must be a list.")
        sources = tuple(repo_path(root, path, "shared.sources", resolve_paths=resolve_paths)
                        for path in shared["sources"])
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
            workspace = repo_path(root, definition["workspace"], f"modules.{name}.workspace",
                                  resolve_paths=resolve_paths)
            if (overlaps(workspace, memory) or overlaps(workspace, root / "project/kanban")
                    or any(overlaps(workspace, other) for other in modules.values())):
                raise ValueError(f"Overlapping workspace, board or memory directory: modules.{name}.")
            modules[name] = workspace
        return Project(root, project_id, project["name"], memory, sources, modules)
    except (OSError, ValueError, RuntimeError) as error:
        raise ValueError(f"Invalid project.json: {error}") from error


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


def coordination_root(root):
    common = subprocess.check_output(
        ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"], cwd=root, text=True,
    ).strip()
    return Path(common) / "kanban-rememory"

def invocation_module(explicit):
    assigned = os.environ.get("KR_MODULE")
    if explicit and assigned and explicit != assigned:
        raise ValueError("Module selection differs from the current invocation.")
    return explicit or assigned or None
