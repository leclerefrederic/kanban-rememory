---
type: tests
id: "Batch-101-Tests"
batch: "Batch-101"
---

# Booking export acceptance tests

> Fictional example of `project/batches/batch-101/tests.md`, including illustrative results. Booking Desk, the builds and revision labels below are teaching examples, not applications or evidence supplied by this repository. In real records, each candidate label is replaced by its full Git commit ID and actual build location.

- Tested commit: `candidate-b`, with the earlier `candidate-a` results retained below.
- Environment or prerequisites: macOS; local Booking Desk demo workspace containing bookings `Élodie` and `Smith, Alex`. No login or network connection is required in this example.
- Technical evidence: `candidate-a` passed an automated accents check; `candidate-b` passed both accents and comma-field regression checks.
- Scope: [SPEC-101 revision 1](project-specification.md), selected by [Batch-101](batch-description.md).

| Candidate | Preserved build location in the example project |
| --- | --- |
| `candidate-a` | `/tmp/booking-demo/candidate-a/Booking Desk.app` |
| `candidate-b` | `/tmp/booking-demo/candidate-b/Booking Desk.app` |

## Results by attempt

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | SPEC-101 / AC-01 | Export Élodie and inspect the CSV. | Name preserved exactly. | OK | `candidate-a` | User reads Élodie unchanged. |
| TEST-02 | SPEC-101 / AC-02 | Export Smith, Alex and inspect the fields. | Complete name in one field; following fields unchanged. | KO | `candidate-a` | Name splits into two fields and shifts later values. Screenshot requested; unavailable. Debt: Batch-101-DEBT-01. |
| TEST-02 | SPEC-101 / AC-02 | Repeat the failed comma case after correction. | Complete name in one field; following fields unchanged. | OK | `candidate-b` | User confirms one complete name field and the original later values. |
| TEST-01 | SPEC-101 / AC-01 | Repeat the accents case because the export writer changed. | Name preserved exactly. | OK | `candidate-b` | User confirms Élodie remains unchanged. |

The failure and [correction decision](batch-report.md#correction-request) remain visible. An earlier OK is not silently attributed to a later revision.

## Startup and actions by case

The following is the final attempt on `candidate-b`. For the first attempt, the agent supplied the `candidate-a` build path with the same fixture and actions. Every presented question includes its startup instructions and OK / KO choices.

### TEST-02 — Keep a comma inside one field

**Start:** Quit other Booking Desk instances. In Finder, open `/tmp/booking-demo/candidate-b/Booking Desk.app`. Select the local demo workspace and the booking `Smith, Alex`. Open the existing CSV preview; no session or connection is needed.

**Do:** Use the existing export action, then load that file in the preview as UTF-8 CSV with a comma delimiter. Inspect the name and the following columns.

**Expect:** `Smith, Alex` occupies one field. Following values keep their original positions. Stop before editing the exported data.

**Choice:** OK / KO. Example User answer: **OK**.

### TEST-01 — Preserve accents

**Start:** Quit other Booking Desk instances. In Finder, open `/tmp/booking-demo/candidate-b/Booking Desk.app`. Select the local demo workspace and the booking `Élodie`. Open the existing CSV preview; no session or connection is needed.

**Do:** Use the existing export action, then load that file in the preview as UTF-8 CSV with a comma delimiter. Read the name.

**Expect:** The name is exactly `Élodie`. Stop before editing the exported data.

**Choice:** OK / KO. Example User answer: **OK**.

After each verdict, the agent presents the next case. A KO first prompts an explanation and screenshot request; the agent records unavailable evidence explicitly. Here, both required cases have passed on the corrected revision, so none remains outstanding.

Return to the [example reading order](../index.md#a-complete-example).
