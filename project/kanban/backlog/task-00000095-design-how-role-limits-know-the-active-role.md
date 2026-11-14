---
type: card
id: "TASK-00000095"
batch: null
specifications: []
---

# TASK-00000095 — Design how role limits know the active role

- Owner: Development Agent
- Dependencies:

## Expected outcome

Design, without implementing, how enforcement of role limits learns the active role, for Claude Code and Codex alike. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] Options compared (environment variable at launch, restricted sub-agents, state file in the repository) with a recommendation the User approves.
- [ ] Claude Code and Codex hook, sandbox and approval behavior read in the official documentation, not search summaries; Codex hooks must not rely on an `ask` answer.
- [ ] The design separates the shared check (one script both can call) from each LLM's hook wiring.
- [ ] Output is a written design in the Card or a Specification; no implementation.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
