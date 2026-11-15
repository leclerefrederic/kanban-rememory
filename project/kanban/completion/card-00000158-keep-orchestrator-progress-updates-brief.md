---
type: card
id: "CARD-00000158"
scope: "agents"
batch: "Batch-014"
specifications: ["SPEC-022"]
---

# CARD-00000158 — Keep Orchestrator progress updates brief

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

During Card or Batch execution, the User sees a live progress line in the original chat, including while a delegated or long-running step is in progress. Messages that ask the User to decide or act retain enough context to answer.

## Scope and authorization

- Post one short, visible line at the start of each meaningful stage, before waiting on a tool or delegated action. Use the conversation language. Examples: “Breaking the Batch into tasks”, “Calling KR Developer”, “Running regression tests”, “Ready for acceptance”, “Publishing”.
- During a long stage, post a brief progress line at a meaningful checkpoint, or confirm that the same stage is still in progress if it lasts about a minute with no new checkpoint. Report a count only when it is measured. Distinguish active work from a wait for a decision or an actual blocker.
- Keep routine tool operations, test details, verification logs and successful notification receipts in the existing records. If a finding materially changes the outcome or calls for User action, explain the evidence and requested decision.
- For completion, state the result briefly. Keep existing acceptance, publication and notification behavior.
- The User authorized development of agents/SPEC-022 on 2026-11-15. This Card tracks implementation in agents/Batch-014.

## Acceptance criteria

- [x] Review the Card and Batch progress guidance and replay the long delegated step. Fresh Codex showed brief labels before delegation and during the wait on the accepted correction.
- [x] Review the interaction and completion scenarios. The earlier controlled simulations and the User's acceptance of the correction are recorded in the Batch. No further replay was requested.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15: Reviewed the scoped correction diff and required checks in Development. The User accepted candidate `f18e413db9ae6d61f8e84e4d6e91b1a682e274a8` and requested publication. See the [Batch record](../../modules/agents/batches/batch-014/report.md).

- 2026-11-15: Local correction `f18e413db9ae6d61f8e84e4d6e91b1a682e274a8` limits routine progress to a stage label. Fresh Codex replay pending. Earlier delivery evidence retained.

- 2026-11-15: Candidate `ce9633e2614977c9c35f31294c6a3c6949aff203` verified on `origin/codex/batch-014`. Waiting for guided acceptance in the original chat.

- 2026-11-15T17:54:43+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T18:23:34+01:00 — Stage moved from `development` to `completion`.
