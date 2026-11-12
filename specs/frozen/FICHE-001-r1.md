# Resume a delivered or closed Lot from its records

- Fiche ID: FICHE-001
- Revision: 1

## Expected outcome

An agent starting a fresh session can read the three Lot documents and identify the exact revision submitted for acceptance, the recorded decision or its absence, and the next action.

## Scope

Cover two situations: a delivered Lot awaiting the User's decision and a closed Lot with a recorded outcome. Use Description.md for the Lot status, UAT.md for the tested revision and acceptance results, and Report.md for the decision and closure evidence.

## Acceptance criteria

- [ ] Given a delivered Lot without a recorded User decision, a fresh session can identify the full tested Git commit, report that the decision is pending, and identify the next action as obtaining the User's explicit decision.
- [ ] Given a closed Lot, a fresh session can identify the full tested Git commit, report the recorded decision, and locate the closing commit and the merge or archive evidence. It can confirm that no closure action remains for that Lot.

## Acceptance scenarios

1. Open a delivered Lot with completed acceptance results and no decision. Compare the agent's answer with the tested revision in UAT.md and the pending decision in Report.md.
2. Open a closed Lot with a recorded decision and closure evidence. Compare the agent's answer with the Lot records and verify the referenced evidence in Git.
