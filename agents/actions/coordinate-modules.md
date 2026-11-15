# Coordinate a module delivery

For a configured multi-module project. Read [shared rules](../guidelines/working-rules.md). The module's Card WIP and delivery ownership both apply. Work from the recorded module branch and worktree. Keep tracking records in the primary checkout, separate from product changes on delivery branches.

1. Confirm selected module, approved scope, authorization, dependencies, intake eligibility and recorded owner. Coordinate only in worktrees of a single clone.
2. From the dedicated delivery worktree, use `python3 agents/tools/manage-module-delivery.py --module MODULE status`. Claim the approved delivery with `claim DELIVERY --owner OWNER --base COMMIT` and add `--approval APPROVAL_COMMIT` for a Batch. Use the recorded session ID for OWNER. Use `--owner-token OWNER` for active Card moves. Maintain the next action with `checkpoint DELIVERY --owner OWNER LABEL`. An interrupted session uses the same recorded owner and worktree after confirming the previous session has stopped. Never clear a lock solely because it is old.
3. After development verification and any required acceptance, use `integration begin DELIVERY --owner OWNER`. Record the remote main tip, confirm it matches the integration base, and verify the combined candidate with current main, including affected shared contracts. Use `integration verify DELIVERY --owner OWNER` before publication. Do not overwrite intervening remote work.
4. Release integration with `integration release DELIVERY --owner OWNER` during any decision or blocker, or after verified publication. Retain module ownership, exact candidates and earlier evidence. Before resuming, reacquire integration and recheck main. If integration changes an accepted candidate, apply affected acceptance checks and the existing User decision rule to the changed candidate.
5. Publish a verified standalone Card with `publish-card DELIVERY --owner OWNER --closing CLOSING_COMMIT`. For a Batch use qualified closure below. On closure record local verification and global impact using `milestone EVENT DELIVERY --owner OWNER --summary SUMMARY --revision COMMIT --evidence PATH --shared`. Reuse the event ID on retry. After checking publication remotely, release the module slot with `finish DELIVERY --owner OWNER --revision CLOSING_COMMIT`. Use the [closure rules](close-batch.md) to retire only verified temporary branches.

## Verify the combined revision

Before running checks, create an integration worktree at the expected main tip and assemble the combined revision there. Do not move main to a tentative result. Keep each check's temporary files and artifacts separate with:

```sh
python3 agents/tools/manage-module-delivery.py --module MODULE run-check DELIVERY --owner OWNER -- CHECK_COMMAND
```

Use the runtime directory for test databases and `KR_ARTIFACT_DIR` for builds. Start network fixtures with dynamically assigned loopback ports and independent data. If a fixture requires a fixed shared resource, run its checks in sequence. To record combined verification, add `--integration-checkout PATH` before `--`. Run all required checks as one command against the exact clean checkout. A failed or interrupted rerun invalidates earlier verification.

## Recover a qualified Batch closure

Record the user's exact decision in the Batch report under User decision as ``- Decision: accepted `FULL_CANDIDATE`.`` or the equivalent with `rejected`. Also record the explicit decision context and required evidence. Add `Batch-Closure: MODULE/Batch-NNN` to the closing commit. Verify that closing preserves the accepted product tree, or excludes the rejected candidate. Changes to declared shared sources, configuration, resources or other product paths require acceptance of the new combined revision. A closing commit limited to Markdown tracking records and Batch evidence can preserve a prior decision. A stale product decision releases integration and keeps the module occupied. Review the combined revision and record the new decision before reacquiring and verifying against current main.

With integration ownership and successful combined checks at that closing revision, run `closure prepare Batch-NNN --owner OWNER --closing CLOSING --candidate CANDIDATE --result accepted`; use `rejected` for rejection. Use `closure publish Batch-NNN --owner OWNER` to publish or resume. This verifies the recovery ref, retained tag or archive, and remote main. It stops if main moved before publication. Restore missing local objects from the authorized qualified recovery ref and reconcile the recorded ownership first. Retain the prior record if remote recovery exists; do not replace it on a mismatch.

Qualify recovery and archives with `PROJECT/MODULE/batch-nnn`. Keep artifact guards under the common Git directory at `kanban-rememory/projects/PROJECT/modules/MODULE/batch-nnn/guard.json`. Retire temporary refs only under the [existing lease and verification procedure](close-batch.md#retire-temporary-branches).
