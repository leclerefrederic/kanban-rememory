---
type: card
id: "TASK-00000129"
batch: null
specifications: []
---

# TASK-00000129 — Signal when Claude Code waits for the user

- Owner: Development Agent
- Dependencies:

## Expected outcome

Implements the signal part of [SPEC-015](../../specs/approved/spec-015-r1.md). A small command, `agents/tools/krr-signal.py`, lets an agent in a session started by KR say explicitly that it waits for the user (`waiting --id ID`) or that work resumed (`resumed`). It appends one JSON line to `signals.jsonl` in the directory named by `KRR_SESSION_DIR`, which KR reads. Silence or a slow command writes nothing. Shared core: any agent that can run a command can use it; the launch instructions that tell Claude Code when to call it come with TASK-00000130.

## Acceptance criteria

- [x] `waiting` requires a stable `--id` and appends `{event, id, time}`; `resumed` appends `{event, time}`; repeating the same call appends a line each time and never fails.
- [x] Outside a KR session (no `KRR_SESSION_DIR`, or a missing directory) the command refuses with a clear message and writes nothing.
- [x] An invalid ID is refused.
- [x] Automated tests cover these cases and run with the other Python tests.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-14T23:16:22+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T23:16:38+01:00 — Stage moved from `development` to `completion`.
