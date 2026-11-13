"""Workflow configuration and initialization."""

import json
import re
from zoneinfo import ZoneInfo

from .files import PROJECT, ROOT


def check_workflow(workflow):
    if not isinstance(workflow, dict):
        raise ValueError("workflow.json must contain an object.")
    stages = workflow.get("stages")
    if (not isinstance(stages, list) or not stages
            or any(not isinstance(stage, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", stage)
                   for stage in stages)
            or len(stages) != len(set(stages))):
        raise ValueError("stages must contain unique folder names.")
    active = workflow.get("active")
    completed = workflow.get("completed")
    if (not isinstance(active, list) or not active or any(stage not in stages for stage in active)
            or completed not in stages or completed in active):
        raise ValueError("Define active stages and a distinct completed stage.")
    transitions = workflow.get("transitions", {})
    if not isinstance(transitions, dict) or any(
        source not in stages or not isinstance(destinations, list)
        or any(destination not in stages or destination == source for destination in destinations)
        for source, destinations in transitions.items()
    ):
        raise ValueError("Transitions must map stage names to lists of distinct destination stages.")
    limit = workflow.get("wip_limit")
    if type(limit) is not int or limit < 1:
        raise ValueError("wip_limit must be a positive integer.")
    timezone = workflow.get("timezone")
    if not isinstance(timezone, str) or not timezone:
        raise ValueError("timezone must be an IANA time zone.")
    try:
        ZoneInfo(timezone)
    except (KeyError, ValueError):
        raise ValueError(f"Unknown time zone: {timezone}") from None
    return workflow


def load_workflow():
    path = PROJECT / "kanban/workflow.json"
    if not path.is_file():
        raise ValueError("No workflow configured. Follow docs/agents/adoption.md before using the board.")
    workflow = check_workflow(json.loads(path.read_text(encoding="utf-8")))
    missing = [stage for stage in workflow["stages"] if not (PROJECT / "kanban" / stage).is_dir()]
    if missing:
        raise ValueError(f"Missing stage folders: {', '.join(missing)}")
    return workflow


TEMPLATES = {
    "short": ([], ["development"]),
    "standard": ([], ["development", "code-review"]),
    "long": (["refinement"], ["development", "code-review", "testing", "deployment"]),
}


def starter_transitions(delivery, active):
    transitions = {
        stage: [following, "archive"] for stage, following in zip(delivery, delivery[1:])
    }
    for stage in active[1:]:
        transitions[stage].append(active[0])
    return transitions


def initialize(args):
    if args.config:
        workflow = json.loads(args.config.read_text(encoding="utf-8"))
    else:
        preparation, active = TEMPLATES[args.template]
        delivery = ["backlog", *preparation, *active, "completion"]
        workflow = {
            "stages": [*delivery, "archive"],
            "transitions": starter_transitions(delivery, active),
            "active": active,
            "completed": "completion",
            "wip_limit": args.wip_limit if args.wip_limit is not None else 1,
            "timezone": args.timezone or "UTC",
        }
    check_workflow(workflow)

    board = PROJECT / "kanban"
    config = board / "workflow.json"
    if board.is_symlink() or config.is_symlink():
        raise ValueError("The board and workflow configuration must be local paths.")
    if config.exists() and json.loads(config.read_text(encoding="utf-8")) != workflow:
        raise ValueError("A different workflow already exists. Use an explicit migration.")
    stages = [board / stage for stage in workflow["stages"]]
    for stage in stages:
        if stage.is_symlink() or (stage.exists() and not stage.is_dir()):
            raise ValueError(f"Stage path is not a local directory: {stage.relative_to(ROOT)}")
    if board.exists():
        outside = [entry.name for entry in board.iterdir()
                   if entry.is_dir() and entry not in stages and any(entry.glob("*.md"))]
        if outside:
            raise ValueError(f"Existing cards outside the proposed stages: {', '.join(sorted(outside))}")

    print(json.dumps(workflow, indent=2))
    for stage in stages:
        if not stage.exists():
            print(f"Create {stage.relative_to(ROOT)}/")
    if not args.apply:
        print("Preview only. Run again with --apply after approval.")
        return 0

    for stage in stages:
        stage.mkdir(parents=True, exist_ok=True)
        if not any(stage.iterdir()):
            (stage / ".gitkeep").touch(exist_ok=True)
    try:
        with config.open("x", encoding="utf-8") as file:
            json.dump(workflow, file, indent=2)
            file.write("\n")
    except FileExistsError:
        if load_workflow() != workflow:
            raise ValueError("A different workflow already exists. Use an explicit migration.") from None
    print("Workflow ready.")
    return 0
