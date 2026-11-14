---
type: card
id: "TASK-00000094"
batch: null
specifications: []
---

# TASK-00000094 — Make the Batch guard follow the configured workflow

- Owner: Development Agent
- Dependencies:
- Priority: Taken before TASK-00000093 at the User's request; real defect, no dependency, no pending decision.

## Expected outcome

Make `agents/tools/guard-batch-work.py` generic: read the active stage from `project/kanban/workflow.json` instead of the hard-coded `project/kanban/development`, and move the KRR-specific `build-app.sh` full-build rule out of the tool. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [x] The guard works with a workflow whose active stage is not `development`.
- [x] The full-build rule stays available for KRR through the Batch record (list of strengthened-check files, empty by default) and is not imposed on other projects.
- [x] Tests for both cases are added to `agents/tools/test-kanban-board.py` and pass.
- [x] No change to the meaning of any role or Batch rule.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T10:38:45+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T10:40:03+01:00 — Stage moved from `development` to `completion`.
