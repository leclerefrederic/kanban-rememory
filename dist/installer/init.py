"""Create kanban-rememory.json and the empty boards of a project from an approved proposal, once.

Run from the root of the repository: python3 init.py proposal.json [--apply]. Without --apply nothing is written.
This installer shares no code with kr; `kr validate` checks its result afterwards."""

import argparse
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from zoneinfo import ZoneInfo

CONFIG = "kanban-rememory.json"
KEYS = ("name", "modules", "workflow", "version", "directory")
OPTIONAL = ("kit", "notifications")
WORK = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
MODULE = re.compile(r"[a-z0-9]+(?:[-_][a-z0-9]+)*")
STAGE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
REQUIRED_STAGES = {"backlog", "development", "completion", "cancellation"}


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate key: {key}.")
        result[key] = value
    return result


def check(data):
    """Validate the proposal and return its folders, relative to the repository root."""
    if not isinstance(data, dict) or not set(KEYS) <= set(data) <= set(KEYS + OPTIONAL):
        raise ValueError(f"The file must contain {', '.join(KEYS)} and may add {', '.join(OPTIONAL)}.")
    directory = data["directory"]
    if not isinstance(directory, str) or not WORK.fullmatch(directory) or directory == "kanban-rememory":
        raise ValueError("directory must be one plain folder name, not kanban-rememory.")
    if "kit" in data and (not isinstance(data["kit"], str) or not VERSION.fullmatch(data["kit"])):
        raise ValueError("kit must be a release number such as 0.1.0.")
    name = data["name"]
    if not isinstance(name, str) or not name.strip() or "\n" in name or "\r" in name:
        raise ValueError("name must be a single-line display name.")
    modules = data["modules"]
    if (not isinstance(modules, list) or len(set(modules)) != len(modules)
            or not all(isinstance(module, str) and MODULE.fullmatch(module) for module in modules)):
        raise ValueError("modules must list unique lowercase module IDs.")
    if "misc" not in modules:
        raise ValueError("modules must include misc.")
    if not isinstance(data["version"], str) or not VERSION.fullmatch(data["version"]):
        raise ValueError("version must be a release number such as 0.1.0.")
    if "notifications" in data:
        check_notifications(data["notifications"])
    stages = check_workflow(data["workflow"])
    return [Path(directory) / "rememory"] + [Path(directory) / "modules" / module / stage
                                             for module in modules for stage in (*stages, "resources")]


def check_notifications(settings):
    if not isinstance(settings, dict) or set(settings) != {"slack", "telegram"}:
        raise ValueError("notifications must contain slack and telegram settings.")
    for service, flags in settings.items():
        if (not isinstance(flags, dict) or set(flags) != {"configured", "active"}
                or not all(isinstance(flag, bool) for flag in flags.values())):
            raise ValueError(f"notifications.{service} must contain boolean configured and active flags.")
        if flags["active"] and not flags["configured"]:
            raise ValueError(f"notifications.{service} must be configured before it can be active.")
    return settings


def check_workflow(workflow):
    """The stages of a new board; the tools rely on the four required ones and on their order."""
    if not isinstance(workflow, dict):
        raise ValueError("workflow must contain an object.")
    stages, active, completed = workflow.get("stages"), workflow.get("active"), workflow.get("completed")
    if (not isinstance(stages, list) or len(stages) != len(set(stages)) or "resources" in stages
            or not all(isinstance(stage, str) and STAGE.fullmatch(stage) for stage in stages)):
        raise ValueError("stages must contain unique folder names other than resources.")
    if missing := REQUIRED_STAGES.difference(stages):
        raise ValueError(f"Missing required stages: {', '.join(sorted(missing))}.")
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
    try:
        ZoneInfo(workflow.get("timezone"))
    except (KeyError, OSError, TypeError, ValueError):
        raise ValueError(f"Unknown time zone: {workflow.get('timezone')}.") from None
    if (stages[0] != "backlog" or active[0] != "development" or completed != "completion"
            or {"backlog", "cancellation"}.intersection(active) or transitions.get("cancellation")):
        raise ValueError("Use backlog for intake, development as the first active stage, "
                         "completion for delivery and cancellation as a terminal stage.")
    return stages


def install(root, proposal, apply):
    config = root / CONFIG
    if config.exists() or config.is_symlink():
        raise ValueError(f"{CONFIG} already exists.")
    source = proposal.read_bytes()  # validate and write the same bytes
    data = json.loads(source.decode("utf-8"), object_pairs_hook=unique_keys)
    folders = [root / path for path in check(data)]
    for folder in folders:
        if folder.resolve() != folder or (folder.exists() and not folder.is_dir()):
            raise ValueError(f"Not a local directory: {folder.relative_to(root)}.")
    print(f"{data['name']}: {', '.join(data['modules'])}")
    for folder in folders:
        print(folder.relative_to(root))
    if not apply:
        print("Preview only. Run again with --apply after approval.")
        return 0
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        if not any(folder.iterdir()):
            (folder / ".gitkeep").touch()
    with tempfile.NamedTemporaryFile(dir=root, prefix=".kr-config-", delete=False) as pending:
        pending.write(source)
    try:
        os.link(pending.name, config)  # refuses to replace a config file created meanwhile
    finally:
        os.unlink(pending.name)
    print("Project modules are ready.")
    return 0


def main(argv=None, root=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    try:
        return install((root or Path.cwd()).resolve(), args.proposal, args.apply)
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
