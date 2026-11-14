---
type: card
id: "TASK-00000131"
batch: null
specifications: []
---

# TASK-00000131 — Start and follow Claude Code sessions in the KRR window

- Owner: Development Agent
- Dependencies:

## Expected outcome

Gives the user a way to start the session of [SPEC-015](../../specs/approved/spec-015-r1.md) and see its state in the KRR window: choose a repository, describe an authorized task, start it, and read whether each session is Working, Waiting for you or Ended. Documents the feature and the Automation permission in the KRR guide. Depends on [TASK-00000130](../completion/task-00000130-control-the-terminal-window-of-a-claude-code-session-in-krr.md).

## Acceptance criteria

- [x] The window offers a task form (repository, task text) that starts a Claude Code session only after the user presses Start.
- [x] A list shows each session's state, including that an ended session can no longer be answered.
- [x] The KRR guide documents how to start a session, the signal protocol and the macOS Automation permission.
- [x] `bash apps/krr/src/macos/build-app.sh` succeeds, the Python and Swift tests pass and board validation passes.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## Evidence

The app builds and starts; Swift and Python tests pass. The form, list and live Terminal control were not exercised in a real Terminal session by the agent (Automation permission needs the User); acceptance covers them.

## History

- 2026-11-14T23:19:21+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T23:20:28+01:00 — Stage moved from `development` to `completion`.
