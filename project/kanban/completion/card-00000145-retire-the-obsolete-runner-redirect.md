---
type: card
id: "CARD-00000145"
batch: null
specifications: []
---

# CARD-00000145 — Retire the obsolete Runner redirect

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

Kanban validation passes after retiring the final Runner redirect.

## Scope and authorization

The User confirmed the local deletion and had previously requested removal of obsolete historical redirects. CARD-128 remains ineligible until SPEC-012 r2 is approved.

Remove the obsolete Runner redirect already deleted locally. Preserve completed Cards and recognize only their exact historical Runner links, using the policy introduced by CARD-142.

## Acceptance criteria

- [x] Runner redirect removed and both historical references accounted for.
- [x] Kanban validation passes and active link checks stay strict.


## Execution and evidence

- State: Complete
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker: None.
- Evidence: Kanban validation, 36 Kanban tests and diff review passed in Development. The exceptions match only the two completed Card paths and the retired href.

## History

- 2026-11-15T13:06:50+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T13:07:31+01:00 — Stage moved from `development` to `completion`.
