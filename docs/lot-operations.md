# Lot pickup and closure

## Record approval

When the User approves scope, capture the exact Lot ID, ordered mission, and frozen Fiche mapping in a Git approval commit before starting development. Keep this commit on a dedicated approval ref. Record its full commit ID in the Lot's operating record. The approval ref must be available to the coding agent. Capture approval separately from the later acceptance decision.

Before pickup, run the board validator and compare the mission and Fiche mapping against the approval commit. If they differ, stop and surface the discrepancy. Keep the approval record when the Lot closes.

## Take ownership

Use one designated worktree for Lot operations. For each pickup, acquire an exclusive repository lock before reading or updating the Lot status. An atomic directory creation in the shared Git directory can serve as the lock for sessions using the same clone. If the lock exists, leave the Lot untouched. After an interruption, verify that the previous operation has stopped and inspect its branch and status before clearing a stale lock. Separate clones require a shared coordinator before scheduled pickup is enabled.

Under the lock, recheck that the Lot is ready, no other Lot is active, and its approval and Fiche checks pass. Create the Lot branch from the recorded main revision, then record the start. If the branch already exists after an interruption, verify its origin and resume the same Lot. Release the lock at the end of the operation.

## Close the Lot

Specification Agent records the User's explicit decision and the full revision submitted to UAT in the Lot Journal. At delivery, verify that the tested revision is reachable from the Lot branch on the authorized remote and keep that branch until final publication is verified. Before closing, verify that the Lot branch points to that revision and rerun validation. Capture the closing file list and the full tested revision in the Lot Journal before switching branches so any missing records can be detected.

- **Accepted** — Merge the tested revision into main and tag that revision. On retry, verify ancestry and check that an existing tag points to the same revision before proceeding. Use fully qualified Git refs when the branch and tag share a name, such as `refs/heads/lot-001` and `refs/tags/lot-001`. If the merge conflicts, stop. Verify the resulting main revision before publishing.
- **Rejected** — Create or verify the archive branch at the tested revision. Preserve the code and automated tests on that branch. On main, stage the approved Fiches, Lot documents, relevant Cards, and any approved Backlog records. Inspect the staged path list before committing. Keep the product code off main.

Record the closed status and decision in a closing commit intended for main. Include a `Lot-Closure: Lot-001` trailer with the actual Lot ID. Before publishing the archive branch or the accepted tag, publish the closing commit under `refs/heads/lot-recovery/lot-001`. Verify that the remote recovery ref points to the exact closing commit and that it contains the expected records. If a recovery ref already exists, verify it and stop on any discrepancy. Publish recovery refs only to a remote authorized to store the Lot records.

If the original worktree is unavailable, fetch the recovery ref and inspect its commit, decision, tested revision, and staged-path evidence. Verify or recreate the archive branch or tag at the tested revision. For acceptance, verify that the closing commit contains the tested revision in its ancestry. For rejection, verify that the closing commit excludes the tested revision. Publish the recovered commit to main using a fast-forward push. If main has diverged, stop for reconciliation and retain the recovery ref. If the closing commit is already present on main, verify the final refs and finish without another commit.

Keep the recovery ref until the remote main and archive branch or tag have been verified. Remove it only after verification. If a Lot was archived before a recovery ref existed, recover the closing records from a trusted copy before continuing.

The procedure is manual. Enable scheduled pickup only after verifying coordination in the deployment environment.
