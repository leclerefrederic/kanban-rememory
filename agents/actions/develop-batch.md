# Develop or correct a Batch

Prerequisites: Developer role, [Batch rules](../guidelines/batches.md), exact User-approved handoff and authorized execution. Work on one Batch in its designated worktree. Cards are Developer-owned implementation records; no Card IDs belong in Batch records.

For a configured multi-module project, apply [module delivery coordination](coordinate-modules.md) for workspace, capacity, runtime resources and integration.

## Verify approval and take ownership

1. Writer records User scope approval/execution authority, ordered mission and exact Spec revisions in report Handoff. Compare the ready Description and pinned approved Specs with that trusted handoff. If authority/snapshot is missing or inconsistent, stop dependent work and ask.
2. Create the matching Git approval commit including required resources; retain a dedicated ref such as `refs/heads/batch-approval/batch-001`. Do not put the commit's own hash in pinned Description. Record the full hash/ref afterward in report Handoff, along with base main commit, working branch, designated worktree and guard path if applicable. Preserve uncommitted Batch records before switching/removing a worktree, even on rejection.
3. In multi-module mode, create the approved dedicated branch/worktree and claim the verified Batch there under the selected module. In single-project mode, acquire an exclusive repository lock before reading/updating pickup status. Atomic directory creation in the shared Git directory works within one clone; another clone needs a shared coordinator. If held, do not change the Batch. Clear a stale lock only after proving its previous operation stopped and inspecting branch/status.
4. Under the applicable pickup lock, recheck ready state, capacity, approval and references. Run:

```sh
python3 agents/tools/manage-kanban-board.py validate
python3 agents/tools/manage-kanban-board.py verify-approval Batch-001 FULL_TRUSTED_APPROVAL_COMMIT
```

`verify-approval` compares ready Description, pinned Spec bytes and linked files under `project/specs/resources/` in each Resources section. Other linked files are references. An identically archived resource matches. Obtain the commit independently from trusted approval records, not files being checked. Keep approval evidence after closure.

5. Create the recorded Batch branch from the agreed main revision if needed, then set in-progress. If it exists after interruption, verify its origin and resume it. Release the lock when the operation ends. Commit product and automated tests on this branch using existing test layout; never commit Batch records there. Respect mission order and technical dependencies.

## Deliver and correct

Record technical decisions, blockers and verification on Cards/Rememory. Record exact candidate, environment, startup instructions and technical evidence in tests.md and technical Handoff fields. Verify that the tested revision is reachable from the authorized remote Batch branch; retain it until final publication. Set delivered and send the configured [delivery notification](notify-user.md). Tester then owns acceptance results; Writer owns summary/decision.

For an authorized blocking correction, verify the request described by [debt policy](../guidelines/batches.md#debt-and-correction), return delivered to in-progress on the same branch and deliver a new candidate. Keep previous candidate/results and revalidate failing, affected and newly unblocked cases. Do not widen scope or overwrite the acceptance artifact. For closure use [close](close-batch.md).

## Protect acceptance builds

For a Batch delivering an artifact, keep its local guard at `<git-common-dir>/kanban-rememory/batch-001/guard.json`; obtain the shared directory using `git rev-parse --path-format=absolute --git-common-dir`. Initialize its parent/JSON with full trusted `base_revision` and `authorized_cards`. Add `full_build_files` only for files whose change requires a full build, such as a build script. Record the absolute guard path (not Card IDs) in Handoff. This local data is absent from a fresh clone: if unavailable, recover revision/artifact/evidence before resuming. Keep it outside artifacts.

Run `python3 agents/tools/guard-batch-work.py change RECORD --card CARD-ID` before code/build/artifact edits; unrelated work waits in backlog until delivery. The guard acts only when invoked, not as a replacement for acceptance.

Before acceptance, `freeze RECORD --artifact PATH` records names, bytes and executable bits. Re-freeze records made before executable-bit protection. Preserve that artifact and run `verify RECORD` before resuming. A documented blocking KO permits `correct RECORD --card CARD-ID --blocking-test TEST-ID` for the authorized Card; correction keeps publication blocked. Build the correction at a new path.

After committing, preserve earlier verdicts and mark affected tests pending for the new candidate. With that commit checked out, run `freeze RECORD --artifact NEW-PATH --restart`; it keeps the previous candidate reference and clears old publication evidence. Revalidate required cases before a new decision. [Closure](close-batch.md#publication-guard) owns the final guard check; [Batch setup](../setup/batches.md) owns optional automatic hook activation.
