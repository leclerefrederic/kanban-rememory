---
type: card
id: "TASK-00000082"
batch: null
specifications: []
---

# TASK-00000082 — Separate reader guides from agent operating instructions

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User request after restoring the README's voice.

## Expected outcome

Give human readers a dedicated `docs/guides/` collection explaining the framework, rules and processes in plain English. Keep executable agent instructions under `docs/agents/` and record templates under `docs/templates/`. The README remains the playful introduction and routes readers to the human guides.

Scope: documentation structure, reader guides, live navigation and installation references, plus adoption checks affected by relocation. Keep approved historical records unchanged; retain minimal link redirects only where those records need an old documentation path. Do not duplicate procedural content or change product behavior.

## Acceptance criteria

- [x] Provide readable guides for framework concepts, adoption and responsibilities, delivery, acceptance and debt; keep commands and agent instructions out of those guides.
- [x] Group operating procedures under `docs/agents/`, preserve templates separately, and give both audiences distinct navigation.
- [x] Keep the approved manifesto intact, update live links and installation paths, and preserve historical references without editing immutable records.
- [x] Verify links, anchors, fresh core and Batch-module adoption, and the documentation diff before closure.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `15c1b4a`. Added the [human guide index](../../../documentation/index.md) and plain-language explanations of the framework, project adoption, delivery, acceptance/debt and Runner. The approved manifesto moved into this collection byte for byte.
- Moved ten existing documents to their appropriate reader or agent location. [Agent instructions](../../../agents/index.md) and the [documentation index](../../../README.md#pick-your-next-move) distinguish audiences; templates remain separate. Updated live paths, installation instructions and the test install package. README navigation uses the human guides and retains its playful voice.
- Seven old documentation paths contain only redirects needed by immutable historical records, including their referenced anchors. No closed Card, approved Specification, Batch record or old journal entry was rewritten.
- `python3 tools/test-kanban-board.py`: all 15 tests passed, including fresh core and Batch-module installation with the relocated references. `python3 tools/manage-kanban-board.py validate` and `git diff --check` passed.
- Reviewed the documentation and installation diff. Verified that all 31 maintained documents are reachable via the separate indexes, and that human guides contain no operational command blocks or links into agent/template instructions. No application code or product behavior changed.
- Flow review: this was the only active Card; all Batches are closed and no blocker remains. Next action: publish the closed Card and verified documentation under standing authorization.

## History

- 2026-11-14 — User requested human-readable guides and explicitly required separating them from the instructions used by agents to operate Kanban Rememory. TASK-00000081 is published; no Batch or other Card is active.

- 2026-11-14T01:30:10+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:34:47+01:00 — Stage moved from `development` to `completion`.
