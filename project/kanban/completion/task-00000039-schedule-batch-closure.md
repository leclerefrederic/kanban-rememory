---
type: card
id: "TASK-00000039"
batch: null
specifications: []
---

# TASK-00000039 — Close decided Batches in the scheduled Development Agent job

- Owner: Kanban Rememory maintainers

## Expected outcome

Have the scheduled job close decided Batches and recover interrupted closures before picking up new work.

## Acceptance criteria

- [x] Resume an interrupted closure or handle a validated or rejected Batch before picking up a ready Batch.
- [x] Verify that the explicit User decision in Report.md applies to the tested commit in Tests.md. Leave the Batch in place and signal a blocker when the decision is missing or the evidence disagrees.
- [x] Apply the accepted merge or rejected archive procedure. Write the Closure evidence section in Report.md and verify publication before reporting completion.
- [x] Verify accepted and rejected paths and replay an interruption after Git operations and before publication. The next scheduled run completes the same closure without duplicate commits or conflicting refs.

## History

- 2026-11-13T22:01:55+01:00 — Stage moved from `backlog` to `development`.

## Execution evidence

- The scheduler entry point is documented in `docs/agents/run-scheduled-batch-job.md`.
- An isolated Git remote verified accepted publication, rejected archive publication, and replay after publishing a recovery ref. Scheduler invocation and the agent's evidence checks still need an end-to-end run.

- 2026-11-13 — User accepted the documented procedure and isolated Git checks as sufficient for closure. Scheduler invocation and agent evidence checks were not verified end to end. No recurring job was enabled.

- 2026-11-13T22:04:22+01:00 — Stage moved from `development` to `completion`.
