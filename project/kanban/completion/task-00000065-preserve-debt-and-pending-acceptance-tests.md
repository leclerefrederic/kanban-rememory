---
type: card
id: "TASK-00000065"
batch: null
specifications: []
---
# TASK-00000065 — Preserve debt and pending acceptance tests

- Owner: Development Agent
- Priority: Explicit execution requested by the User.

## Acceptance criteria

- [x] Document debt on OK and KO, blocking correction, and carryover of required tests.
- [x] Verify a partial rejection commit preserves evidence while rejected code stays on the archive branch.

## History

- 2026-11-13T21:33:29+01:00 — Stage moved from `backlog` to `development`.

## Execution evidence

- Isolated Git fixture preserved report and pending tests on main, with rejected code on the archive branch. Eleven board tests passed.

- 2026-11-13T21:33:54+01:00 — Stage moved from `development` to `code-review`.

- 2026-11-13T21:33:54+01:00 — Stage moved from `code-review` to `completion`.
