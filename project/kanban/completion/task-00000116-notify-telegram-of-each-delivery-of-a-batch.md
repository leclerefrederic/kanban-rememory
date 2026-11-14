---
type: card
id: "TASK-00000116"
batch: null
specifications: []
---

# TASK-00000116 — Notify Telegram of each delivery of a Batch

- Owner: Development Agent
- Dependencies:

## Expected outcome

A corrected Batch notifies the User again when its new candidate is ready. A second ChatGPT review of 2026-11-14 reported, and reading the code confirmed, that the Telegram receipt key was `(chat, batch, event, blocker)`, empty for `delivered`, so the second delivery of a Batch was skipped as a duplicate. The `delivered` event now requires `--revision`, the full tested commit, and that revision is part of the receipt key and of the message. Retries of the same delivery are still skipped. `blocked` and `closed` keep their keys. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] `notify-telegram.py delivered` requires `--revision` with a full commit ID and rejects it on other events.
- [x] Two deliveries of one Batch with different revisions each send; a retry with the same revision is skipped.
- [x] The message shows the short revision.
- [x] `agents/configure-telegram.md` shows the new call.
- [x] Tests cover the three cases and fail against the previous tool.
- [x] Board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:46:00+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:47:00+01:00 — Stage moved from `development` to `completion`.
