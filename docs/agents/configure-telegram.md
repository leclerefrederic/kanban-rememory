# Configure Telegram notifications

Copy `tools/notify-telegram.py` to the project if you want Telegram notifications.

1. Create a bot with BotFather. Set `TELEGRAM_BOT_TOKEN` through the secret settings of the environment running the Development Agent.
2. Open the bot chat and send `/start`, or add the bot to the intended group and send it a command. Use a trusted Bot API client to call `getUpdates` and read the numeric `message.chat.id` from that message. Set it as `TELEGRAM_CHAT_ID` in the same environment.
3. Run `python3 tools/notify-telegram.py test` to review the destination. Rerun with `--send-to CHAT_ID` using the numeric ID shown. Confirm receipt in Telegram.
4. Set `TELEGRAM_EVENTS` to a comma-separated selection of `delivered,blocked,closed`. Clear it to disable event notifications.

From the project root, call the tool with the event, Batch ID, and confirmed chat ID. For example:

```sh
python3 tools/notify-telegram.py delivered --batch Batch-001 --send-to "$TELEGRAM_CHAT_ID"
```

Use `blocked` with a stable `--blocker-id` and record the actionable details in the Batch report. Use `closed` after verifying publication and recording the outcome in the report. The command stores successful sends in the shared local Git directory. Retries in that clone skip recorded sends. After an ambiguous failure, check the destination before retrying. Telegram may have received the message before the local receipt was recorded.

See the [Telegram Bot API](https://core.telegram.org/bots/api).
