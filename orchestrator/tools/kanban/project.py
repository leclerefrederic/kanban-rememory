"""Project settings, the fixed record layout and the Git locations the tools use."""

from dataclasses import dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from zoneinfo import ZoneInfo

SETTINGS = Path("project/settings.json")
MODULES = Path("project/modules")
JOURNAL = Path("project/rememory")
MISC = "misc"
KEYS = ("schema_version", "name", "modules", "workflow", "version")
LEGACY_KEYS = ("last_card_id",)  # installed settings may still carry it; it is ignored
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
MODULE = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
STAGE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


@dataclass(frozen=True)
class Project:
    root: Path
    name: str
    modules: tuple
    workflow: dict
    version: str

    def board(self, module):
        if module not in self.modules:
            raise ValueError(f"Unknown module: {module!r}.")
        return self.root / MODULES / module

    @property
    def journal(self):
        return self.root / JOURNAL

    @property
    def frozen(self):
        """Stages a Card never leaves: their records are history."""
        return {stage for stage in self.workflow["stages"] if not self.workflow["transitions"].get(stage)}

    def now(self):
        return datetime.now(ZoneInfo(self.workflow["timezone"]))


def bump(version, part):
    """The next release number: part is patch, minor or major."""
    major, minor, patch = map(int, version.split("."))
    return {"major": f"{major + 1}.0.0", "minor": f"{major}.{minor + 1}.0", "patch": f"{major}.{minor}.{patch + 1}"}[part]


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def common_directory(root):
    """The clone's Git directory, where the phase state lives."""
    return Path(git(root, "rev-parse", "--path-format=absolute", "--git-common-dir"))


def load_project(root):
    settings = root / SETTINGS
    if settings.is_symlink() or not settings.is_file():
        raise ValueError("Create project/settings.json first: see orchestrator/install.md.")
    return parse_settings(root, settings.read_bytes())


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate settings key: {key}.")
        result[key] = value
    return result


def parse_settings(root, source):
    try:
        data = json.loads(source.decode("utf-8"), object_pairs_hook=unique_keys)
        if not isinstance(data, dict) or not set(KEYS) <= set(data) <= {*KEYS, *LEGACY_KEYS}:
            raise ValueError(f"Settings must contain exactly: {', '.join(KEYS)}.")
        if type(data["schema_version"]) is not int or data["schema_version"] != 2:
            raise ValueError("Unsupported schema_version; expected 2. See orchestrator/install.md to upgrade.")
        name = data["name"]
        if not isinstance(name, str) or not name.strip() or "\n" in name or "\r" in name:
            raise ValueError("name must be a single-line display name.")
        modules = data["modules"]
        if (not isinstance(modules, list) or len(set(modules)) != len(modules)
                or not all(isinstance(module, str) and MODULE.fullmatch(module) for module in modules)):
            raise ValueError("modules must list unique lowercase module IDs.")
        if MISC not in modules:
            raise ValueError(f"modules must include {MISC}.")
        version = data["version"]
        if not isinstance(version, str) or not VERSION.fullmatch(version):
            raise ValueError("version must be a release number such as 0.1.0.")
        return Project(root, name, tuple(modules), check_workflow(data["workflow"]), version)
    except ValueError as error:
        raise ValueError(f"Invalid project settings: {error}") from None


def check_workflow(workflow):
    if not isinstance(workflow, dict):
        raise ValueError("workflow must contain an object.")
    stages = workflow.get("stages")
    if (not isinstance(stages, list) or not stages or len(stages) != len(set(stages)) or "resources" in stages
            or not all(isinstance(stage, str) and STAGE.fullmatch(stage) for stage in stages)):
        raise ValueError("stages must contain unique folder names other than resources.")
    active, completed = workflow.get("active"), workflow.get("completed")
    if (not isinstance(active, list) or not active or any(stage not in stages for stage in active)
            or completed not in stages or completed in active):
        raise ValueError("Define active stages and a distinct completed stage.")
    transitions = workflow.get("transitions")
    if not isinstance(transitions, dict) or any(
            source not in stages or not isinstance(targets, list)
            or any(target not in stages or target == source for target in targets)
            for source, targets in transitions.items()):
        raise ValueError("transitions must map stages to lists of other stages.")
    limit = workflow.get("wip_limit")
    if type(limit) is not int or limit < 1:
        raise ValueError("wip_limit must be a positive integer.")
    timezone = workflow.get("timezone")
    try:
        ZoneInfo(timezone)
    except (KeyError, OSError, TypeError, ValueError):
        raise ValueError(f"Unknown time zone: {timezone}") from None
    return workflow


def check_new_workflow(workflow):
    """A new board needs the stages the tools rely on; existing boards keep their approved stages."""
    if missing := {"backlog", "development", "completion", "cancellation"}.difference(workflow["stages"]):
        raise ValueError(f"Missing required stages: {', '.join(sorted(missing))}.")
    if (workflow["stages"][0] != "backlog" or workflow["active"][0] != "development"
            or workflow["completed"] != "completion"
            or {"backlog", "cancellation"}.intersection(workflow["active"])
            or workflow["transitions"].get("cancellation")):
        raise ValueError("Use backlog for intake, development as the first active stage, "
                         "completion for delivery and cancellation as a terminal stage.")


def init(root, proposal, apply):
    """Create the settings and the empty boards from an approved proposal, once."""
    settings = root / SETTINGS
    if settings.exists() or settings.is_symlink():
        raise ValueError("Project settings already exist; an upgrade needs an approved migration.")
    source = proposal.read_bytes()  # validate and write the same bytes
    project = parse_settings(root, source)
    check_new_workflow(project.workflow)
    paths = [project.journal] + [project.board(module) / stage for module in project.modules
                                 for stage in (*project.workflow["stages"], "resources")]
    for path in paths:
        if path.resolve() != path or (path.exists() and not path.is_dir()):
            raise ValueError(f"Not a local directory: {path.relative_to(root)}.")
    print(f"{project.name}: {', '.join(project.modules)}")
    for path in paths:
        print(path.relative_to(root))
    if not apply:
        print("Preview only. Run again with --apply after approval.")
        return 0
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
        if not any(path.iterdir()):
            (path / ".gitkeep").touch()
    with tempfile.NamedTemporaryFile(dir=settings.parent, prefix=".settings-", delete=False) as pending:
        pending.write(source)
    try:
        os.link(pending.name, settings)  # refuses to replace a settings file created meanwhile
    finally:
        os.unlink(pending.name)
    print("Project modules are ready.")
    return 0
