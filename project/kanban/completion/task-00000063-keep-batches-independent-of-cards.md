---
type: card
id: "TASK-00000063"
batch: null
specifications: []
---
# TASK-00000063 — Keep Batches independent of Cards

- Owner: Development Agent

## Acceptance criteria

- [x] Document that Batch records contain Specification references and evidence. Card references are maintained on Cards.
- [x] Reject Card IDs and links in new Batch records while preserving existing historical records.

## History

- 2026-11-13T21:03:43+01:00 — Stage moved from `backlog` to `development`.

## Execution evidence

- Validator rejects Card IDs and board links in Batch records. Existing historical references remain readable. Eleven board tests passed.

- 2026-11-13T21:04:54+01:00 — Stage moved from `development` to `code-review`.

- 2026-11-13T21:04:54+01:00 — Stage moved from `code-review` to `completion`.
