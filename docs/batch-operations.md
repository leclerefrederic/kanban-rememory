# Batch pickup and closure

## Record approval

Specification Agent records the explicit User approval with the exact Batch ID, ordered mission, and frozen Specification revisions. It makes the approved snapshot available to Development Agent through the handoff. Before starting development, Development Agent checks the ready files against that approval and creates the Git approval commit from the matching snapshot. If the approval or snapshot is unavailable or the files differ, stop and ask the User. Keep this commit on a dedicated approval ref. Record its full commit ID in the Batch's operating record. The approval ref must be available to the coding agent. Capture approval separately from the later acceptance decision.

Before pickup, run the board validator and run `python3 tools/board.py verify-approval Batch-001 APPROVED_COMMIT_ID` with the full commit ID from the trusted approval record. The command compares the ready Description and each pinned Specification byte for byte. Obtain the commit ID from the approval record independently of the files being checked. If they differ, stop and surface the discrepancy. Keep the approval record when the Batch closes.

## Take ownership

Use one designated worktree for Batch operations. For each pickup, acquire an exclusive repository lock before reading or updating the Batch status. An atomic directory creation in the shared Git directory can serve as the lock for sessions using the same clone. If the lock exists, leave the Batch untouched. After an interruption, verify that the previous operation has stopped and inspect its branch and status before clearing a stale lock. Separate clones require a shared coordinator before scheduled pickup is enabled.

Under the lock, recheck that the Batch is ready, no other Batch is active, and its approval and Specification checks pass. Run the approval command under the same lock immediately before pickup. Create the Batch branch from the recorded main revision, then record the start. If the branch already exists after an interruption, verify its origin and resume the same Batch. Release the lock at the end of the operation.

## Close the Batch

Development Agent records the delivered commit and how to test it in tests.md. Specification Agent records UAT results there, summarizes gaps in report.md, and records the explicit User decision in report.md with a reference to the tested revision in tests.md. Development Agent verifies that the decision applies to that revision before closing. At delivery, verify that the tested revision is reachable from the Batch branch on the authorized remote and keep that branch until final publication is verified. Before closing, verify that the Batch branch points to that revision and rerun validation and the approval command. For a decided Batch, the approval command allows the status line to change and checks the remaining Description and Specification bytes. Development Agent records the closing file list and a reference to the tested revision in the Closure evidence section of report.md before switching branches so missing records can be detected.

- **Accepted** — Merge the tested revision into main and tag that revision. On retry, verify ancestry and check that an existing tag points to the same revision before proceeding. Use fully qualified Git refs when the branch and tag share a name, such as `refs/heads/batch-001` and `refs/tags/batch-001`. If the merge conflicts, stop. Verify the resulting main revision before publishing.
- **Rejected** — Create or verify the archive branch at the tested revision. Preserve the code and automated tests on that branch. On main, stage the approved Specifications, Batch documents, relevant Cards, and any approved Backlog records. Inspect the staged path list before committing. Keep the product code off main.

Record the closed status and decision in a closing commit intended for main. Include a `Batch-Closure: Batch-001` trailer with the actual Batch ID. Before publishing the archive branch or the accepted tag, publish the closing commit under `refs/heads/batch-recovery/batch-001`. Verify that the remote recovery ref points to the exact closing commit and that it contains the expected records. If a recovery ref already exists, verify it and stop on any discrepancy. Publish recovery refs only to a remote authorized to store the Batch records.

If the original worktree is unavailable, fetch the recovery ref and inspect its commit, decision, tested revision, and staged-path evidence. Verify or recreate the archive branch or tag at the tested revision. For acceptance, verify that the closing commit contains the tested revision in its ancestry. For rejection, verify that the closing commit excludes the tested revision. Publish the recovered commit to main using a fast-forward push. If main has diverged, stop for reconciliation and retain the recovery ref. If the closing commit is already present on main, verify the final refs and finish without another commit.

Keep the recovery ref until the remote main and archive branch or tag have been verified. Remove it only after verification. If a Batch was archived before a recovery ref existed, recover the closing records from a trusted copy before continuing.

The procedure is manual. Scheduled closure is pending. See Kanban card TASK-00000039 for closure priority and retry criteria. Enable scheduled pickup only after verifying coordination in the deployment environment.

For a fresh session handling a delivered or closed Batch, see [the handoff guide](batch-handoff.md).
