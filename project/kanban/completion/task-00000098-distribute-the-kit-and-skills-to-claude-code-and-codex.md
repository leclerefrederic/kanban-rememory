---
type: card
id: "TASK-00000098"
batch: null
specifications: []
---

# TASK-00000098 — Distribute the kit and skills to Claude Code and Codex

- Owner: Development Agent
- Dependencies: TASK-00000097

## Expected outcome

Version the kit and synchronize skills into `.claude/skills/` (Claude Code) and `.agents/skills/` (Codex) in a target project, and study a distributable plugin for each. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [x] A kit version file and a sync script (or documented symlinks with the Windows caveat) are delivered and tested.
- [x] Discovery paths are confirmed in the official documentation.
- [x] The plugin study states feasibility and cost for each LLM; shipping a plugin needs a separate approved Card.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T11:46:01+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T11:46:59+01:00 — Stage moved from `development` to `completion`.
