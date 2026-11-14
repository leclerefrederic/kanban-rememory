---
type: specification
id: "SPEC-101"
revision: "1"
---

# Preserve booking names in CSV exports

> Fictional example, written by Specification Agent. In the example project, this approved revision lives at `project/specs/approved/spec-101-r1.md`. It describes the agreed behavior; the tests and report record what was actually delivered.

## Expected outcome

Booking staff can export customer names containing accents or commas without repairing the exported data. Success means both sample names survive export exactly and remain in one CSV field.

## Scope

Correct name encoding and quoting in the existing CSV export. Keep the existing export action, column order and fields. No new export format or configuration is needed.

## Acceptance criteria

- **AC-01 — Accents:** given a booking named `Élodie`, export it and read the CSV as UTF-8. The name is exactly `Élodie`.
- **AC-02 — Commas:** given a booking named `Smith, Alex`, export it and read the CSV. The complete name occupies one field, and the following fields retain their original values and positions.

## Resources

None required. The two sample names above are sufficient test data; no real customer data is needed.

This approved revision stays unchanged during correction. Restoring either criterion does not add scope.

Return to the [example reading order](../index.md#a-complete-example).
