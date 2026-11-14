---
type: card
id: "TASK-00000101"
batch: "Batch-101"
specifications: ["SPEC-101"]
---

# TASK-00000101 — Preserve complete names in the CSV writer

> Fictional example, written and maintained by Development Agent. Its final location in the example project is `project/kanban/completion/task-00000101-preserve-csv-names.md`. This Card tracks execution independently and points to its Batch; the Batch never contains the Card.

- Owner: Development Agent
- Dependencies: None.
- Authorization: User approved and authorized [Batch-101](batch-description.md), selecting [SPEC-101 revision 1](project-specification.md).

## Expected outcome

Correct the existing writer so accents survive UTF-8 export and commas inside a name do not split the field. Add automated regression coverage for both acceptance cases; preserve the export action and other columns.

## Acceptance criteria

- [x] The regression checks preserve `Élodie` exactly and keep `Smith, Alex` in one field without shifting later columns.
- [x] Both acceptance cases pass on the final candidate and the User accepts that revision.
- [x] The diff is reviewed and the accepted delivery is merged and published at the agreed delivery point.

## Execution and evidence

- State: completed
- Actual start: 2026-01-12
- Actual finish: 2026-01-12
- Blocker: None remaining.
- Technical evidence: `candidate-b` passes the two automated export regression checks. The comma case was added after acceptance exposed the missing coverage in `candidate-a`.
- Acceptance evidence: [TEST-01 and TEST-02](batch-tests.md#results-by-attempt) pass on `candidate-b`.
- Delivery evidence: the [accepted decision and closure](batch-report.md#user-decision) identify `candidate-b`, its merge and publication.

Revision labels are fictional stand-ins for actual Git commit IDs. The commit publishing a real Card is found in Git history; a commit cannot contain its own ID.

## History

- 2026-01-12 09:00 — Created in Backlog after authorization; moved to Development with capacity available.
- 2026-01-12 10:00 — Delivered `candidate-a`; Card remains in Development, waiting for the required User acceptance.
- 2026-01-12 10:20 — TEST-02 is KO; acceptance is blocked. Recorded the defect and resumed work after authorization to correct the agreed behavior.
- 2026-01-12 11:00 — Delivered `candidate-b` with regression coverage. State returns to waiting for acceptance.
- 2026-01-12 11:30 — Both cases pass; User accepts `candidate-b`.
- 2026-01-12 11:45 — Merge and publication verified; moved to Completion. Times use Europe/Paris.

Return to the [example reading order](../index.md#a-complete-example).
