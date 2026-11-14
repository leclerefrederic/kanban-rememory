---
type: card
id: "TASK-00000093"
batch: null
specifications: []
---

# TASK-00000093 — Move the daily template into the kit templates

- Owner: Development Agent
- Dependencies:

## Expected outcome

Move `project/rememory/daily-template.md` into `agents/templates/` so copying `agents/` and `documentation/` gives a self-contained kit. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [x] The template lives in `agents/templates/` and `project/rememory/` no longer holds it.
- [x] References updated in `agents/templates/project-layout.md`, `agents/install-in-a-project.md`, `agents/maintain-rememory.md` and `INSTALL_FILES` in `agents/tools/test-kanban-board.py`.
- [x] The User confirmed where the template lands in a target project.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T10:46:05+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T10:47:07+01:00 — Stage moved from `development` to `completion`.
