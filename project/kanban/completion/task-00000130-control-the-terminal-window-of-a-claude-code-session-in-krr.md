---
type: card
id: "TASK-00000130"
batch: null
specifications: []
---

# TASK-00000130 — Control the Terminal window of a Claude Code session in KRR

- Owner: Development Agent
- Dependencies:

## Expected outcome

Implements the Terminal and intervention parts of [SPEC-015](../../specs/approved/spec-015-r1.md) in KRR. KR starts Claude Code in a minimized Terminal window it can identify, reads `signals.jsonl`, and for each new `waiting` ID restores that window at normal size, brings it forward and sends one Telegram alert through `configure-telegram.py run --send -- attention`; the window comes forward even when the alert is disabled or fails. A `resumed` signal minimizes it again; while the user is still unresolved the window stays visible. Other Terminal windows are never touched. A session whose window closes or whose launcher exits is marked ended. Scheduled watchers are unchanged. Depends on [TASK-00000129](../completion/task-00000129-signal-when-claude-code-waits-for-the-user.md).

## Acceptance criteria

- [x] A tested state machine handles `waiting` once per ID, ignores a repeated ID, minimizes on `resumed`, and ignores signals after the session ended.
- [x] The Terminal window is started minimized, identified by its window ID, and only that window is restored or minimized.
- [x] The alert is requested once per intervention and a failure or disabled Telegram never prevents bringing the window forward.
- [x] A closed window or exited session becomes `ended` and no further window action happens.
- [x] Automated tests cover the state machine and the script building with a fake Terminal; the app builds with warnings as errors.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## Evidence

Swift logic tests with a fake Terminal pass (`apps/krr/tests/macos/run-tests.sh`) and the app builds. The real Terminal AppleScript (`TerminalApp`) could not be exercised from the agent session because Automation permission needs the User; it is covered by the acceptance cases.

## History

- 2026-11-14T23:16:38+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T23:19:21+01:00 — Stage moved from `development` to `completion`.
