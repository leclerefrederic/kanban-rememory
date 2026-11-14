---
type: card
id: "TASK-00000123"
batch: "Batch-008"
specifications: ["SPEC-012"]
---

# TASK-00000123 — Document the Claude Code role check and its limits

- Owner: Development Agent
- Dependencies:

## Expected outcome

No page contradicts the delivered role check, and the User can tell which tool, role and action is protected. The page that marked role hooks as planned says what exists. An agent procedure explains how to install, use and remove the Claude Code check. The reader and agent pages list, for Claude Code and for Codex, what the check does and does not cover, and label each fact that was not tested as unconfirmed. Projects without the check, sessions without a declared role, Codex, and the chat applications are never described as protected. Shared core: only the Claude branch changes.

## Acceptance criteria

- [x] `documentation/use-with-chatgpt-and-claude.md` describes the delivered Claude check and marks Codex and the chat applications advisory; no page says role hooks are planned.
- [x] A new agent page `agents/configure-claude-role-hook.md` covers installation, starting a session as a role, removal, and the limits; it is linked from `agents/index.md` and the install procedure.
- [x] The limits name what is not covered and each unconfirmed fact is labelled as such.
- [x] A test fails if a page says role hooks are planned.
- [x] Board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:23:02+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:24:23+01:00 — Stage moved from `development` to `completion`.
