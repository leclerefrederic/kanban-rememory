---
type: card
id: "TASK-00000125"
batch: null
specifications: []
---
# TASK-00000125 — Configure Telegram once on macOS and Windows

- Owner: Development Agent
- Dependencies: existing Telegram sender
- Approval to execute: User explicitly requested a single tested setup tool and macOS/Windows procedures in this chat, 2026-11-14.
- Priority: targeted User request following failed interactive setup attempts.

## Expected outcome

Configure Telegram once through a normal Python command on macOS or Windows, without pasted scripts, manual chat-ID lookup or repeated environment exports. Agents automatically reuse the saved configuration. Preserve the Batch-008 acceptance candidate and its scope; this separate request is developed on codex/telegram-configuration from main, in its own worktree.

## Acceptance criteria

- [x] A single interactive tool validates the bot, discovers a fresh private-chat message, confirms the destination and sends a test with understandable recovery instructions.
- [x] Configuration persists outside Git, with owner-only permissions on macOS and an explicit current-user ACL on Windows; cancellation and failed verification preserve existing configuration.
- [x] The supported run command automatically loads saved configuration in new processes and supplies it to the unchanged notification sender, including the exact Batch-008 candidate. Direct environment-based calls remain supported.
- [x] macOS and Windows instructions cover identical steps and honest verification limits.
- [x] Automated tests exercise interactive input, Telegram failures, recipient confirmation, persistence, sender integration and platform-specific storage; applicable existing checks pass.

## Execution and evidence

- State: completed
- Actual finish: 2026-11-14
- Actual start: 2026-11-14
- Blocker:
- Context: Batch-008 is delivered at candidate 843b4b3. User explicitly resumed this separate setup request to unblock its Telegram tests. Development is isolated in /tmp/krr-telegram-configuration; no Batch candidate, record or shared checkout is changed.

## History

- 2026-11-14 — User authorized this separate configuration tool after the temporary setup snippets failed. No real token or chat ID is recorded here.

- 2026-11-14T21:39:23+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14 — Resumed on the User’s instruction in an isolated worktree from main. The run wrapper supplies settings to the original candidate without modifying it.

## Verification and closure

- Implementation revision: `4c7c0cb`. Reviewed the full implementation and documentation diff while in Development.
- [Native CI](https://github.com/leclerefrederic/kanban-rememory/actions/runs/43641670969): macOS 22 passing tests; Windows 20 passing tests, two POSIX-only tests skipped. Windows ran native private-file ACL/persistence operations. API traffic is simulated.
- Local checks: 22 setup tests, 25 existing adoption tests, board validation, skill synchronization and whitespace checks passed.
- User confirmed full live macOS setup in this chat on 2026-11-14. Real Telegram delivery on Windows remains unexecuted; native CI is not a claim of live Windows delivery.
- Matching setup/run procedures are in agents/configure-telegram.md. The unchanged Batch-008 sender can receive configuration using run --script.
- Flow review: this was the only active card (WIP 1/1); no setup blocker remains. Existing backlog cards remain outside this targeted request. Next action is the separate Batch-008 notification acceptance against its recorded candidate; no Batch verdict is inferred.

- 2026-11-14T22:14:43+01:00 — Stage moved from `development` to `completion`.
