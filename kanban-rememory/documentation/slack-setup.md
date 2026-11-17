# Configure Remy for Slack

1. In your Slack workspace, create or select a channel for Remy.
2. Create a Slack app from [Your Apps](https://api.slack.com/apps). In its settings, open **Incoming Webhooks**, activate them, and select **Add New Webhook to Workspace**. Choose the channel and select **Allow**. [Slack's webhook guide](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/)
3. Copy the generated webhook URL. Open an interactive terminal in the project root and run:

   ```sh
   python3 kanban-rememory/orchestrator/tools/notifications.py setup-slack
   ```

   On Windows, use `py -3` instead of `python3`. Paste the URL at the hidden prompt and press Enter. Keep it out of chats, command arguments, and the repository.
4. Send a setup test and check that it appears in the selected Slack channel:

   ```sh
   python3 kanban-rememory/orchestrator/tools/notifications.py test --send
   ```

Run `notifications.py status` to check the active service and the location of the configuration. Remy stores the webhook in `slack.json` alongside the Telegram configuration, outside the repository. Slack takes precedence while that file is present. To return to a previously configured Telegram destination, remove `slack.json` locally. The next status check should show Telegram.

Remy posts requests for attention and delivery confirmations in the chosen Slack channel. Make decisions and grant approvals in the conversation named in the alert.
