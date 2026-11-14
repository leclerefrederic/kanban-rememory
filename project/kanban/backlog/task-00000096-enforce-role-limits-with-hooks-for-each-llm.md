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

Implement what the approved role-limits Specification (SPEC-012, Batch-008) requires, and nothing else: a role-limit check built from the role file headers in `agents/roles/*.md` and the optional Claude Code hook that calls it. Codex stays advisory in SPEC-012; a Codex branch needs a later Specification revision. The automatic check before `git push` already exists ([TASK-00000101](../completion/task-00000101-run-the-batch-checks-automatically-before-pushing-to-main.md)) and must not be duplicated. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] A write or a read forbidden for the active role is refused with an explicit message; an allowed write or read passes.
- [ ] The behavior is tested without relying on the model's cooperation, for the shared check and the Claude hook, in `agents/tools/test-kanban-board.py`.
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
- 2026-11-14 — Rewritten from SPEC-012: Claude Code hook only, Codex advisory. Delivered on `claude/batch-008` (tested commit `843b4b3d0da50a0ce67f99024a1487b13eaffd57`) as TASK-00000115 and related Cards; close this Card after Batch-008 is accepted and merged.
