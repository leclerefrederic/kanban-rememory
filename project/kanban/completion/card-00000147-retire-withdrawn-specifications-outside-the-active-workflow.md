---
type: card
id: "CARD-00000147"
batch: null
specifications: []
---

# CARD-00000147 — Retire withdrawn specifications outside the active workflow

- Owner: KR Developer
- Dependencies:

## Expected outcome

Withdrawn proposals remain traceable without appearing in active Batch selection.

## Scope and authorization

The User requested a retired folder after reviewing the obsolete and consolidated proposals.

Add project/specs/retired/ for withdrawn, obsolete or consolidated proposals. Preserve existing approved revisions and Batch rejection semantics. Move SPEC-014 and SPEC-020 there with reasons and completed Card references.

## Acceptance criteria

- [x] Retired drafts are retained with a reason and excluded from active selection.
- [x] Adoption and lifecycle documentation describe the directory.
- [x] Board validation and relevant checks pass.


## Execution and evidence

- State: complete
- Actual start:
- Actual finish: 2026-11-15
- Blocker: none

[Journal](../../rememory/2026-11-15.md)

## History

- Reviewed the scoped diff and checks in Development. All 37 board tests passed, including rejection of a retired revision in a draft Batch selection. The board validated and both retired revisions match their previous Git blobs byte for byte. No blockers; WIP is clear at closure.

- 2026-11-15T13:29:26+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T13:30:42+01:00 — Stage moved from `development` to `completion`.
