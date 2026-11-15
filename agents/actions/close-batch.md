# Close or recover a Batch

Developer only. Apply [Batch invariants](../guidelines/batches.md); use the designated worktree and exclusive repository coordination described in [development](develop-batch.md#verify-approval-and-take-ownership). An explicit User decision on the tested revision is required. Standalone Card closure follows project rules separately.

## Close the Batch

1. Reconcile Description state, tests' full candidate/results, Writer's recorded decision and report Handoff. Confirm required tests/blocking debt and any explicit nonblocking deferrals. Verify the branch points to the tested revision, reachable on the authorized remote; rerun `validate` and `verify-approval` with the trusted commit. Lifecycle status changes are permitted by approval verification, not other scope changes. Record closing file list and tested revision in Closure evidence before switching branches; preserve uncommitted records.
2. **Accepted:** merge the tested revision into main and tag that revision. On retry verify ancestry and existing tag target. Use fully qualified refs, especially when branch/tag names coincide. Stop on merge conflicts and verify resulting main before publication.
3. **Rejected:** create/verify the archive branch at the tested revision. Keep rejected code and automated tests there. On main make a partial closing commit containing approved Specs, Batch records (including debt/outstanding tests) and applicable standalone Kanban records only. Inspect staged paths; preserve existing main history.
4. Record closed status/decision in a closing commit for main with trailer `Batch-Closure: Batch-001` using the actual ID. Before publishing accepted tag or rejected archive, publish this commit to `refs/heads/batch-recovery/batch-001` on a remote authorized to hold the records. Verify the exact remote tip and expected records. If an existing recovery ref differs, stop.
5. Apply the [publication guard](#publication-guard) when configured, publish the tag/archive and main, and verify final remote refs/ancestry. Never claim merge, publication or deployment without its evidence. Then [retire temporary branches](#retire-temporary-branches), record closure evidence and send one configured [closure notification](notify-user.md).

## Recover an interrupted closure

If the worktree is unavailable, fetch the recovery ref and inspect its closing commit, decision, candidate and file-list evidence. Verify/recreate archive branch or tag at the exact candidate. Accepted closing history must contain that revision; rejected history must exclude it. Publish to main with a fast-forward push. If main diverged, stop for reconciliation and retain recovery. If main already contains the closing commit, verify final refs and finish without a duplicate commit.

If archival predates recovery refs, recover records from a trusted copy first. Preserve approval evidence. To locate an old closure, inspect the exact `Batch-Closure` trailer on main and verify records/decision/candidate/archive; historical `Lot-Closure` and `lots/`/`Lots/` paths remain valid. A publishing commit cannot contain its own hash; the trailer and expected refs locate it afterward.

If the optional pre-push check refuses, report its message and keep the Batch at its current state until resolved; never bypass it. A retry uses the same closing commit/archive and completes only remaining steps. [Resume](resume-work.md) routes fresh sessions.

## Retire temporary branches

Record fully qualified working, recovery and retained archive refs in Closure evidence. Expected tips: tested revision for working, closing commit for recovery. Preserve the approval ref.

1. Query published remote refs, not stale tracking refs. Verify remote main contains the exact closing commit and archive resolves to the exact candidate (dereference annotated tags). Accepted candidate must be an ancestor of remote main; rejected candidate must stay outside. Fetch objects for ancestry if needed.
2. Verify each temporary ref belongs to this Batch, differs from main/archive/approval and remains at its expected tip. Delete with a fully qualified ref and exact lease, for example:

```sh
git push --force-with-lease="$temporary_ref:$expected_tip" origin ":$temporary_ref"
```

Use the tested commit for the working ref. Confirmed absence means already retired. Preserve moved/unverifiable refs and report discrepancies; if publication/archive cannot be verified, preserve both temporary refs.

3. Query remote again to confirm deletion and retained refs. Separately delete a local temporary branch with `git branch -d` only at its expected commit, with no checked-out worktree and reachability from a verified retained ref. Set that retained upstream when needed to make ancestry explicit. Preserve unexpected commits/occupied worktrees. If safe deletion is refused, report what remains; no routine forced local deletion.

## Publication guard

For an accepted artifact delivery, guard JSON must record `verification` with candidate `revision` and `technical_checks: "passed"`, plus `full_build: "passed"` if changed files appear in `full_build_files`. Record User `decision` with the same revision and `result: "accepted"`. Keep check evidence in Batch records.

Before pushing, run `python3 agents/tools/guard-batch-work.py publish RECORD`; add `--revision COMMIT` when publishing a commit other than checked-out HEAD. For rejection record the rejected revision and `result: "rejected"`; the command checks exclusion from published history and does not require technical passes. [Batch setup](../setup/batches.md) describes the optional automatic pre-push coverage. It checks only applicable closures with a guard, not all pushes or non-Git changes.
