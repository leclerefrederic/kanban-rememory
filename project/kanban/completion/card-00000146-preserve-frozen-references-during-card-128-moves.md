---
type: card
id: "CARD-00000146"
batch: null
specifications: []
---

# CARD-00000146 — Preserve frozen references during CARD-128 moves

- Owner: KR Developer
- Dependencies:

## Expected outcome

CARD-128 can move through the board without updating three frozen documents.

## Scope and authorization

The User approved exactly the three historical references from CARD-95, CARD-96 and approved SPEC-012 r2. Preserve those links and accept their retired targets; preserve normal behavior for all other links.

## Acceptance criteria

- [x] CARD-128 moves through Development and Completion in a fixture with frozen files byte-identical.
- [x] Active links update, unrelated invalid links fail validation, and the board tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

Verification in Development: reviewed scoped diff; 37 Kanban tests and live board validation passed. Targeted regression checked both moves, byte-identical historical files and rejection of an active stale link.

## History

- 2026-11-15T13:14:34+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T13:15:33+01:00 — Stage moved from `development` to `completion`.
