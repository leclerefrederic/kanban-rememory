---
type: card
id: "TASK-00000115"
batch: null
specifications: []
---

# TASK-00000115 — Compare the required resources in verify-approval

- Owner: Development Agent
- Dependencies:

## Expected outcome

`verify-approval` also checks the required resources of each pinned Specification against the approval snapshot. A second ChatGPT review of 2026-11-14 replaced a binding mockup and the check still passed; reading the code confirmed that only the Batch description and the Specification files were compared. The check now reads the relative links of each approved Specification's "Resources" section, compares every linked repository file with its bytes in the approval commit, accepts the archived copy of a file moved from `resources/active/` to `resources/archived/`, and fails when a linked file is missing from the snapshot or differs. Links to external addresses and anchors are ignored. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] `verify-approval` fails with "Approval mismatch" when a linked required resource differs from the approval snapshot or is absent from it.
- [x] It still passes when the resource is unchanged, and when it was moved to `resources/archived/` with the same bytes.
- [x] External links and anchors in the Resources section are ignored.
- [x] The Batches closed so far still verify against their recorded approval commits, or the exceptions are listed in the journal.
- [x] Tests cover each case and fail against the previous tool; the documentation says the command compares resources.
- [x] Board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:43:55+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:45:07+01:00 — Stage moved from `development` to `completion`.
