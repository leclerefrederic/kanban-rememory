---
type: card
id: "TASK-00000089"
batch: null
specifications: []
---

# TASK-00000089 — Add connected examples of project delivery records

- Owner: Development Agent
- Dependencies: None.
- Priority: User requested the missing examples after the directory migration.

## Expected outcome

Readers can follow one concrete delivery through five filled examples in `documentation/examples/`: a Specification, Batch description, independent Card, acceptance tests and report. Use one fictional booking-export scenario and make its illustrative status explicit.

Scope: English reader documentation, navigation from the README and guide index, and inclusion in the existing adoption test package. Preserve agent templates and live delivery records. Examples explain linked IDs, approval, verification, correction, final acceptance and closure without claiming real execution or creating a product feature.

## Acceptance criteria

- [x] Provide five concise, filled examples aligned with the existing record formats and shared rules.
- [x] Link the scenario coherently; keep Cards independent of Batch contents and preserve failed attempts alongside corrected results.
- [x] Make all examples discoverable from the README and guide index; distinguish fictional evidence from actual project records.
- [x] Verify links, record mappings and installation tests, then review the diff before closure.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `995742c`.
- Added five filled English examples in `documentation/examples/`, linked from the guide index and README. The fictional scenario preserves accents and commas in booking exports, including a failed attempt, authorized correction, retests and accepted closure.
- Reviewed the examples against the templates, actor responsibilities and closure procedure. Batch records contain no Card IDs or links. Each file explicitly identifies its content as fictional; no demo application, real execution, User verdict or delivery is claimed.
- Verification: all 15 existing adoption tests pass with the examples included in the installed documentation. Repository links and whitespace checks pass. The five records also validate after placement into their canonical locations in an isolated adopted repository, confirming header mappings and one-way Card references. The temporary probe's initial macOS path-normalization issue was corrected before this successful verification; no production code changed.
- Flow review: all existing Batches remain closed; no other active Card or blocker. Unrelated local files remain excluded from publication.

## History

- 2026-11-14 — User requested examples of a Batch, Specification and Card, added Tests and Report, then asked where they were. Implement the complete linked set as reader documentation.

- 2026-11-14T02:03:18+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T02:06:34+01:00 — Stage moved from `development` to `completion`.
