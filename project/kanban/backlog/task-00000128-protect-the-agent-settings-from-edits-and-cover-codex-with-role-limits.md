---
type: card
id: "TASK-00000128"
batch: null
specifications: []
---

# TASK-00000128 — Protect the agent settings from edits and cover Codex with role limits

- Owner: Development Agent
- Dependencies:

## Expected outcome

Two gaps left by Batch-008 (SPEC-012 revision 1), recorded on [TASK-00000095](../completion/task-00000095-design-how-role-limits-know-the-active-role.md) and [TASK-00000096](../completion/task-00000096-enforce-role-limits-with-hooks-for-each-llm.md): the role-limit check does not guard its own configuration (`.claude/settings.json`, `.codex/`), which an agent can edit unless a hook, a deny rule or managed settings prevents it, and Codex stays advisory because its hook input carries no agent identity. This Card tracks the work only. It needs a new Specification revision written by the Specification Agent and approved by the User before any implementation; the Development Agent does not edit `project/specs/`. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule.

## Acceptance criteria

- [ ] A Specification revision covering protection of the agent settings and, once a per-session role declaration is tested, a Codex check, is written, approved by the User and verified in Git.
- [ ] Unconfirmed facts of SPEC-012 (hooks in the desktop apps, the Codex hook environment, Codex hooks for sub-agents) are tested or stay labelled unconfirmed.
- [ ] After approval, implement only what that Specification requires; adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
