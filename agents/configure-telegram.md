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

## Send an alert

Telegram only alerts the User. The chat stays the place for answers, permissions and acceptance decisions, a Telegram reply changes nothing, and the tool adds no reminder or scheduler.

From the project root, use the wrapper in [Commands for KR Developers](#commands-for-kr-developers). Sending Telegram is an external tool action: use the configured, confirmed recipient and check the delivery result. One agent, ordinarily KR Developer, sends the event even when the Orchestrator relays its result.

### Message structure and language

Every work alert has the same five parts:

1. Emoji and hook: 🔔 Action required, 🧪 Ready to test, or ✅ Work completed.
2. Project name (`--project`, otherwise the repository folder name).
3. Card or Batch ID (`--reference` for attention/completed, `--batch` for Batch events).
4. Brief summary (`--text`): at most two sentences describing the requested work and what is waiting or what was verified. The delivery event also includes the tested revision.
5. Next action (`--next-action`): begin with a verb and state the concrete decision or action and where to act. When nothing is required, say "No action required" in the User's language.

Use the User's conversation language for the hook, labels, summary and next action. If the language is unknown, use English. `--language fr` supplies French hooks and labels; English is the default. For another known language, supply `--language`, a translated `--label` (text only; the tool supplies the emoji), and `--project-label`, `--reference-label`, `--summary-label`, `--next-action-label` (plus `--revision-label` for delivery). These are tool arguments for the agent, not questions for the User. The tool does not translate free text or infer the conversation language.

For an action or acceptance alert, supply `--chat-name` with the actual application and available conversation title. Do not hardcode Codex or Claude Code: those names in examples are placeholders for the real host. Add `--link` only when the environment provides a reliable direct chat link. Never invent a host, title or URL. Do not replace the required action with a bare "see tests.md" or "see report.md".

```sh
python3 agents/tools/configure-telegram.py run --send -- attention --task "Export report" --id export-format --reference CARD-00000042 --text "The report is ready to export; its format needs your decision." --next-action "Choose PDF or CSV in the original chat." --chat-name "Actual application · Export report"
python3 agents/tools/configure-telegram.py run --send -- completed --task "Export report" --id export-report --reference CARD-00000042 --text "The report was exported and its contents verified." --next-action "No action required." --chat-name "Actual application · Export report"
```

Without `--send`, the command renders a preview and sends nothing. The wrapper supplies the saved recipient and enabled events (`attention`, `completed`, `delivered`, `blocked`, `closed`).

### Cadence and duplicate prevention

Send when human intervention becomes necessary (after asking in the original chat, before waiting), when a candidate is delivered for acceptance, or when the requested outcome is finished and verified. Do not send routine progress, intermediate Card completion or errors resolved autonomously. There is no timer, periodic reminder, minimum delay or automatic resend because the User has not answered. A distinct later request remains a separate event.

The agent declares sameness: retain the same stable `--id` for a resend, even with different wording or after resuming in another chat; use a new ID for a new request. When unsure, use a new ID: a possible extra alert is preferable to a missed request. Keep `--task` stable across resends. The key is destination, project, kind, task and declared ID; wording, language and conversation title are not part of it.

Older receipts contain a hash of task and text rather than their original values. They are preserved and recognized when the original wording matches. For a reworded pre-upgrade resend, supply the known original wording with `--previous-text` so the tool can prove the match. Once matched, later rewordings use the stable key. Without a provable match, check the original alert; if still uncertain, choose a new ID and accept the possible duplicate. The tool cannot reconstruct old wording and does not silently suppress ambiguous new requests.

For Batch delivery, use `delivered` with the full tested commit from `tests.md`, not a second generic attention alert. Each corrected candidate remains independently notifiable:

```sh
python3 agents/tools/configure-telegram.py run --send -- delivered --batch Batch-001 --revision FULL_TESTED_COMMIT --text "The approved changes are implemented and verified." --next-action "Start the guided acceptance tests in the original chat." --chat-name "Actual application · Batch acceptance"
```

Use `blocked` with a stable `--blocker-id`, a brief summary and the specific action needed to unblock work. After Batch closure and publication are verified, use `closed` with its verified summary and explicit next action; do not also send `completed`. The aliases `closed` and `completed` with the same Batch reference and Batch ID as `--id` share one outcome. The Batch ID is their canonical task regardless of its human-readable title.

## Delivery states

The tool prints one state line and records alerts in the shared local Git directory.

| Output | Meaning | What to do |
| --- | --- | --- |
| `confirmed delivery` | Telegram confirmed the message. | Nothing. A retry of the same alert is skipped. |
| `already confirmed` | This alert was sent earlier. | Nothing. |
| `event is disabled` or `Nothing was sent` | The event is off or the configuration is missing. | Keep the request or result in the chat and say that no alert was sent. |
| `not sent, the request was refused` | Telegram certainly did not deliver it. | Fix the cause and retry; a retry is safe. |
| `delivery not confirmed and the outcome is unknown` | The message may have been delivered. | Tell the User in the chat. Check the destination, then rerun with `--confirm-retry` only if it did not arrive. A plain rerun is refused. |

Never tell the User that they were notified unless the tool printed `confirmed delivery`.

See the [Telegram Bot API](https://core.telegram.org/bots/api).

## Commands for KR Developers

Use `configure-telegram.py run` for each send: it reads the saved file and passes settings to a child process. It overrides any stale `TELEGRAM_*` values for that child only. Neither the parent shell nor the application needs to be restarted. It never prints the token or puts it in command arguments.

For example, preview a test, then send it:

```sh
python3 agents/tools/configure-telegram.py run -- test
python3 agents/tools/configure-telegram.py run --send -- test
```

The default sender is `notify-telegram.py` beside the setup tool. The wrapper only supplies configuration; it preserves the sender's event validation, deduplication, result messages and exit code. Use that sender's supported event arguments after `--`. Without `--send`, the sender previews; with `--send`, the wrapper supplies the previously confirmed recipient. Do not supply `--send-to` yourself.

For a Batch delivery:

```sh
python3 agents/tools/configure-telegram.py run --send -- delivered --batch Batch-001 --revision FULL_TESTED_COMMIT --text "The approved changes are implemented and verified." --next-action "Start the guided acceptance tests in the original chat." --chat-name "Actual application · Batch acceptance"
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
