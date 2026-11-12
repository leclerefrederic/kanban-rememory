# Resume a delivered or closed Lot

Read the Lot's Description, UAT, and Journal in that order. Use Description for status, UAT for the full tested commit and results, and the Journal for the User's decision and closing evidence. If the records disagree, report the discrepancy and keep the Lot at its current state.

## Delivered and awaiting a decision

Confirm that Description says `delivered`, UAT identifies the full tested commit, and the Journal records a pending decision. Verify that the commit exists in Git and matches the revision identified in the Journal if it repeats the value. Report that revision and ask for the User's explicit decision. OK or KO results are evidence for that decision.

## Closed

Confirm that Description says `closed` and the Journal records acceptance or rejection. Use the full tested commit from UAT. Locate the closing commit on main by its exact trailer. For Lot-001, inspect the results of:

```sh
git log main --format='%H %(trailers:key=Lot-Closure,valueonly)' -- Lots/Lot-001
```

Verify that the matching commit records the closed status and the same decision. On acceptance, check that the tested commit is an ancestor of main and that the Lot tag resolves to it. On rejection, check that the archive branch resolves to the tested commit and that the tested commit is outside main's ancestry. Use fully qualified refs for the tag and archive branch. When the closing commit and the required publication evidence agree, report that closure is complete.

When writing the Journal, record the closing trailer and the expected Git refs. These allow an agent to locate the closing commit even though its own hash is unavailable while composing it.
