---
type: report
id: "Batch-101-Report"
batch: "Batch-101"
---

# Booking export delivery report

> Fictional example of `project/batches/batch-101/report.md`, after accepted closure. Dates, decisions, results and revision labels are illustrative. Labels such as `approval`, `candidate-b` and `closure` stand for full Git commit IDs in a real project; they are not executable Git references.

## Handoff

- Scope approval: User approved [SPEC-101 revision 1](project-specification.md) on 2026-01-12 at 09:00 Europe/Paris.
- Execution authorization: User authorized development of [Batch-101](batch-description.md) in the same instruction.
- Approval commit and ref: `approval`, `refs/heads/batch-approval/batch-101`.
- Base main commit: `base`.
- Working branch: `codex/batch-101`.
- Designated worktree: `/tmp/booking-demo/worktree`.
- Guard record: `/tmp/booking-demo/repository/.git/kanban-rememory/batch-101/guard.json`.

Scope approval authorized the work; it did not accept the later delivery.

## Delivery summary and gaps

The export writer now preserves accented names and quotes names containing commas. Both agreed acceptance cases passed on `candidate-b`. The existing export action and columns are unchanged.

The first candidate failed the comma case. Its results were retained, the same open Batch returned to development for authorized correction, and a separate candidate was delivered. See the [results by attempt](batch-tests.md#results-by-attempt).

## Open debt and outstanding tests

| Reference | Severity and acceptance impact | Related test | Resolution |
| --- | --- | --- | --- |
| Batch-101-DEBT-01 | S1 — Major. Names containing commas corrupt the export's columns; acceptance blocked. | TEST-02 | Corrected in `candidate-b`, confirmed by TEST-02 OK and included in the accepted, published delivery. Resolved. |

No open debt or required test remains. TEST-01 was repeated on `candidate-b` because the shared writer changed. Correcting the defect alone did not validate either case; both were executed again. No debt was deferred.

## Correction request

- Recorded on 2026-01-12 at 10:20 Europe/Paris against `candidate-a`.
- Failing test: TEST-02. Expected one complete name field; observed `Smith` and `Alex` in separate fields with later values shifted.
- Evidence: User observation in [TEST-02](batch-tests.md#results-by-attempt). Screenshot requested but unavailable.
- Affected scenarios: TEST-02 fails; TEST-01 must be repeated because correction changes the same writer. No other case is blocked or omitted.
- Authorization: User authorized restoring AC-02 within the unchanged approved Specification. No new requirement was added.
- Follow-through: retained candidate A and its results, resumed the open Batch in development, delivered candidate B at 11:00, then resumed acceptance with TEST-02 followed by TEST-01.

## User decision

On 2026-01-12 at 11:30 Europe/Paris, after both cases passed, the User explicitly accepted `candidate-b` with no deferred debt and authorized closure. Specification Agent recorded `validated`; Development Agent then performed closure.

## Closure evidence

- Accepted candidate: `candidate-b`.
- Merge commit on `main`: `merge`, containing the accepted candidate.
- Closing commit: `closure`, with trailer `Batch-Closure: Batch-101` and the description set to `closed`.
- Recovery publication: the closing records at `closure` were published and verified under `refs/heads/batch-recovery/batch-101` before the delivery tag.
- Delivery tag: `batch-101`, pointing to the tested and accepted `candidate-b`.
- Final publication: `origin/main` verified at `closure` on 2026-01-12 at 11:45 Europe/Paris; the published tag resolves to `candidate-b`. The recovery ref was removed after both checks.
- Delivery point: verified merge and publication. No production deployment is claimed.

This section is shown as a later read of the completed history. The closing commit is resolved through its trailer; it cannot record its own hash inside itself.

Return to the [example reading order](../index.md#a-complete-example).
