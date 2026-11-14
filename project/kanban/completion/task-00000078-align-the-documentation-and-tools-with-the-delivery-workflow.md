---
type: card
id: "TASK-00000078"
batch: null
specifications: []
---

# TASK-00000078 — Align the documentation and tools with the delivery workflow

- Owner: Development Agent
- Dependencies: TASK-00000073.
- Priority: User authorized the documentation audit corrections, following the existing acceptance-instructions Card.

## Expected outcome

Make the framework's entry points, roles, templates, and commands agree so a newly adopting project can execute the documented workflow without inventing missing rules.

Scope: standalone versus Batch rules; Batch states, approval handoff, debt resolution, naming, drafts and IDs; scheduler status and navigation; reusable examples, resource history and KRR getting started. Preserve approved historical records. Do not implement the future scheduler or change the Runner application.

## Acceptance criteria

- [x] Define standalone scope approval and Git permissions alongside the optional Batch workflow.
- [x] Document Batch transitions including correction, durable handoff locations, and later debt resolution without modifying closed reports.
- [x] Align roles and templates with actual filenames, remove required personal tools, and make scheduler status and instructions discoverable at adoption.
- [x] Allow valid draft Batch preparation without weakening ready/approved checks; make command IDs consistent with documented paths and preserve historical compatibility.
- [x] Add a worked Specification/Batch example, shared-resource revision/archive example, and a source-verified KRR startup guide.
- [x] Verify draft/ready transitions, approval checks and ID handling with regression tests; check links and adoption from an isolated repository and review the diff before closure.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None. TASK-00000073 is closed and published in e93b653.

- Starting revision: `e93b653`. The containing publication commit identifies this change.
- Aligned the [shared instructions](../../../docs/agents/work-in-a-project.md), actor roles, manifesto, installation instructions and templates. The [Batch workflow](../../../docs/batches/batch-workflow.md) names lifecycle transitions and the [operations guide](../../../docs/batches/start-and-close-batches.md) locates approval, correction, guard and debt evidence.
- Added a [worked delivery example](../../../docs/batches/delivery-example.md), resource history example, and [Runner startup guide](../../../docs/runner/getting-started.md) checked against the current Swift sources and build script. Scheduler documentation explicitly describes a procedure, not an implemented dispatcher.
- `python3 tools/test-kanban-board.py`: all 15 tests passed, including draft preparation, ready-state requirements, malformed status rejection, lifecycle approval verification, case-compatible Batch arguments, isolated Batch module adoption, the four example records, and notification previews without sending messages. Existing legacy checks remain covered.
- `python3 tools/manage-kanban-board.py validate` and `git diff --check`: passed. All 23 documentation files are reachable from README; relative Markdown links and heading anchors pass validation. Reviewed the changed code and documentation before closure.
- No product build, live application acceptance, scheduler activation, or external notification was performed. Existing unrelated local files and approved historical records were preserved.
- Flow review: this was the only active Card; TASK-00000073 dependency is satisfied. Next action: publish the closed Card and verified changes under standing authorization.

## History

- 2026-11-14 — User authorized all necessary corrections identified by the documentation audit. No Batch is active.

- 2026-11-14T00:59:57+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:12:58+01:00 — Stage moved from `development` to `completion`.
