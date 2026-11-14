# Worked delivery example

This fictional booking-export example shows how the records fit together. Replace the sample IDs and bracketed evidence with actual project values. Approval, execution, test results, and delivery decisions must come from the real work; the examples do not grant authorization.

## Approved Specification

File: `project/specs/approved/spec-001-r1.md`. Prepare this revision in draft, review it in ready, then move it to approved when the User approves Batch scope.

```markdown
---
type: specification
id: "SPEC-001"
revision: "1"
---
# Preserve booking names in CSV exports

## Expected outcome

Booking staff can export names with accents and commas without repairing the data afterward.

## Scope

Preserve complete names in the existing CSV export. Keep the existing export action and fields.

## Acceptance criteria

- Exporting a booking named "Élodie" and reading the CSV preserves "Élodie" exactly.
- Exporting a booking named "Smith, Alex" and reading the CSV keeps the complete name in one field.

## Resources

None required for this change.
```

## Ready Batch

File: `project/batches/batch-001/description.md`. This is the state after scope approval and before Development Agent pickup.

```markdown
---
type: batch
id: "Batch-001"
specifications: [{"id":"SPEC-001","revision":"1","path":"project/specs/approved/spec-001-r1.md"}]
status: ready
---
# Booking export delivery

## Objective

Deliver the approved CSV preservation behavior and verify both acceptance cases.

## Execution constraints

Use the existing export format and test fixture. Delivery is accepted at verified merge to main.
```

The selection order is the mission priority. Development Agent tracks implementation independently on Cards that may reference `Batch-001` and `SPEC-001`. Batch records do not contain Card references.

## Acceptance tests

File: `project/batches/batch-001/tests.md`. Prepare the scenarios before development. Before `delivered`, Development Agent replaces the candidate placeholders with the exact tested commit, build, and executable startup instructions.

```markdown
---
type: tests
id: "Batch-001-Tests"
batch: "Batch-001"
---
# Acceptance tests

- Tested commit: [full candidate commit, supplied at delivery]
- Environment or prerequisites: [exact build path and launch command], test account and booking fixture.
- Technical evidence: [automated export test results for that commit]

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | SPEC-001 | Export the booking named Élodie and read the CSV. | Name preserved exactly. | Not run | Pending delivery | |
| TEST-02 | SPEC-001 | Export the booking named Smith, Alex and read the CSV. | Name remains in one field. | Not run | Pending delivery | |

## Startup and actions by case

TEST-01 — Open [exact build] using [launch command], sign in with [test account], and load [booking fixture]. Export Élodie and read the CSV. Expect the unchanged name. Stop before editing the exported file. Verdict: OK / KO.

TEST-02 — Open [exact build] using [launch command], sign in with [test account], and load [booking fixture]. Export Smith, Alex and read the CSV. Expect one complete name field. Stop before editing the exported file. Verdict: OK / KO.
```

Each case repeats its startup instructions inside the verdict question. After recording TEST-01, present TEST-02 immediately. On KO, collect the explanation and screenshot, or record that no screenshot is available. A later attempt adds its own revision and verdict; it does not replace the earlier result.

## Report and handoff

File: `project/batches/batch-001/report.md`. Specification Agent records the User's actual approval. Development Agent fills technical handoff fields after creating the approval commit; it must not insert that hash into the pinned description.

```markdown
---
type: report
id: "Batch-001-Report"
batch: "Batch-001"
---
# Batch report

## Handoff

- Scope approval: [User decision and date], SPEC-001 revision 1.
- Execution authorization: [User instruction authorizing development].
- Approval commit and ref: [full commit], refs/heads/batch-approval/batch-001.
- Base main commit: [full base commit].
- Working branch: codex/batch-001.
- Designated worktree: [absolute path].
- Guard record: [absolute shared Git directory]/kanban-rememory/batch-001/guard.json.

## Delivery summary and gaps

Pending development and acceptance.

## Open debt and outstanding tests

No defect observed yet. TEST-01 and TEST-02 remain to be executed on the delivered candidate.

## Correction request

None.

## User decision

Pending acceptance of the delivered revision.

## Closure evidence

Pending delivery decision and publication.
```

## Resolve debt in a later Batch

Suppose Batch-001 is later accepted with an explicitly deferred, nonblocking display defect, `Batch-001-DEBT-01`. Its closed report stays unchanged. A successor report uses that same reference, links to `../batch-001/report.md`, and records the fix revision, passing regression test, and accepted delivery containing the fix. The original reference still identifies the defect; the successor provides its resolution.

If Batch-001 was rejected with TEST-02 blocked, a successor's tests retain the original reference `Batch-001/TEST-02`, expected result, and reason for the blockage. Fixing the blocker does not pass TEST-02: it must actually run. A rejected successor leaves the debt unresolved in the published baseline.

For the complete sequence, follow [Batch operations](start-and-close-batches.md). For shared attachments, see [Specification resources](batch-workflow.md#specification-resources).
