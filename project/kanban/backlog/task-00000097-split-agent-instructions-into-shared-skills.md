---
type: card
id: "TASK-00000097"
batch: null
specifications: []
---

# TASK-00000097 — Split agent instructions into shared skills

- Owner: Development Agent
- Dependencies: TASK-00000092

## Expected outcome

Reduce initial reading load: short `AGENTS.md` plus three `SKILL.md` skills (standalone work, Specification Agent, Development Agent) with Batch procedures as on-demand reference files, using one skill text for both LLMs. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] Initial reading load measured before and after (baseline: Development Agent 8,446 words, Specification Agent 6,227, standalone 4,685).
- [ ] Review shows every existing rule appears exactly once and no rule's meaning changed.
- [ ] A fresh session identifies its role, the Batch state and the next authorized action (test in `agents/install-in-a-project.md`).
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
