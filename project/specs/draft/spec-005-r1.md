---
type: specification
id: "SPEC-005"
revision: "1"
---
# Scheduled Batch execution and recovery

## Expected outcome

A recurring job reads durable Batch records and dispatches the next authorized action. KR Developer runs through the configured Codex or Claude Code engine on the designated Batch worktree. The job uses the same Batch rules regardless of the engine.

## Trigger order

On each tick, acquire the repository's exclusive lock and recheck the records. Execute at most one action in this order:

1. Resume an interrupted closure from its verified recovery evidence.
2. Close a decided Batch after verifying the explicit User decision against the exact tested revision. Publish accepted work or archive rejected work with a partial records-only commit to main.
3. Dispatch a recorded correction request on the current Batch branch. Resume a previously claimed request if its execution stopped and no agent still owns it.
4. Resume interrupted development on its existing branch after verifying its recorded state and ownership.
5. Pick up an approved ready Batch only when no other Batch is active and the approval snapshot passes verification.

An isolated KO verdict, a Batch awaiting acceptance tests or a User decision, and an idle repository produce no development action. Missing or conflicting evidence blocks the affected action and is reported. Refuse overlapping work across ticks and require shared coordination before enabling multiple clones.

## Correction handoff

KR Writer records a machine-readable correction request in the Batch records. Include a stable request ID, Batch ID, tested revision, blocking scenario, expected and observed behavior, evidence links, and affected or blocked tests. A request is actionable only for the matching open Batch and candidate. Preserve prior verdicts and the frozen artifact.

The scheduler records its claim durably and dispatches KR Developer on the same Batch branch. The agent corrects within the approved scope, verifies the change, and records a new candidate commit and build. A repeated tick must resume or reconcile the same claim without launching duplicate work. KR Tester resumes acceptance on the new candidate, starting with the failed scenario, then the affected and newly unblocked tests. The User retains the final acceptance or rejection decision.

## Acceptance criteria

- Exercise all five action types in isolated repositories, including simultaneous eligible actions, and verify the priority order and one-action-per-tick behavior.
- Verify that a KO without a correction request, a delivered Batch awaiting a decision, and an idle repository do not launch the engine.
- Exercise correction with Codex and Claude Code. Verify that the job uses the existing branch and a second tick does not duplicate an active claim. Interrupt and resume one correction without losing evidence.
- Replay accepted and rejected closure and interrupt after publishing recovery evidence. Verify the next tick completes the same closure and that rejected product changes remain outside main.
- Verify that missing approval, stale correction requests, decision and revision mismatches, and a held lock prevent unauthorized changes. Report delivered, blocked, and closed outcomes through the configured notification channel.
- Verify end-to-end invocation by the scheduler in an isolated environment before enabling live operation.

## Resources

- [Scheduled job procedure](../../../agents/actions/scheduled-batch-job.md) describes the existing closure-first procedure.
- [Batch operations](../../../agents/guidelines/batches.md) defines approval, correction, coordination, and closure rules.

## Editorial alignment

On 2026-11-15, under the approved CARD-00000141 migration plan, role names and acceptance ownership were aligned with KR Writer, KR Developer and KR Tester. This scheduler draft still awaits scope approval and execution authorization.
