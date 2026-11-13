# Resume a delivered or closed Batch

Read the Batch's Description, UAT, and Journal in that order. Use Description for status, UAT for the full tested commit and results, and the Journal for the User's decision and closing evidence. If the records disagree, report the discrepancy and keep the Batch at its current state.

## Delivered and awaiting a decision

Confirm that Description says `delivered`, UAT identifies the full tested commit, and the Journal shows the decision is pending. Verify that the commit exists in Git and matches the revision identified in the Journal if it repeats the value. Report that revision and ask for the User's explicit decision. OK or KO results are evidence for that decision.

## Closed

Confirm that Description says `closed` and the Journal records acceptance or rejection. Use the full tested commit from UAT. Locate the closing commit on main by its exact trailer. For Batch-001, inspect the results of:

```sh
git log main --format='%H %(trailers:key=Batch-Closure,valueonly)' -- project/batches/batch-001
```

Verify that the matching commit records the closed status and the same decision. On acceptance, check that the tested commit is an ancestor of main and that the Batch tag resolves to it. On rejection, check that the archive branch resolves to the tested commit and that the tested commit is outside main's ancestry. Use fully qualified refs for the tag and archive branch. When the closing commit and the required publication evidence agree, report that closure is complete.

Development Agent records the closing trailer and expected Git refs in the Closure evidence section of report.md. These allow an agent to locate the closing commit even though its own hash is unavailable while composing it.

## Replay the pilot acceptance scenarios

From a fresh kit clone, run `python3 tools/replay-batch-uat.py /tmp/batch-uat-replay` with a path that does not yet exist. The command creates a separate Git repository and prints the tested and closing commits. Use the three records at `uat-delivered` for the pending-decision scenario and those at `main` for the closed scenario. Compare each answer with the commits printed by the fixture and verify the closing trailer and tag in Git.

For historical records, use the original ID and `Lot-Closure` trailer. Include the historical `lots/` or `Lots/` path in the Git log query when the closure predates the directory migration.
