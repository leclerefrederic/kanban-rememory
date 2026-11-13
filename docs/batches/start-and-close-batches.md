# Batch pickup and closure

## Record approval

Specification Agent records the explicit User approval with the exact Batch ID, ordered mission, and approved Specification revisions. It makes the approved snapshot available to Development Agent through the handoff. Before starting development, Development Agent checks the ready files against that approval and creates the Git approval commit from the matching snapshot. If the approval or snapshot is unavailable or the files differ, stop and ask the User. Keep this commit on a dedicated approval ref. Record its full commit ID in the Batch's operating record. The approval ref must be available to the coding agent. Capture approval separately from the later acceptance decision.

Before pickup, run the board validator and run `python3 tools/manage-kanban-board.py verify-approval Batch-001 APPROVED_COMMIT_ID` with the full commit ID from the trusted approval record. The command compares the ready Description and each pinned Specification byte for byte. Obtain the commit ID from the approval record independently of the files being checked. If they differ, stop and surface the discrepancy. Keep the approval record when the Batch closes.

## Take ownership

Use one designated worktree for Batch operations. For each pickup, acquire an exclusive repository lock before reading or updating the Batch status. An atomic directory creation in the shared Git directory can serve as the lock for sessions using the same clone. If the lock exists, leave the Batch untouched. After an interruption, verify that the previous operation has stopped and inspect its branch and status before clearing a stale lock. Separate clones require a shared coordinator before scheduled pickup is enabled.

Under the lock, recheck that the Batch is ready, no other Batch is active, and its approval and Specification checks pass. Run the approval command under the same lock immediately before pickup. Create the Batch branch from the recorded main revision, then record the start. If the branch already exists after an interruption, verify its origin and resume the same Batch. Release the lock at the end of the operation.

## Record debt and resume acceptance

Every observed defect opens debt, including defects found during an OK test. Record each defect once in the Batch report with a stable reference, the affected Specification and test, severity, impact, and whether it blocks acceptance. Use S0 for an unusable system, S1 for an essential workflow without an acceptable workaround, S2 for degraded operation, and S3 for a minor defect. Record test verdicts independently. List each blocked or unexecuted required scenario in tests.md with its original ID and expected result, and link it to the report where applicable.

A blocking defect prevents acceptance. Continue independent scenarios where possible. Correct the defect on the open Batch branch within the approved scope, record the new candidate commit, and replay the failing and affected scenarios before running the newly unblocked tests. Preserve earlier results with their tested revisions. Acceptance requires verification of the correction and all required scenarios. Any remaining nonblocking debt requires an explicit decision to defer it.

If the User rejects the Batch, preserve open debt and outstanding tests in the closing records. Unchanged approved Specifications become eligible for selection again. If their requirements change, prepare a new draft revision. Before approving a successor Batch, review prior reports for the selected Specifications and their dependencies. Carry forward relevant open debt and every required outstanding scenario, with its original reference, expected result, and reason it did not run. Include the original failing scenario as a regression check. Resolve blocking debt before dependent work proceeds. Close each debt entry only with evidence of the verified fix and the required test results.

## Close the Batch

Development Agent records the delivered commit and how to test it in tests.md. Specification Agent records UAT results there, summarizes gaps in report.md, and records the explicit User decision in report.md with a reference to the tested revision in tests.md. Development Agent verifies that the decision applies to that revision before closing. At delivery, verify that the tested revision is reachable from the Batch branch on the authorized remote and keep that branch until final publication is verified. Before closing, verify that the Batch branch points to that revision and rerun validation and the approval command. For a decided Batch, the approval command allows the status line to change and checks the remaining Description and Specification bytes. Development Agent records the closing file list and a reference to the tested revision in the Closure evidence section of report.md before switching branches so missing records can be detected.

- **Accepted** — Merge the tested revision into main and tag that revision. On retry, verify ancestry and check that an existing tag points to the same revision before proceeding. Use fully qualified Git refs when the branch and tag share a name, such as `refs/heads/batch-001` and `refs/tags/batch-001`. If the merge conflicts, stop. Verify the resulting main revision before publishing.
- **Rejected** — Create or verify the archive branch at the tested revision. Preserve the code and automated tests on that branch. On main, create a new partial closing commit with the approved Specifications, Batch documents including debt and outstanding tests, and any applicable standalone Kanban records. Inspect the staged paths before committing. Keep rejected product code and automated test changes on the archive branch. Preserve the existing main history.

Record the closed status and decision in a closing commit intended for main. Include a `Batch-Closure: Batch-001` trailer with the actual Batch ID. Before publishing the archive branch or the accepted tag, publish the closing commit under `refs/heads/batch-recovery/batch-001`. Verify that the remote recovery ref points to the exact closing commit and that it contains the expected records. If a recovery ref already exists, verify it and stop on any discrepancy. Publish recovery refs only to a remote authorized to store the Batch records.

If the original worktree is unavailable, fetch the recovery ref and inspect its commit, decision, tested revision, and staged-path evidence. Verify or recreate the archive branch or tag at the tested revision. For acceptance, verify that the closing commit contains the tested revision in its ancestry. For rejection, verify that the closing commit excludes the tested revision. Publish the recovered commit to main using a fast-forward push. If main has diverged, stop for reconciliation and retain the recovery ref. If the closing commit is already present on main, verify the final refs and finish without another commit.

Keep the recovery ref until the remote main and archive branch or tag have been verified. Remove it only after verification. If a Batch was archived before a recovery ref existed, recover the closing records from a trusted copy before continuing.

The procedure is manual. Scheduled closure is pending. See Kanban card TASK-00000039 for closure priority and retry criteria. Enable scheduled pickup only after verifying coordination in the deployment environment.

For a fresh session handling a delivered or closed Batch, see [the handoff guide](resume-a-batch.md).

## Protect acceptance builds

For a Batch delivering a build artifact, keep a local JSON guard record with the trusted `base_revision` and `authorized_cards`. Run `python3 tools/guard-batch-work.py change RECORD --card TASK-ID` before changing code, build scripts, or delivery artifacts. Put unrelated work in Backlog until delivery. Keep the guard record outside the artifact directory.

Run `python3 tools/guard-batch-work.py freeze RECORD --artifact PATH` before starting acceptance. Keep the recorded artifact in place and run `verify RECORD` before resuming acceptance. When a documented KO blocks required scenarios, record its test ID and run `python3 tools/guard-batch-work.py correct RECORD --card TASK-ID --blocking-test TEST-ID`. The authorized Development card can then proceed through the change check. Preserve the frozen artifact and build the correction at a separate path. Publication stays blocked during correction.

After committing the correction, retain the previous verdicts and record the affected tests as pending for the new candidate. Run `python3 tools/guard-batch-work.py freeze RECORD --artifact NEW-PATH --restart` with the new commit checked out. The guard retains the previous candidate reference and clears prior publication evidence. Revalidate the failing, affected, and newly unblocked tests before recording a new decision.

Before publishing an accepted delivery to main, record `verification` with `revision` and `technical_checks: "passed"`. For changes to `build-app.sh`, also record `full_build: "passed"` after a successful full build. Record `decision` with the User-approved `revision` and `result: "accepted"`. Run `python3 tools/guard-batch-work.py publish RECORD` as a required step before pushing. Keep evidence of each check in the Batch records.
