# Resume recorded work

Read the assigned role, Card/Batch status, owner and checkpoint. Search Rememory by stable ID and read the latest relevant entry/evidence; expand only when the history is needed. Do not load every daily journal. Reconcile dependencies, authorization and role-permitted Git evidence. Conflicting records stop dependent work; report what disagrees.

For Cards, find the existing file across configured stages, keep interrupted/blocked work there and follow [Kanban rules](../guidelines/kanban.md). Reuse authorization for the same action; do not reopen completed Cards. The Orchestrator resumes the existing native child when available, otherwise establishes whether ownership stopped before replacing it.

## Delivered Batch

Read Description, tests, report in that order: status, full candidate/results, User decision/closing evidence. Handoff locates approval ref, branch, worktree and guard. Developer verifies Git; Writer/Tester request that evidence through the Orchestrator rather than operate Git.

If delivered with decision pending, confirm the full commit exists and matches repeated records. Route pending executable cases to [Tester](../roles/tester.md#run-and-guide-acceptance) with complete startup. For blocking debt, continue independent tests and arrange authorized correction or record rejection. Preserve previous candidates and blocked cases. Only once all required tests pass and blocking debt is resolved, ask the User's explicit delivery decision, including nonblocking deferrals. Individual OK verdicts do not accept the Batch.

## Interrupted development or closure

Resume the same Batch state/branch under the recorded authority and [development procedure](develop-batch.md). Preserve frozen artifacts and recover a missing guard before edits. For a recorded decision or recovery ref, [close/recover](close-batch.md) before selecting new work.

## Closed Batch

Verify closed Description and report decision against the exact tested commit. Developer finds the matching closing trailer on main, for example:

```sh
git log main --format='%H %(trailers:key=Batch-Closure,valueonly)' -- project/batches/batch-001
```

Verify the commit records that decision/state. Accepted candidate is an ancestor of main and its tag resolves to it; rejected candidate is outside main and its archive branch resolves to it. Use fully qualified refs. Verify published closing evidence and [remaining branch cleanup](close-batch.md#retire-temporary-branches). Retrieve candidates from durable archives, never reopen the Batch. Report retained temporary refs/worktrees and reason. For older history use original IDs, `Lot-Closure` and the original `lots/`/`Lots/` path.
