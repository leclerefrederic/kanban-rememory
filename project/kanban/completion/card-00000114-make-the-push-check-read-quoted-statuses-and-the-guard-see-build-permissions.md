---
type: card
id: "CARD-00000114"
batch: null
specifications: []
---

# CARD-00000114 — Make the push check read quoted statuses and the guard see build permissions

- Owner: Development Agent
- Dependencies:

## Expected outcome

Two gaps found by a second ChatGPT review of 2026-11-14 and confirmed by reading the code are closed. (1) The push check read the Batch status with its own pattern, so `status: "closed"` was not recognised as `closed`, although the board accepts quoted values, and a push could skip the publication guard. It now uses the shared front-matter reader. (2) The artifact digest covered names and bytes but not permissions, so a build whose executable bit was removed still counted as intact. The digest now includes the executable bit. A guard record frozen before this change no longer matches and must be frozen again; no Batch is active today. Shared core: the same for ChatGPT/Codex and Claude.

## Acceptance criteria

- [x] `check-batch-publication.py` reads the status with the shared `header_value`, and a quoted `status: "closed"` triggers the guard like the unquoted form.
- [x] The artifact digest includes the executable bit; removing it from a frozen build fails `verify`.
- [x] Tests cover both cases and fail against the previous tools.
- [x] The documentation states that earlier guard records must be frozen again.
- [x] Board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:41:03+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:42:41+01:00 — Stage moved from `development` to `completion`.
