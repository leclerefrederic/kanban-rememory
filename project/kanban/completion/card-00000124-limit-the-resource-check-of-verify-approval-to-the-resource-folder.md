---
type: card
id: "CARD-00000124"
batch: null
specifications: []
---

# CARD-00000124 — Limit the resource check of verify-approval to the resource folder

- Owner: Development Agent
- Dependencies:

## Expected outcome

`verify-approval` compares only the files under `project/specs/resources/` that an approved Specification links in its Resources section, not every linked repository file. CARD-00000115 compared every linked file, and on Batch-008 it rejected SPEC-012, which links the two role files, which that Batch changes, and the dated journal, as references to living documents. The User chose on 2026-11-14 to limit the check to the resource folder, where binding attachments such as mockups live. A binding file linked from elsewhere in the repository is no longer checked unless it is moved into that folder; the documentation says so. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] `verify-approval` still fails when a linked file under `project/specs/resources/` differs from the snapshot or is absent from it, and still accepts its archived copy.
- [x] A linked file outside `project/specs/resources/` can change without failing the check.
- [x] `verify-approval Batch-008` passes against the recorded approval commit.
- [x] The documentation states the limit; tests cover both cases; board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:28:42+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:29:20+01:00 — Stage moved from `development` to `completion`.
