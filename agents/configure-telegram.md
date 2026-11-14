# Configure Telegram once on macOS or Windows

Use `agents/tools/configure-telegram.py`. It configures one private Telegram conversation for the current operating-system account, outside the repository. Claude Code and Codex can then load the same settings through its `run` command, including from fresh sessions. No shell exports, pasted Python snippets, third-party ID bot or manual chat-ID lookup are needed.

Copy both `agents/tools/configure-telegram.py` and `agents/tools/notify-telegram.py` when adopting this optional feature in another project. Python 3.9 or later and an internet connection are required. The workflow is the same on both systems; Windows uses the Python launcher `py -3` (or `python` if that is your installed command).

## Before starting

1. In Telegram, open [BotFather](https://t.me/BotFather), send `/newbot`, and create your notification bot. Keep its API token private. For an existing bot such as Remy, reuse its token; there is no need to create another bot.
2. Open a normal Terminal on macOS or PowerShell on Windows, and change to the repository directory. Do not paste the token into the chat, a shell command, or a repository file. The setup tool asks for it with hidden input.

## macOS

From the repository directory:

```sh
python3 agents/tools/configure-telegram.py
```

## Windows

From the repository directory in PowerShell:

```powershell
py -3 agents/tools/configure-telegram.py
```

## The same setup steps on both systems

1. Paste the API token when asked. Nothing appears while typing: that is expected.
2. The tool verifies the token with Telegram and displays the bot's name and exact conversation link. Confirm visually that this is your bot.
3. Open that link. Press **Start** if necessary, then send the unique `/setup_...` message printed by the tool. Return to the Terminal and press Enter. **The bot does not automatically reply**; the next result appears in the Terminal. This fresh code identifies your conversation without relying on old `/start` messages.
4. The tool shows the detected person's name and numeric chat ID. Answer `y` only if this is the intended recipient. This authorizes the test and future alerts through this configuration.
5. The tool sends a test. Check that it arrived in that Telegram conversation, then answer `y` to confirm receipt. Only then is configuration saved. If replacing existing settings, cancellation or a failed test leaves the previous settings intact.

Success means both that the test arrived and that the Terminal printed **Configuration saved**. This proves configuration and test delivery, not completion of the Batch acceptance scenarios.

## Storage and later tests

| System | Configuration file | Protection |
| --- | --- | --- |
| macOS | `~/.config/kanban-rememory/telegram.json` | File mode `600`: only the account owner can read or write it. |
| Windows | `%LOCALAPPDATA%\KanbanRememory\telegram.json` | A new file receives an explicit current-user full-control ACL and no inherited permissions before the token is written. Saving is refused if this fails. |

The token is stored in this private file in plain text, not in the macOS Keychain or Windows Credential Manager. It is never put in Git or printed by the tool. It is shared by projects using the same OS account; configure separately on another computer or OS account. The saved event list supports both the Batch notifications and the attention/completed events when the selected sender implements them.

Display configuration status without exposing the key, or send another test:

```sh
python3 agents/tools/configure-telegram.py status
python3 agents/tools/configure-telegram.py test --send
```

On Windows, replace `python3` with `py -3`. `test` without `--send` displays the destination and sends nothing. To change the bot or recipient, run the initial setup again. The tool asks before replacing existing configuration. It does not read or execute the earlier experimental `telegram.env` file.

## Commands for Development Agents

Use `configure-telegram.py run` for each send: it reads the saved file and passes settings to a child process. It overrides any stale `TELEGRAM_*` values for that child only. Neither the parent shell nor the application needs to be restarted. It never prints the token or puts it in command arguments.

For example, preview a test, then send it:

```sh
python3 agents/tools/configure-telegram.py run -- test
python3 agents/tools/configure-telegram.py run --send -- test
```

The default sender is `notify-telegram.py` beside the setup tool. The wrapper only supplies configuration; it preserves the sender's event validation, deduplication, result messages and exit code. Use that sender's supported event arguments after `--`. Without `--send`, the sender previews; with `--send`, the wrapper supplies the previously confirmed recipient. Do not supply `--send-to` yourself.

For a Batch delivery:

```sh
python3 agents/tools/configure-telegram.py run --send -- delivered --batch Batch-001 --revision FULL_TESTED_COMMIT
```

The supplied revision must be the full tested commit from the Batch records. Direct calls to `notify-telegram.py` with explicit environment variables and `--send-to` remain supported. This setup tool does not replace the project's authorization or notification rules, and does not make a Telegram reply an instruction.

### Test an unchanged acceptance candidate

Keep the candidate in its designated scratch checkout. To supply configuration without editing or replacing its sender, use its absolute path with `--script`:

```sh
python3 agents/tools/configure-telegram.py run --script "/path/to/candidate/agents/tools/notify-telegram.py" --send -- test
```

PowerShell equivalent (replace the example path with the actual candidate path):

```powershell
py -3 agents/tools/configure-telegram.py run --script "C:\path\to\candidate\agents\tools\notify-telegram.py" --send -- test
```

For Batch-008, use the sender from its recorded revision, with the attention/completed event arguments defined by that candidate. Do not test the older sender on main and present that result as Batch-008 acceptance. The wrapper does not advance its status or record a verdict.

## If a step fails

- **No code found:** verify the displayed bot link and send the exact new `/setup_...` text in its private conversation. Press Enter or choose retry in the tool. No manual ID search is needed. Cancel with Ctrl+C if needed.
- **Wrong token:** copy the API token from BotFather, not the bot's username. No settings are replaced.
- **Webhook or another reader:** use a bot dedicated to notifications, or have the owner stop its competing reader. The tool does not delete webhooks or acknowledge/discard pending updates. A full pending queue is reported rather than silently consumed.
- **Network failure or uncertain test delivery:** check Telegram before retrying. The tool does not automatically repeat a send whose outcome is unknown, and preserves previous settings.
- **Redirected input / EOF:** run the file normally in Terminal or PowerShell, as shown above. Do not use `python -`, a pipe, or a here-document. The tool refuses noninteractive setup before asking for the key.
- **File or permissions error:** the tool cannot confirm configuration. Fix access to the displayed per-user location and rerun. Do not weaken permissions or store the token in the repository.
- **Agent sandbox prevents access or networking:** grant the narrow access needed to the saved file and Telegram using the agent environment's permission mechanism. The tool cannot bypass that boundary. Do not paste the token into a chat as a workaround.

## Verification

Run `python3 agents/tools/test-telegram-setup.py` on macOS or `py -3 agents/tools/test-telegram-setup.py` on Windows. Tests use fake credentials and simulated Telegram responses; they send no Telegram messages. On macOS, the regression test runs a real terminal session with hidden input. Windows exercises its native ACL handling when the suite is run there; a mocked ACL test alone is not proof of a Windows run.

Record live bot delivery and Windows execution separately from automated test results. An unexecuted platform check or real Telegram test is not a pass.

References: [Telegram bot setup](https://core.telegram.org/bots/tutorial), [Bot API](https://core.telegram.org/bots/api), [Windows icacls](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/icacls), [Windows whoami](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/whoami).
