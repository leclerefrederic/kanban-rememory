---
type: card
id: "TASK-00000096"
batch: null
specifications: []
---

# TASK-00000096 — Enforce role limits with hooks for each LLM

- Owner: Development Agent
- Dependencies: TASK-00000095

## Expected outcome

Implement what the approved role-limits Specification requires, and nothing else: a shared role-limit check built from the Write access and Forbidden sections of `agents/roles/*.md`, and the optional Claude Code and Codex hook branches that call it. The automatic check before `git push` already exists ([TASK-00000101](../completion/task-00000101-run-the-batch-checks-automatically-before-pushing-to-main.md)) and must not be duplicated. If the approved Specification differs from this text, rewrite this Card from the Specification before starting. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] A write forbidden for the active role is refused with an explicit message; an allowed write passes.
- [ ] The behavior is tested without relying on the model's cooperation, for the shared check and each hook branch, in `agents/tools/test-kanban-board.py`.
- [ ] The kit works without either branch installed, and installing a branch is one documented command.
- [ ] The hook files are part of the kit's package lists and `agents/templates/project-layout.md`.
- [ ] `documentation/use-with-chatgpt-and-claude.md` no longer marks role hooks as planned and states what was delivered; the install procedure, the agent index and the roles are consistent with it.
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-14 — Refreshed under TASK-00000104 after TASK-00000092 to 103; see the Rememory entry of that day for what changed.
