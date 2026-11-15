---
type: card
id: "CARD-00000156"
scope: "memory"
batch: null
specifications: []
---

# CARD-00000156 — Archive old project Rememory subdirectories

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

Keep the project Rememory focused on its dated journal. Move the three historic subdirectories to the local archive.

## Scope and authorization

- Move `project/rememory/{evidence,runner-removal,telegram-setup}` to `Archives/rememory/`, preserving their contents and names. Keep project and module journals in place.
- Before moving evidence still referenced by the project, verify that it remains retrievable. Point affected links in active, mutable records to the retained history when needed. Preserve frozen records and the existing Git ignore rule.
- The User authorized execution on 2026-11-15.

## Acceptance criteria

- [x] The three directories are present under ignored `Archives/rememory/`, with their original content.
- [x] Dated journals still work at project and module level. The active board validates in a clean checkout without the local archive.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

- Verified revision: `649d12bc97c07973ac903b353a75ef0271277285`. Compared bytes for all 20 archived files, reviewed the diff, and validated the board in a clean checkout without the archive during Development. Five historical evidence links in the project journal refer to the published pre-archive revision. [Project Rememory](../../rememory/2026-11-15.md).

## History

- 2026-11-15T17:33:52+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T17:35:24+01:00 — Stage moved from `development` to `completion`.
