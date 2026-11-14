---
type: card
id: "TASK-00000090"
batch: null
specifications: []
---

# TASK-00000090 — Clarify reader guide names and cover everyday project requests

- Owner: Development Agent
- Dependencies: None.
- Priority: User requested clearer guide names and missing user journeys, explicitly including assign-a-task.

## Expected outcome

Readers can find a guide by the action they want to take. Name the Runner guide explicitly, identify Batch delivery and acceptance guides by their subject, and explain how to assign a task, resume work and report a defect through conversation.

Scope: English reader guides and navigation, necessary link updates, installation test paths. Reuse existing workflow rules and link detailed explanations instead of duplicating them. Preserve the shared manifesto, agent procedures, live project records and application behavior. Do not add scheduler behavior, product features or new approval requirements.

## Acceptance criteria

- [x] Use explicit lowercase filenames for Runner, Batch delivery and Batch testing guides, with no obsolete redirects or broken references.
- [x] Add assign-a-task, resume-work and report-a-defect guides that explain user inputs and agent responses under existing scope, ownership and authorization rules.
- [x] Make each guide discoverable from the README and documentation index, with consistent titles and cross-links and no agent operating commands in reader guides.
- [x] Review the documentation against the working rules; verify links, guide reachability and all adoption tests before closure.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `d3512b5`.
- Renamed the three ambiguous guides to `use-kanban-rememory-runner.md`, `deliver-a-batch.md` and `test-and-accept-a-batch.md`. Titles, README navigation, cross-links and installation test paths now use the same explicit names; no redirects remain.
- Added reader guides for assigning a task, resuming work and reporting a defect. They use conversational examples, explain what the agent records, and preserve existing scope, Card ownership, Batch acceptance and publication rules. Reduced the duplicate resumption explanation in the setup guide.
- Verification: all 15 existing adoption tests passed. Board link validation and whitespace checks passed. All 15 reader documents, including the five examples and index, are reachable from the README. No obsolete guide references, agent command blocks or links into agent procedures remain in reader documentation.
- Reviewed the diff against shared working instructions and the Specification Agent role. The shared manifesto, application code and historical project records are unchanged.
- Flow review: all Batches remain closed; no other active Card or blocker. Unrelated local files remain excluded from publication.

## History

- 2026-11-14 — User identified runner as an unclear guide name and assign-a-task as a missing user guide. Extend the same action-oriented naming and coverage to routine resumption and defect reporting.

- 2026-11-14T02:08:30+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T02:11:10+01:00 — Stage moved from `development` to `completion`.
