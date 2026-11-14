---
type: card
id: "TASK-00000132"
batch: null
specifications: []
---
# TASK-00000132 — Remove the KRR companion app

- Owner: Development Agent
- Dependencies: none
- Approval and priority: The User explicitly requested removal of the app and its references, and asked to delegate execution to the Development Agent on 2026-11-14.

## Expected outcome

The repository provides the Kanban Rememory framework without the retired companion app.

## Scope

Remove the app under `apps/`, its guides, dedicated tooling and tests, and related references in active files. Preserve Batch records, Specifications, existing Cards, the framework and Telegram setup.

## Acceptance criteria

- [x] The app tree, app-specific tooling and active app documentation are removed.
- [x] The framework and Telegram tests pass, and documentation links resolve.
- [x] Historical Batch records, Specifications and Cards stay intact.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14

## History

- 2026-11-14T23:39:17+01:00 — Stage moved from `backlog` to `development`.
- Actual finish: 2026-11-14
- Verified in Development: 32 framework tests, 22 Telegram setup tests, board validation, skill synchronization, diff review and whitespace checks.
- The retired operating guide was replaced with a pointer to its Git history so two immutable completed Cards keep resolving. No active document links to the old guide.
- Flow review: this was the only Development Card. Batch-009 was handled separately and its candidate files were preserved.
- See [Rememory](../../rememory/runner-removal/2026-11-14.md).

- 2026-11-14T23:40:21+01:00 — Stage moved from `development` to `completion`.
