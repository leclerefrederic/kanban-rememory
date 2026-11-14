---
type: card
id: "TASK-00000099"
batch: null
specifications: []
---

# TASK-00000099 — Clean up duplicated principles and legacy references

- Owner: Development Agent
- Dependencies:

## Expected outcome

Cleanup: one source of truth for the lean principles (README, manifesto, agent rules) with a check that detects drift; set an abandonment date for about 55 legacy references (`Lot`, `UAT.md`, `lots/`) without rewriting approved history; replace `codex/batch-001` examples with `<agent>/batch-001`. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] A single principles source exists and a check fails when the copies diverge.
- [ ] The User approves the abandonment date; legacy references are removed or dated accordingly, approved history unchanged.
- [ ] No `codex/batch-` example remains in `agents` and `documentation`.
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
