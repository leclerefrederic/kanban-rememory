---
type: card
id: "TASK-00000127"
batch: null
specifications: []
---

# TASK-00000127 — Notify a different request that reuses a confirmed Telegram alert ID

- Owner: Development Agent
- Dependencies:

## Expected outcome

Corrects Batch-008-DEBT-01 within SPEC-011 ("Avoid duplicate alerts"), as requested in the Correction request of the Batch-008 report. The Telegram receipt key used chat, project, kind and an ID the agent chooses, so a different request that reused a confirmed ID was skipped as a duplicate. For `attention` and `completed` alerts the key now also covers the task and the text of the request; a Batch ID still names one outcome, so a closure and a completion of the same Batch stay one alert. A resend of the same alert, or the same work resumed in another chat, stays ignored. No feature is added. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] A different request, text or task that reuses a confirmed ID in the same project is sent.
- [x] A resend of the same alert, including from another chat title or link, is reported as a duplicate.
- [x] A Batch closure and a completion of the same Batch remain one alert; delivered and blocked alerts keep their keys.
- [x] Tests cover these cases; board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T22:52:00+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T22:52:13+01:00 — Stage moved from `development` to `completion`.
