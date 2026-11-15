# Configure the Telegram option

Install only under the project's recorded authorization. Copy `orchestrator/tools/configure-telegram.py`, `orchestrator/tools/notify-telegram.py` and `orchestrator/tools/test-telegram-setup.py`. Real setup needs Python 3.9+ and network access. One private recipient configuration serves every project of the operating-system account. No scheduler is installed.

Give the user the [private setup guide](../../documentation/telegram-setup.md). They run the interactive command in Terminal or PowerShell and enter the token privately; never ask for it in chat, shell arguments or a repository file. The tool verifies the bot, a fresh `/setup_...` message, the recipient and a test receipt before saving. A failed or cancelled replacement keeps the previous settings.

```sh
python3 orchestrator/tools/configure-telegram.py status
python3 orchestrator/tools/configure-telegram.py test
```

On Windows use `py -3`. `status` and `test` without `--send` expose no token and send nothing; `test --send` sends a real test. Record saved configuration, API delivery and the user's receipt confirmation separately.

The configuration is `~/.config/kanban-rememory/telegram.json` (mode 600) on macOS and `%LOCALAPPDATA%\KanbanRememory\telegram.json` with a current-user-only ACL on Windows. It is plaintext private configuration. Do not execute old `telegram.env` files.

If a sandbox blocks file or network access, request only that permission; never bypass it or expose the secret. Follow the human guide for wrong tokens, missing setup codes, competing webhooks and uncertain delivery. Work alerts follow [notification actions](../actions/notify-user.md).

## Verify

`python3 orchestrator/tools/test-telegram-setup.py` uses fake credentials and simulated responses and sends nothing. On macOS it also tests a real hidden-input terminal; Windows ACL behavior is native only on Windows. Unexecuted checks are not passes.
