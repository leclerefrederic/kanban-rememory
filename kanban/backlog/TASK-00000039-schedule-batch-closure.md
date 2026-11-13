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

- [ ] Resume an interrupted closure or handle a validated or rejected Batch before picking up a ready Batch.
- [ ] Verify that the explicit User decision in Report.md applies to the tested commit in Tests.md. Leave the Batch in place and signal a blocker when the decision is missing or the evidence disagrees.
- [ ] Apply the accepted merge or rejected archive procedure. Write the Closure evidence section in Report.md and verify publication before reporting completion.
- [ ] Verify accepted and rejected paths and replay an interruption after Git operations and before publication. The next scheduled run completes the same closure without duplicate commits or conflicting refs.
