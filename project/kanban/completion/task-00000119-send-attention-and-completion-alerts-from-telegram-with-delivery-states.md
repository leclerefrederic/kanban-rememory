---
type: card
id: "TASK-00000119"
batch: "Batch-008"
specifications: ["SPEC-011"]
---

# TASK-00000119 — Send attention and completion alerts from Telegram with delivery states

- Owner: Development Agent
- Dependencies:

## Expected outcome

`agents/tools/notify-telegram.py` sends the two alerts of SPEC-011: **Intervention needed** (`attention`) and **Task completed** (`completed`). Each alert carries the project, the task, what is waiting or the verified result, the chat title and, when available, a link. One alert is confirmed per intervention request or completed task, identified by a stable ID, in a new ledger table. The existing `delivered` and `blocked` events become attention alerts and `closed` becomes a completion alert, with keys that make a Batch delivery and a later completion notifiable once each and never twice. A send that Telegram refuses definitely may be retried. A send whose outcome is unknown is recorded as unconfirmed and is not resent until `--confirm-retry` is given after the destination was checked. The tool reports the notification state in plain lines. It adds no scheduler, reminder, reply handling or approval. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] `attention` and `completed` require a task, a stable ID, a text and a chat name; an optional link and an optional localized label are accepted.
- [x] `delivered`, `blocked` and `closed` keep working and produce the same alerts through the same code path; a Batch delivery produces one alert only.
- [x] A confirmed alert is not sent again; distinct requests, tasks, projects and new candidates are independent.
- [x] A definite failure can be retried; an unknown outcome is recorded as unconfirmed and blocks a blind resend until `--confirm-retry`.
- [x] The tool prints the notification state, never claims delivery that was not confirmed, and sends nothing when the event is disabled or the configuration is missing.
- [x] Tests cover each case; board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:10:41+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:12:28+01:00 — Stage moved from `development` to `completion`.
