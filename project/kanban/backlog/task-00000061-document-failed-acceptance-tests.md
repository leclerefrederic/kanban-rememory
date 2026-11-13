---
type: card
id: "TASK-00000061"
batch: null
specifications: []
---
# TASK-00000061 — Record evidence for failed acceptance tests

- Owner: Specification Agent
- Dependencies: Batch-003 must be delivered before implementation.

## Expected outcome

Make each failed acceptance test reproducible from the Batch records.

## Acceptance criteria

- [ ] After a KO, ask what happened and request the exact error and a screenshot before presenting the next test.
- [ ] Record the observed behavior under the relevant test and case. Store supplied screenshots in the Batch's evidence directory and link them from the result. Record when a screenshot is unavailable.
- [ ] Verify the procedure with one KO accompanied by a screenshot and one KO without a screenshot.
