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

- [ ] The template lives in `agents/templates/` and `project/rememory/` no longer holds it.
- [ ] References updated in `agents/templates/project-layout.md`, `agents/install-in-a-project.md`, `agents/maintain-rememory.md` and `INSTALL_FILES` in `agents/tools/test-kanban-board.py`.
- [ ] The User confirmed where the template lands in a target project.
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
