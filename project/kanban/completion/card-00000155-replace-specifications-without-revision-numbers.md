---
type: card
id: "CARD-00000155"
scope: "specifications"
batch: null
specifications: []
---

# CARD-00000155 — Use each Specification in one Batch

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

A Specification has one stable ID and serves one Batch. After that Batch closes, the Specification is retired and remains available as historical evidence.

## Scope and authorization

- The User authorized development in the original Codex conversation on 2026-11-15 by asking to execute Card 155 after clarifying the one-Batch lifecycle.
- Remove revision numbers from new Specification filenames, metadata, templates and new Batch references. Keep an exact approval snapshot of the selected text and resources.
- Apply the lifecycle `draft → ready → approved → retired`. Associate the Specification with its Batch at `ready`. It is `approved` for development and remains with that Batch through testing and any corrections. Retire it at verified Batch closure. A retired Specification cannot be selected again.
- Preserve frozen Specifications, previous Batch records and their revisioned references. Keep legacy history and approval verification readable without rewriting those records.

## Acceptance criteria

- [x] Create and approve a new Specification and pin it in a Batch using its ID without a revision number. Verify that changing its approved text or resources is detected.
- [x] Select a ready Specification for a Batch, approve it and close that Batch. It remains tied to that Batch throughout corrections, is archived as retired on closure and is refused in another Batch. Exercise accepted and rejected closure.
- [x] Open and verify a historical Batch linked to the retired Specification, including a legacy numbered revision. Its recorded reference, archived bytes and approval evidence are intact.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

Verified product commit: `7305de8cef12ebc15368e61526d12c998284ab6b`. Reviewed the diff in Development. Kanban suite passed 47 tests, including single-use pins, legacy snapshots and resource verification. Delivery fixtures passed for simple retirement, accepted and rejected module closure, and interrupted publication recovery. Six publication guard tests passed.

## History

- KR Developer claimed `specifications` from main `e571a01` on `codex/card-00000155` in `/private/tmp/kr-card155` (owner `codex-card-155`).

- 2026-11-15T17:24:37+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T17:31:09+01:00 — Stage moved from `development` to `completion`.
