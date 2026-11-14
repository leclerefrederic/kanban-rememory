# Lot-001 acceptance tests

[Description](description.md) · [Lot Journal](report.md)

## Environment and prerequisites

Tested revision: `2a56a7b3f70a4965a897bb129fb34f07acd13e1c` on `refs/heads/lot-001`. Use the [handoff guide](../../../agents/batches/resume-a-batch.md) with the local Git fixture at `/tmp/kr-lot001-uat.ImjrGa`. For UAT-01 read the Lot files at `refs/heads/uat-delivered`. For UAT-02 read them at `refs/heads/main`. The fixture's tested commit is `a856daf0597dc48e1e23823841ed1b62da0f7504` and its closing commit is `20ce44201513d523213d0962f3e35aa21e916e5e`.

## Scenarios and expected results

| ID | Scenario | Expected result |
| --- | --- | --- |
| UAT-01 | In a fresh session, read a delivered Lot with completed acceptance results and no recorded decision. | The agent identifies the full tested Git commit, reports that the decision is pending, and identifies the next action as obtaining the User's explicit decision. |
| UAT-02 | In a fresh session, read a closed Lot and check the referenced evidence in Git. | The agent identifies the full tested Git commit, recorded decision, closing commit, and merge or archive evidence. It confirms that no closure action remains. |

## Results

Development checks passed.

- UAT-01: OK (User).
- UAT-02: OK (User).
