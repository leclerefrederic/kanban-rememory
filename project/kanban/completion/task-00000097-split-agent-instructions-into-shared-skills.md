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

Reduce initial reading load with three `SKILL.md` entry points (standalone work, Specification Agent, Development Agent) that route to the existing instructions. The User chose this routing approach over moving rules into the skills: no rule is moved or duplicated, so its meaning cannot change. One skill text serves ChatGPT/Codex and Claude; copying it into `.claude/skills/` and `.agents/skills/` belongs to [TASK-00000098](../backlog/task-00000098-distribute-the-kit-and-skills-to-claude-code-and-codex.md).

## Acceptance criteria

- [x] Initial reading load is measured before and after, counting the words of the documents an agent must read at the start of a session for each work mode.
- [x] The skills restate no rule and every path they name exists; a test checks both the format and the paths.
- [x] A fresh session reading only its skill identifies its role, the Batch state and the next authorized action.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T11:29:42+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T11:31:19+01:00 — Stage moved from `development` to `completion`.
