---
type: card
id: "TASK-00000120"
batch: "Batch-008"
specifications: ["SPEC-011"]
---

# TASK-00000120 — Tell the Development Agent when to alert the User

- Owner: Development Agent
- Dependencies:

## Expected outcome

The Development Agent knows when to send the two Telegram alerts of SPEC-011, for work with or without a Batch: Intervention needed at the moment it needs the User, and Task completed only when the requested outcome is verified, nothing in between. The rules live in the Development Agent role. The skills route to them, the Telegram page says how to send, and the reader documentation tells the User what to expect. The chat stays authoritative: an alert authorizes nothing and a Telegram reply is not an instruction. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] The role file states when to alert, when not to, how to word and identify the alert, how to report the notification state in the chat, and that the chat remains authoritative.
- [x] The Batch delivery and closure rules say which event to use so that one outcome never produces two alerts.
- [x] The standalone skill routes to these rules; skill copies match the kit.
- [x] The reader documentation describes the alerts and their limits.
- [x] Board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:13:30+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:14:10+01:00 — Stage moved from `development` to `completion`.
