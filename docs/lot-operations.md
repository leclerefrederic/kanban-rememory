# Lot pickup and closure

## Record approval

When the User approves scope, capture the exact Lot ID, ordered mission, and frozen Fiche mapping in a Git approval commit before starting development. Keep this commit on a dedicated approval ref. Record its full commit ID in the Lot's operating record. The approval ref must be available to the coding agent. Capture approval separately from the later acceptance decision.

Before pickup, run the board validator and compare the mission and Fiche mapping against the approval commit. If they differ, stop and surface the discrepancy. Keep the approval record when the Lot closes.

## Take ownership

Use one designated worktree for Lot operations. For each pickup, acquire an exclusive repository lock before reading or updating the Lot status. An atomic directory creation in the shared Git directory can serve as the lock for sessions using the same clone. If the lock exists, leave the Lot untouched. After an interruption, verify that the previous operation has stopped and inspect its branch and status before clearing a stale lock. Separate clones require a shared coordinator before scheduled pickup is enabled.

Under the lock, recheck that the Lot is ready, no other Lot is active, and its approval and Fiche checks pass. Create the Lot branch from the recorded main revision, then record the start. If the branch already exists after an interruption, verify its origin and resume the same Lot. Release the lock at the end of the operation.

## Close the Lot

Cowork records the User's explicit decision and the full revision submitted to UAT in the Lot Journal. Before closing, verify that the Lot branch points to that revision and rerun validation. Capture the closing file list before switching branches so any missing local records can be detected.

- **Accepted** — Merge the tested revision into main and tag that revision. On retry, verify ancestry and check that an existing tag points to the same revision before proceeding. Use fully qualified Git refs when the branch and tag share a name, such as `refs/heads/lot-001` and `refs/tags/lot-001`. If the merge conflicts, stop. Verify the resulting main revision before publishing.
- **Rejected** — Create or verify the archive branch at the tested revision. Preserve the code and automated tests on that branch. On main, stage the approved Fiches, Lot documents, relevant Cards, and any approved Backlog records. Inspect the staged path list before committing. Keep the product code off main.

Record the closed status and decision in the closing commit on main. Include a `Lot-Closure: Lot-001` trailer with the actual Lot ID. On retry, search main for that trailer and verify that the commit contains the expected records. If the commit exists, resume publication from that commit. If only the archive exists, verify its revision and continue with the closing records. Keep the Lot's local records until the closing commit and branch or tag references are verified on the remote.

The procedure is manual. Enable scheduled pickup only after verifying coordination in the deployment environment.
