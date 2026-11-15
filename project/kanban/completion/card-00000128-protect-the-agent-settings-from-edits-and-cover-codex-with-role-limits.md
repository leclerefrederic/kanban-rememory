---
type: card
id: "CARD-00000128"
batch: null
specifications: ["SPEC-012"]
---

# CARD-00000128 — Protect the agent settings from edits and cover Codex with role limits

- Owner: Development Agent
- Dependencies:

## Expected outcome

Two gaps left by Batch-008 (SPEC-012 revision 1), recorded on [CARD-00000095](../completion/card-00000095-design-how-role-limits-know-the-active-role.md) and [CARD-00000096](../completion/card-00000096-enforce-role-limits-with-hooks-for-each-llm.md): the role-limit check does not guard its own configuration (`.claude/settings.json`, `.codex/`), which an agent can edit unless a hook, a deny rule or managed settings prevents it, and Codex stays advisory because its hook input carries no agent identity. This Card tracks the work only. It needs a new Specification revision written by the Specification Agent and approved by the User before any implementation; the Development Agent does not edit `project/specs/`. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule.

## Acceptance criteria

- [x] A Specification revision covering protection of the agent settings and, once a per-session role declaration is tested, a Codex check, is written, approved by the User and verified in Git.
- [x] Unconfirmed facts of SPEC-012 (hooks in the desktop apps, the Codex hook environment, Codex hooks for sub-agents) are tested or stay labelled unconfirmed.
- [x] After approval, implement only what that Specification requires; adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker: none

[Technical evidence](../../rememory/evidence/card-00000128-role-protection.md). Reviewed the scoped diff in Development. The approved Specification's staged SHA-256 matched the approval. Claude Code 2.1.323 on macOS refused synthetic writes/deletions on the protected surfaces while allowing an ordinary project write. Codex CLI 0.169.0 stays advisory because no trusted per-call role binding qualified. Desktop and subagent runtime surfaces remain unconfirmed. Board validation, 37 Kanban tests, skill consistency and 14 role migration tests in a clean archive passed.

## History

- 2026-11-15 — KR Writer submitted [SPEC-012 r2](../../specs/approved/spec-012-r2.md) for scope review.
- 2026-11-15 — User replied “vas y.” after review of SPEC-012 revision 2, approving that scope and authorizing CARD-128 development.

- 2026-11-15T13:16:03+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T13:21:42+01:00 — Stage moved from `development` to `completion`.
