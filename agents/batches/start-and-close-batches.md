# Batch pickup and closure

## Record approval

Specification Agent records explicit User scope approval and execution authorization in the Handoff section of `report.md`, identifying the Batch, ordered mission, and exact Specification revisions. Before starting development, Development Agent checks the Batch's `ready` description and its pinned Specifications against that approval and creates the Git approval commit from the matching snapshot, including required resources. If the approval or snapshot is unavailable or differs, stop and ask the User. Keep this commit on a dedicated ref such as `refs/heads/batch-approval/batch-001`, available to the coding agent. Do not add the commit's own ID to its pinned `description.md`.

Development Agent completes the same Handoff section with the full approval commit and ref, base main commit, working branch (for example `<agent>/batch-001`), designated worktree, and guard path when applicable. Add the approval commit ID after creating it; the report is not part of the immutable scope comparison. Cross-check the handoff against the User approval and trusted ref rather than deriving authorization from files under review. Preserve these records in the designated worktree and closing commit. Before switching or removing a worktree, preserve its uncommitted Batch records; do not discard them with rejected code.

Before pickup, run the board validator and run `python3 agents/tools/manage-kanban-board.py verify-approval Batch-001 APPROVED_COMMIT_ID` with the full commit ID from the trusted approval record. The command compares the ready Description, each pinned Specification and the files under `project/specs/resources/` linked in each Specification's Resources section byte for byte. Other linked files are references and may change; move a binding file into that folder to protect it. A resource moved to `project/specs/resources/archived/` with the same bytes still matches. Obtain the commit ID from the approval record independently of the files being checked. If they differ, stop and surface the discrepancy. Keep the approval record when the Batch closes.

## Take ownership

Use one designated worktree for Batch operations. For each pickup, acquire an exclusive repository lock before reading or updating the Batch status. An atomic directory creation in the shared Git directory can serve as the lock for sessions using the same clone. If the lock exists, leave the Batch untouched. After an interruption, verify that the previous operation has stopped and inspect its branch and status before clearing a stale lock. Separate clones require a shared coordinator before scheduled pickup is enabled.

Under the lock, recheck that the Batch is ready, no other Batch is active, and its approval and Specification checks pass. Run the approval command under the same lock immediately before pickup. Create the Batch branch from the recorded main revision, then record the start. If the branch already exists after an interruption, verify its origin and resume the same Batch. Release the lock at the end of the operation.

## Record debt and resume acceptance

Every observed defect opens debt, including defects found during an OK test. Record each defect once in the Batch report with a stable reference, the affected Specification and test, severity, impact, and whether it blocks acceptance. Use S0 for an unusable system, S1 for an essential workflow without an acceptable workaround, S2 for degraded operation, and S3 for a minor defect. Record test verdicts independently. List each blocked or unexecuted required scenario in tests.md with its original ID and expected result, and link it to the report where applicable.

A blocking defect prevents acceptance. Continue independent scenarios where possible. Specification Agent records the correction request in `report.md`: tested revision, failing scenario, expected and observed behavior, evidence, affected or blocked tests, and execution authorization. Development Agent verifies the request and scope, transitions the same Batch from `delivered` to `in-progress`, corrects on its existing branch, and delivers a new candidate commit. Replay failing and affected scenarios before newly unblocked tests. Preserve earlier candidates and results with their revisions. Acceptance requires verification of the correction and all required scenarios. Any remaining nonblocking debt requires an explicit decision to defer it. See the [state table](batch-workflow.md#batch-states-and-transitions).

If the User rejects the Batch, preserve open debt and outstanding tests in the closing records. Unchanged approved Specifications become eligible for selection again. If their requirements change, prepare a new draft revision. Before approving a successor Batch, review prior reports for the selected Specifications and their dependencies. Carry forward relevant open debt and every required outstanding scenario, with its original reference, expected result, and reason it did not run. Include the original failing scenario as a regression check. Resolve blocking debt before dependent work proceeds. Close each debt entry only with evidence of the verified fix and the required test results.

After a Batch closes, its report remains immutable. Resolve inherited debt in the successor report using the original reference, for example `Batch-001-DEBT-01`, and a link to the original report. Record the fix revision, regression and outstanding-test results, and accepted delivery containing the correction. Search later reports for that exact debt reference to find its current disposition. A rejected successor does not resolve debt in the published baseline. Do not change the original report or create a second identity for the same defect. See the [cross-Batch example](delivery-example.md#resolve-debt-in-a-later-batch).

## Close the Batch

Development Agent records the delivered commit and how to test it in `tests.md`. Specification Agent records acceptance results there, summarizes gaps in `report.md`, and records the explicit User decision with a reference to the tested revision. Development Agent verifies that the decision applies to that revision before closing. At delivery, verify that the tested revision is reachable from the Batch branch on the authorized remote and keep that branch until final publication is verified. Before closing, verify that the Batch branch points to that revision and rerun validation and the approval command. After approval, the command permits lifecycle status changes but still compares the remaining description and Specification bytes. Development Agent records the closing file list and tested revision in Closure evidence before switching branches so missing records can be detected.

- **Accepted** — Merge the tested revision into main and tag that revision. On retry, verify ancestry and check that an existing tag points to the same revision before proceeding. Use fully qualified Git refs when the branch and tag share a name, such as `refs/heads/batch-001` and `refs/tags/batch-001`. If the merge conflicts, stop. Verify the resulting main revision before publishing.
- **Rejected** — Create or verify the archive branch at the tested revision. Preserve the code and automated tests on that branch. On main, create a new partial closing commit with the approved Specifications, Batch documents including debt and outstanding tests, and any applicable standalone Kanban records. Inspect the staged paths before committing. Keep rejected product code and automated test changes on the archive branch. Preserve the existing main history.

Record the closed status and decision in a closing commit intended for main. Include a `Batch-Closure: Batch-001` trailer with the actual Batch ID. Before publishing the archive branch or the accepted tag, publish the closing commit under `refs/heads/batch-recovery/batch-001`. Verify that the remote recovery ref points to the exact closing commit and that it contains the expected records. If a recovery ref already exists, verify it and stop on any discrepancy. Publish recovery refs only to a remote authorized to store the Batch records.

If the original worktree is unavailable, fetch the recovery ref and inspect its commit, decision, tested revision, and staged-path evidence. Verify or recreate the archive branch or tag at the tested revision. For acceptance, verify that the closing commit contains the tested revision in its ancestry. For rejection, verify that the closing commit excludes the tested revision. Publish the recovered commit to main using a fast-forward push. If main has diverged, stop for reconciliation and retain the recovery ref. If the closing commit is already present on main, verify the final refs and finish without another commit.

If a Batch was archived before a recovery ref existed, recover the closing records from a trusted copy before continuing. After publication, finish by [retiring the temporary branches](#retire-temporary-branches).

This procedure can be followed manually by Development Agent. The [scheduled-job procedure](../run-scheduled-batch-job.md) documents closure and recovery priority; it is not an installed scheduler. Automated dispatch of corrections, interrupted development, and pickup still requires implementation and end-to-end verification. Installing the kit does not enable autonomous Batch execution.

For a fresh session handling a delivered or closed Batch, see [the handoff guide](resume-a-batch.md).

## Retire temporary branches

As part of closing a Batch, retire its working branch and recovery branch once the final publication is verified. Record the fully qualified working, recovery and durable archive refs in Closure evidence. Their expected tips are the tested revision for the working branch and the closing commit for the recovery branch. Keep the approval ref.

1. On the authorized remote, verify that main contains the exact closing commit and that the durable archive points to the exact tested revision. For acceptance the archive is the Batch tag and the candidate must be an ancestor of remote main. For rejection the archive is the designated archive branch and the candidate must remain outside remote main's ancestry. Compare published refs, not stale remote-tracking refs. Fetch the published objects if needed for ancestry checks. Resolve an annotated tag to its commit.
2. For each temporary ref, verify that it belongs to the Batch, differs from main and from every retained archive or approval ref, and still points to its expected tip. Use a fully qualified ref and an exact lease for deletion. For example, after verifying the remote recovery ref and setting `temporary_ref` and `expected_tip` to that ref and the full closing commit:

   ```sh
   git push --force-with-lease="$temporary_ref:$expected_tip" origin ":$temporary_ref"
   ```

   Use the tested commit as the expected tip when deleting the working ref. Treat a confirmed absent ref as already retired. If a ref moved or verification fails, preserve the affected ref and report the discrepancy. If final publication or the archive cannot be verified, preserve both temporary refs.
3. Check the remote again to confirm removal and preservation of main and the archive. Check local refs separately. Delete a local temporary branch with `git branch -d` only if it is at the expected commit, has no checked-out worktree and its tip is reachable from a verified retained ref. Use the retained ref as the branch's upstream if needed to make that ancestry check explicit. Preserve branches with unexpected commits and leave occupied worktrees alone. If Git refuses a safe deletion, report what remains. Do not force local deletion as part of routine closure.

A retry uses the same closing commit and archive. It verifies them again and finishes only the remaining cleanup, without another closing commit or archive.

## Protect acceptance builds

For a Batch delivering a build artifact, keep its guard at `<git-common-dir>/kanban-rememory/batch-001/guard.json`, substituting the Batch directory. Obtain the absolute shared Git directory with `git rev-parse --path-format=absolute --git-common-dir`. Create the parent directory and initialize the JSON with the full trusted base commit and authorized Card IDs:

```json
{"base_revision": "FULL_BASE_COMMIT", "authorized_cards": ["CARD-00000001"]}
```

If the project has files whose changes need a full build before publication, such as a build script, add their file names when creating the record: `"full_build_files": ["build.sh"]`. Leave the field out when no file needs this check.

Record the absolute guard path in `report.md` Handoff, not its Card IDs. The guard is local operational data shared by worktrees of that clone; it is not in a fresh clone. If it is unavailable, stop and recover the recorded revision, artifact and verification evidence before resuming. Keep it outside the artifact directory. Run `python3 agents/tools/guard-batch-work.py change RECORD --card CARD-ID` before changing code, build scripts, or delivery artifacts. Put unrelated work in Backlog until delivery. The guard enforces checks when invoked; it is not a Git hook or a replacement for acceptance review.

Run `python3 agents/tools/guard-batch-work.py freeze RECORD --artifact PATH` before starting acceptance. The recorded digest covers file names, bytes and the executable bit; a record frozen before the executable bit was included must be frozen again. Keep the recorded artifact in place and run `verify RECORD` before resuming acceptance. When a documented KO blocks required scenarios, record its test ID and run `python3 agents/tools/guard-batch-work.py correct RECORD --card CARD-ID --blocking-test TEST-ID`. The authorized Development card can then proceed through the change check. Preserve the frozen artifact and build the correction at a separate path. Publication stays blocked during correction.

After committing the correction, retain the previous verdicts and record the affected tests as pending for the new candidate. Run `python3 agents/tools/guard-batch-work.py freeze RECORD --artifact NEW-PATH --restart` with the new commit checked out. The guard retains the previous candidate reference and clears prior publication evidence. Revalidate the failing, affected, and newly unblocked tests before recording a new decision.

Before publishing an accepted delivery to main, record `verification` with `revision` and `technical_checks: "passed"`. If the guard record lists file names in `full_build_files` (empty by default), a change to any of them also requires `full_build: "passed"` after a successful full build. Record `decision` with the User-approved `revision` and `result: "accepted"`. Run `python3 agents/tools/guard-batch-work.py publish RECORD` as a required step before pushing; add `--revision COMMIT` when the commit to publish is not the checked-out `HEAD`. For a rejected delivery, record `decision` with the rejected `revision` and `result: "rejected"`: `publish` then checks that this revision stays out of the published history and does not require the technical checks. Keep evidence of each check in the Batch records.

To run that check automatically, enable the optional push check once per clone with `git config core.hooksPath agents/tools/git-hooks`. When a push to `main` moves a Batch to `closed` and the Batch has a guard record, the hook runs `publish` on the pushed commit, for an accepted or a rejected closure, and refuses the push if it fails. Other pushes are not checked, and work that bypasses Git is not covered.
