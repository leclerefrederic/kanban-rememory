"""Workflow configuration checks."""

import re
from zoneinfo import ZoneInfo


def check_workflow(workflow):
    if not isinstance(workflow, dict):
        raise ValueError("workflow must contain an object.")
    stages = workflow.get("stages")
    if (not isinstance(stages, list) or not stages
            or any(not isinstance(stage, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", stage)
                   for stage in stages)
            or len(stages) != len(set(stages)) or "resources" in stages):
        raise ValueError("stages must contain unique folder names other than resources.")
    active = workflow.get("active")
    completed = workflow.get("completed")
    if (not isinstance(active, list) or not active or any(stage not in stages for stage in active)
            or completed not in stages or completed in active):
        raise ValueError("Define active stages and a distinct completed stage.")
    transitions = workflow.get("transitions")
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


def check_new_workflow(workflow):
    """Rules for a newly configured board; existing boards keep their approved stages."""
    check_workflow(workflow)
    required = {"backlog", "development", "completion", "cancellation"}
    if missing := required.difference(workflow["stages"]):
        raise ValueError(f"Missing required stages: {', '.join(sorted(missing))}")
    if (workflow["stages"][0] != "backlog" or workflow["active"][0] != "development"
            or workflow["completed"] != "completion"
            or {"backlog", "cancellation"}.intersection(workflow["active"])
            or workflow["transitions"].get("cancellation")):
        raise ValueError("Use backlog for intake, development as the first active stage, "
                         "completion for delivery, and cancellation as a terminal stage.")
    return workflow
