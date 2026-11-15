---
type: card
id: "CARD-00000157"
scope: "memory"
batch: null
specifications: []
---

# CARD-00000157 — Centralize project and module journals

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

Keep all Rememory journals under `project/rememory/`. The project journal lives in `project/rememory/project/` and each module journal in `project/rememory/modules/<module-id>/`.

## Scope and authorization

- Align journal routing, resumption, milestone writes and setup with the new paths. A simple install creates the project journal directory. A modular install also creates a journal directory for each declared module. The Kanban and module Specification and Batch locations stay as configured.
- Keep one global milestone per verified publication. Module notes hold useful rationale and resumption context. Retrying a write must preserve a single entry.
- Preview the migration of existing journals and their internal and incoming links. Preserve dates, ownership, entries and evidence. Resolve collisions before moving. Update mutable references where needed and keep frozen references resolvable without changing frozen records. Verify recovery and repeated migration before applying the plan.
- On 2026-11-15 the User authorized development, migration preserving links and the completion Telegram through Remy.

## Acceptance criteria

- [x] Simple and modular installation previews show the new journal paths. Approved setup creates the expected directories.
- [x] Project and module notes, post-publication milestones, status and resume operations resolve the correct journal. Replaying a milestone creates no duplicate.
- [x] In a fixture with dated project and module journals, migrate after preview and verify contents, existing links and frozen historical references. A collision stops before writes. A repeat preserves the entries and layout.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:
- Verified revision: `b89e02580189fbd6a7b19cacfdb231a6246150eb`. Reviewed diff and previewed, applied and repeated the migration in the dedicated worktree. Eleven module delivery tests, three focused migration tests and the scoped journal role test passed. Board validation and skill synchronization passed.
- Five dated journals moved and eight module journal locations created. A minimal forward link preserves the original address referenced by two closed Cards. The routed project journal is the only destination for new project milestones.
- [Project journal](../../rememory/project/2026-11-15.md).

## History

- 2026-11-15T17:49:53+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T17:50:20+01:00 — Stage moved from `development` to `completion`.
