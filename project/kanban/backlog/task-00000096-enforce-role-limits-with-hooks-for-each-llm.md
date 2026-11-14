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

Implement the approved design: a shared role-limit check built from the Write access and Forbidden sections of `agents/roles/*.md`, plus a Claude Code hook branch and a Codex hook branch that call it. The automatic guard call before `git push` moved to [TASK-00000101](task-00000101-run-the-batch-checks-automatically-before-pushing-to-main.md). Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] A write forbidden for the active role is refused with an explicit message; an allowed write passes.
- [ ] The behavior is tested without relying on the model's cooperation, for the shared check and each hook branch.
- [ ] The kit works without either branch installed.
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
