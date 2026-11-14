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

Cleanup in two parts, with no change to the meaning of a rule. (1) One source of truth for the lean principles: the principles appear in the README section "The guiding principles", in the manifesto `documentation/lean-specifications.md` and in the agent rules `agents/lean-specifications.md`; keep one and derive the others, with a check that fails when they diverge. (2) The branch example `codex/batch-001` appears in four places, as `codex/batch-001` or `codex/batch-101` (`agents/roles/development-agent.md`, `agents/batches/delivery-example.md`, `agents/batches/start-and-close-batches.md`, `documentation/examples/batch-report.md`); replace it with the neutral `<agent>/batch-001`. The legacy references (`Lot`, `UAT.md`, `lots/`) are kept: the board tools still read historical records, and the User decided on 2026-11-14 not to set an abandonment date or remove that support. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [x] The manifesto is the single authority for the six principles. The agent rules repeat its six headings, the README summarises them and links to it, and a test fails when the headings or the README structure diverge. The wording of each principle is still compared by a human.
- [x] No `codex/batch-` example remains in `agents`, `documentation` and the README.
- [x] The installed skill copies still match `agents/skills/` (`python3 agents/tools/sync-skills.py --check`).
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14 — Refreshed under TASK-00000104 after TASK-00000092 to 103; see the Rememory entry of that day for what changed.
- 2026-11-14 — The legacy-reference part was removed at the User's request: the tool support for the old format stays and no abandonment date is needed. See the Rememory entry of that day.

- 2026-11-14T20:56:36+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:57:40+01:00 — Stage moved from `development` to `completion`.
