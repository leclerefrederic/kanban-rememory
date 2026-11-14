---
type: card
id: "TASK-00000094"
batch: null
specifications: []
---

# TASK-00000094 — Make the Batch guard follow the configured workflow

- Owner: Development Agent
- Dependencies:

## Expected outcome

Make `agents/tools/guard-batch-work.py` generic: read the active stage from `project/kanban/workflow.json` instead of the hard-coded `project/kanban/development`, and move the KRR-specific `build-app.sh` full-build rule out of the tool. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] The guard works with a workflow whose active stage is not `development`.
- [ ] The full-build rule stays available for KRR through the Batch record (list of strengthened-check files, empty by default) and is not imposed on other projects.
- [ ] Tests for both cases are added to `agents/tools/test-kanban-board.py` and pass.
- [ ] No change to the meaning of any role or Batch rule.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
