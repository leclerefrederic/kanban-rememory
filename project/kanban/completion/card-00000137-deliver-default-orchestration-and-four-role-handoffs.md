---
type: card
id: "CARD-00000137"
batch: "Batch-011"
specifications: ["SPEC-017","SPEC-018","SPEC-019"]
---

# CARD-00000137 — Deliver default orchestration and four role handoffs

- Owner: Development Agent
- Dependencies:

## Expected outcome

Deliver the approved default Orchestrator startup, Writer and Developer naming and Card boundaries, and KR Tester role in the same workflow.

- Priority: Batch-011 mission authorized by the User.

## Acceptance criteria

- [x] Both host startup entries default to KR Orchestrator and preserve explicitly assigned roles.
- [x] KR Writer prepares only backlog Cards, KR Developer retains execution, and KR Tester owns guided acceptance with matching launch and optional hook instructions.
- [x] Technical checks and approval verification pass, and four isolated user journeys are ready for the exact candidate.

## Execution and evidence

- State: Verified
- Actual start:
- Actual finish: 2026-11-15
- Blocker:

- Board checks: 33 passed, including covered Writer backlog writes, denied active/completed writes, Tester path boundaries and legacy launch compatibility. Telegram checks: 22 passed.
- Both CLIs identified the behavioral default in read-only startup probes. An explicit Claude Tester retained its role. These probes were technical checks rather than User acceptance.
- Four empty, isolated fixtures with independent local bare remotes validate successfully.
- Review and flow: inspected the scoped diff, no blocker; close this implementation Card and proceed with Batch delivery after remote verification.

## History

- 2026-11-15T01:07:26+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T01:14:50+01:00 — Stage moved from `development` to `completion`.
