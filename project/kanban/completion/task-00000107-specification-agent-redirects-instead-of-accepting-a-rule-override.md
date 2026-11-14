---
type: card
id: "TASK-00000107"
batch: null
specifications: []
---

# TASK-00000107 — Specification Agent redirects instead of accepting a rule override

- Owner: Development Agent
- Dependencies:

## Expected outcome

The Specification Agent cannot write the Rememory journal, so it cannot record an exception and must not accept one. When the User asks it to act against a rule, it names the rule and tells the User to continue in a new session, or an existing one, with the agent whose role allows the action. This corrects the choice of TASK-00000106, which gave the Specification Agent a narrow journal access; that closed Card keeps its text, and the journal records the change. The Development Agent keeps the confirm-and-record rule. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] The shared instructions say that an agent without journal write access does not accept an override and redirects the User to a session with the right agent.
- [x] The Specification Agent role no longer has journal write access and lists accepting an override as forbidden.
- [x] The reader documentation matches.
- [x] Board validation and adoption tests pass; the installed skill copies still match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:08:56+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:09:24+01:00 — Stage moved from `development` to `completion`.
