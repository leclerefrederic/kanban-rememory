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

The role-limits design is delivered as a Specification, not by this Card. The Specification Agent writes it, the User approves it, and it is verified in Git as an approved revision; this Card tracks that handoff and closes then. The Development Agent does not edit `project/specs/`. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([TASK-00000092](../completion/task-00000092-document-shared-core-and-llm-skill-branches.md)).

Decisions already taken by the User (2026-11-14): protect the transitions (approval, acceptance, publication) rather than the sessions; the automatic push check is delivered ([TASK-00000101](../completion/task-00000101-run-the-batch-checks-automatically-before-pushing-to-main.md)) and not part of this design; Claude and Codex hooks are an optional layer; the Coworker mode stays advisory. Verified findings to hand over: Claude Code can start a session as a named agent (`--agent`) and its hook receives `agent_type`; the Codex hook input has no agent identity, and whether its hook inherits the launching environment is unconfirmed; `.claude/` and `.codex/` must be protected from edits by the agent; ChatGPT, Work and Codex share one project space, so no product boundary separates the roles.

## Acceptance criteria

- [x] The User gave the go-ahead; the findings and decisions are recorded in Rememory for the Specification Agent.
- [x] A Specification covering role limits is written by the Specification Agent, approved by the User and verified in Git: SPEC-012 revision 1 (approval commit `c8430e0ee0e596df29f7996e99a52614848b4b54`, Batch-008).
- [x] The Specification keeps Codex advisory, keeps the Coworker mode advisory and states that the check does not guard its own configuration. Protecting `.claude/` and `.codex/` from agent edits is not in SPEC-012; it needs a new Specification revision if the User wants it.
- [x] Points still unverified (hooks in the desktop apps, the Codex hook environment, Codex hooks for sub-agents) are listed as unconfirmed in SPEC-012.
- [ ] Board validation passes.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-14 — Refreshed under TASK-00000104 after TASK-00000092 to 103; see the Rememory entry of that day for what changed.
- 2026-11-14 — Criteria aligned with SPEC-012 as approved: Codex advisory, `.claude/` and `.codex/` protection left out of scope. Close this Card after Batch-008 is accepted.
