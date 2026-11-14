---
type: card
id: "CARD-00000110"
batch: null
specifications: []
---

# CARD-00000110 — Flag the stale sentences of the closed Batch-007 report

- Owner: Development Agent
- Dependencies:

## Expected outcome

A reader of the closed Batch-007 report is not misled by two sentences written before acceptance. The User ordered the modification of this closed record, which is an exception to report immutability. The two sentences are in sections owned by the Specification Agent, so the Development Agent leaves them unchanged and adds one note in its own Closure evidence section. The exception is recorded in the journal.

## Acceptance criteria

- [x] `project/batches/batch-007/report.md` Closure evidence says the "Delivery summary and gaps" and "Open debt and outstanding tests" sentences predate acceptance and that "User decision" is authoritative.
- [x] No other line of the report changed.
- [x] The journal records the exception: the rule, the User's instruction, what was done, date and time.
- [x] Board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:23:05+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:23:32+01:00 — Stage moved from `development` to `completion`.
