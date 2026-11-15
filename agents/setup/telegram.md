# Configure the Telegram option

Install only under the project's recorded authorization. Copy `agents/tools/configure-telegram.py` and `agents/tools/notify-telegram.py`; require Python 3.9+ and network access for real setup. This option shares one private recipient configuration per operating-system account across Codex/Claude projects. No scheduler is installed.

Give the User the [private setup guide](../../documentation/telegram-setup.md). They run the interactive command in Terminal/PowerShell and enter the token privately; never ask them to paste it into chat, shell arguments or a repo file. The tool verifies the bot, fresh `/setup_...` message, intended recipient and test receipt before saving. Failed/cancelled replacement preserves previous settings.

```sh
python3 agents/tools/configure-telegram.py status
python3 agents/tools/configure-telegram.py test
```

On Windows use `py -3` (or the installed Python command). Status and test without `--send` expose no token and send nothing. Initial setup is `python3 agents/tools/configure-telegram.py`; `test --send` is a real test to the confirmed recipient. Record configuration saved, real API delivery and User receipt confirmation separately; none is Batch acceptance.

macOS config is `~/.config/kanban-rememory/telegram.json` with mode 600; Windows `%LOCALAPPDATA%\KanbanRememory\telegram.json` uses a current-user-only ACL established before writing. It is plaintext private configuration, not Keychain/Credential Manager. Configure another computer/account separately. Do not execute old `telegram.env` files.

If a sandbox prevents file/network access, request only the required environment permission; do not bypass it or expose the secret. Interactive setup refuses redirected input/EOF. Follow the human guide for wrong tokens, missing setup codes, competing webhook/readers, permissions and uncertain delivery; the tool does not delete webhooks or discard queued updates.

For work alerts load [notification actions](../actions/notify-user.md), including cadence, exact revision, deduplication and delivery-state recovery. Do not introduce a new per-project opt-in/default-disabled behavior through installation instructions; follow current project policy.

## Verify

`python3 agents/tools/test-telegram-setup.py` uses fake credentials and simulated responses, no real messages. On macOS it also tests a real hidden-input terminal. Windows ACL behavior is native only when run on Windows; mocks do not prove a Windows run. Record automated tests, native platforms and real delivery separately; unexecuted checks are not passes.
