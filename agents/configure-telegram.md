# Configure Telegram notifications

Copy `agents/tools/notify-telegram.py` to the project if you want Telegram notifications.

1. Create a bot with BotFather. Set `TELEGRAM_BOT_TOKEN` through the secret settings of the environment running the Development Agent.
2. Open the bot chat and send `/start`, or add the bot to the intended group and send it a command. Use a trusted Bot API client to call `getUpdates` and read the numeric `message.chat.id` from that message. Set it as `TELEGRAM_CHAT_ID` in the same environment.
3. Run `python3 agents/tools/notify-telegram.py test` to review the destination. Rerun with `--send-to CHAT_ID` using the numeric ID shown. Confirm receipt in Telegram.
4. Set `TELEGRAM_EVENTS` to a comma-separated selection of `attention,completed`. The Batch events `delivered`, `blocked` and `closed` are accepted as well: `delivered` and `blocked` send the same alert as `attention`, and `closed` the same as `completed`. Clear the variable to disable alerts.

## Send an alert

Telegram only alerts the User. The chat stays the place for answers, permissions and acceptance decisions, a Telegram reply changes nothing, and the tool adds no reminder or scheduler.

From the project root, give the task, a stable ID, what is waiting or the verified result, and the conversation to resume. Write `--text` and `--label` in the User's language; the icon keeps the two alerts distinguishable. Add `--link` only if the environment provides a direct link, and never invent one. For example:

```sh
python3 agents/tools/notify-telegram.py attention --task "Export report" --id export-format --text "Choose the file format." --chat-name "Claude Code · Export report" --send-to "$TELEGRAM_CHAT_ID"
python3 agents/tools/notify-telegram.py completed --task "Export report" --id export-report --text "Report exported; checks passed." --chat-name "Claude Code · Export report" --send-to "$TELEGRAM_CHAT_ID"
```

Without `--send-to`, the command shows a preview and sends nothing. The project name defaults to the repository folder name; `--project` overrides it.

For a Batch, use the Batch events so the same event never produces two alerts:

```sh
python3 agents/tools/notify-telegram.py delivered --batch Batch-001 --revision FULL_TESTED_COMMIT --send-to "$TELEGRAM_CHAT_ID"
```

Use the full tested commit from `tests.md` as `--revision`: each delivery of a Batch, including a corrected one, sends once. Use `blocked` with a stable `--blocker-id`. After a Batch closes and its publication is verified, use `closed`; if you also send `completed` for that Batch, give the Batch ID as `--id` so the two are one outcome.

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
