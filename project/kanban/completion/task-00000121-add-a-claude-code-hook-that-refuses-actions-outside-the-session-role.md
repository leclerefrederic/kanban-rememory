---
type: card
id: "TASK-00000121"
batch: "Batch-008"
specifications: ["SPEC-012"]
---

# TASK-00000121 — Add a Claude Code hook that refuses actions outside the session role

- Owner: Development Agent
- Dependencies:

## Expected outcome

A `PreToolUse` hook for Claude Code, `agents/tools/role-limit-hook.py`, refuses a read, a write or a Bash command that the role of the session does not allow, and tells the User which agent to continue with. The role comes only from the identity Claude Code gives a session started as a named agent (`agent_type`); a session with no known role is not restricted. The limits are read from the role files, which stay their only definition: each role file gets a machine-readable header holding the same Read and Write lists as its prose, and a test fails when the two diverge. The hook only allows or denies, never offers an override, and never allows what a role forbids. Its blind spots (shell writes it cannot see, paths outside the project, unknown agent names, a failing hook) are documented, not hidden. Shared core: the role files are the same for ChatGPT/Codex and Claude; the hook is an optional Claude Code branch.

## Acceptance criteria

- [x] Each role file has a header with its read and write limits, and a test fails when a path in the header is missing from the prose lists.
- [x] The hook denies a Specification Agent read of `project/kanban/`, a write outside `project/specs/` and `project/batches/`, and Git commands; it denies a Development Agent read of `project/specs/draft/` or `ready/` and any write under `project/specs/`.
- [x] A refusal names the rule and the agent to continue with, offers no override, and changes nothing.
- [x] In-role reads and writes pass, including the Development Agent writing the journal.
- [x] A session with no `agent_type`, or an unknown one, is not restricted; text in files never sets the role.
- [x] Tests cover each case; board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:16:06+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:18:16+01:00 — Stage moved from `development` to `completion`.
