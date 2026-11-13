---
type: card
id: "TASK-00000068"
batch: null
specifications: []
---

# TASK-00000068 — Standardize core Kanban stages

- Owner: Development Agent
- Dependencies:

## Expected outcome

Use Cancellation as the terminal Kanban stage for tasks explicitly abandoned.

## Acceptance criteria

- [x] Rename the Kanban stage and directory to `cancellation` in the repository board and built-in workflow templates. Update the workflow configuration, transitions, instructions, and local links.
- [x] Migrate existing cards with their stable IDs, history, and cancellation rationale. Preserve immutable historical records and support existing adopted boards until they choose to migrate.
- [x] Verify that cancelled cards are excluded from completed throughput. Run the board validator and adoption tests.

- [x] Require Backlog, Development, Completion, and Cancellation in new workflows, including custom workflows. Preserve compatibility with existing boards.

## Execution and evidence

- State: completed
- Actual start: 2026-11-13
- Actual finish: 2026-11-13
- Blocker:

## History

- 2026-11-13T21:49:26+01:00 — Stage moved from `backlog` to `development`.

- Verified the migrated card byte for byte, the separate Cancellation and Completion stages, and all eleven adoption tests.

- 2026-11-13T21:50:20+01:00 — Stage moved from `development` to `code-review`.

- 2026-11-13T21:50:20+01:00 — Stage moved from `code-review` to `completion`.
