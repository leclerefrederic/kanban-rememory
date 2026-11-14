---
type: batch
id: "Batch-101"
specifications: [{"id":"SPEC-101","revision":"1","path":"project/specs/approved/spec-101-r1.md"}]
status: closed
---

# Deliver reliable booking exports

> Fictional example, shown after accepted closure. In the example project, this file is `project/batches/batch-101/description.md`. The path in its header identifies the approved Specification in that fictional project.

## Objective

Deliver [SPEC-101 revision 1](project-specification.md): preserve accented names and names containing commas in the existing CSV export.

## Execution constraints

The selection contains one Specification, so there is no competing mission priority. Keep its approved revision unchanged throughout implementation and correction.

Use the existing export action. Both [acceptance cases](batch-tests.md) must pass on the final candidate before the User accepts delivery. The agreed delivery point is verified merge and publication to `main`; production deployment is outside this Batch.

The [report](batch-report.md) preserves scope approval, correction, the User's acceptance decision and closure evidence. `closed` describes completion of that process; the decision in the report distinguishes acceptance from rejection.

Return to the [example reading order](../index.md#a-complete-example).
