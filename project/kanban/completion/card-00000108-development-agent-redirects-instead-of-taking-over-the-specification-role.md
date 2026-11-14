---
type: card
id: "CARD-00000108"
batch: null
specifications: []
---

# CARD-00000108 — Development Agent redirects instead of taking over the Specification role

- Owner: Development Agent
- Dependencies:

## Expected outcome

Neither agent takes over the other role's work, even on the User's instruction. When an instruction would put an agent outside its role, it names the rule and tells the User to continue in a new session, or in an existing one, with the agent whose role allows the action. This extends CARD-00000107 from the Specification Agent to the Development Agent. The confirm-and-record rule of CARD-00000106 remains only for a rule that is not a role limit, and only for an agent that can write the journal. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] The shared instructions say that no agent acts outside its role on an instruction, and that it redirects the User to the right agent.
- [x] The confirm-and-record rule applies only to a rule that is not a role limit, for an agent that can write the journal.
- [x] The Development Agent role lists taking over the Specification role as forbidden.
- [x] The reader documentation matches.
- [x] Board validation and adoption tests pass; the installed skill copies still match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:11:37+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:12:04+01:00 — Stage moved from `development` to `completion`.
