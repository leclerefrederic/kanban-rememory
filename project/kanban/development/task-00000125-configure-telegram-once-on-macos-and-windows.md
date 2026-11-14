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

- [ ] A single interactive tool validates the bot, discovers a fresh private-chat message, confirms the destination and sends a test with understandable recovery instructions.
- [ ] Configuration persists outside Git, with owner-only permissions on macOS and an explicit current-user ACL on Windows; cancellation and failed verification preserve existing configuration.
- [ ] The supported run command automatically loads saved configuration in new processes and supplies it to the unchanged notification sender, including the exact Batch-008 candidate. Direct environment-based calls remain supported.
- [ ] macOS and Windows instructions cover identical steps and honest verification limits.
- [ ] Automated tests exercise interactive input, Telegram failures, recipient confirmation, persistence, sender integration and platform-specific storage; applicable existing checks pass.

## Execution and evidence

- State: in-progress
- Actual start: 2026-11-14
- Blocker:
- Context: Batch-008 is delivered at candidate 843b4b3. User explicitly resumed this separate setup request to unblock its Telegram tests. Development is isolated in /tmp/krr-telegram-configuration; no Batch candidate, record or shared checkout is changed.

## History

- 2026-11-14 — User authorized this separate configuration tool after the temporary setup snippets failed. No real token or chat ID is recorded here.

- 2026-11-14T21:39:23+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14 — Resumed on the User’s instruction in an isolated worktree from main. The run wrapper supplies settings to the original candidate without modifying it.
