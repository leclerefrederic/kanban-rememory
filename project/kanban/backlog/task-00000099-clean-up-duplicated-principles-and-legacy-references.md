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

Cleanup in three parts, with no change to the meaning of a rule. (1) One source of truth for the lean principles: the principles appear in the README section "The guiding principles", in the manifesto `documentation/lean-specifications.md` and in the agent rules `agents/lean-specifications.md`; keep one and derive the others, with a check that fails when they diverge. (2) Legacy references (`Lot`, `UAT.md`, `lots/`): about 52 matches remain, almost all in the board tools (`agents/tools/kanban/batches.py`, 15) and their tests (32) that still read historical records, and only about 4 in agent procedures. Removing the tool support depends on a User decision about an abandonment date; do not rewrite approved history. (3) The branch example `codex/batch-001` appears in four places (`agents/roles/development-agent.md`, `agents/batches/delivery-example.md`, `agents/batches/start-and-close-batches.md`, `documentation/examples/batch-report.md`); replace it with the neutral `<agent>/batch-001`. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [ ] A single principles source exists and a check fails when the other copies diverge.
- [ ] The User approves the abandonment date before any legacy tool support is removed; agent procedures no longer carry legacy wording, and approved history is unchanged.
- [ ] No `codex/batch-` example remains in `agents`, `documentation` and the README.
- [ ] The installed skill copies still match `agents/skills/` (`python3 agents/tools/sync-skills.py --check`).
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-14 — Refreshed under TASK-00000104 after TASK-00000092 to 103; see the Rememory entry of that day for what changed.
