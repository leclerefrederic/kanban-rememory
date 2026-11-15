# Notify the user

Use only when Telegram is configured. [Setup](../setup/telegram.md) owns the private configuration. Alerts authorize nothing: answers, permissions and acceptance belong in the original chat, and a Telegram reply is not an instruction. Never include secrets or unnecessary personal data.

## Card delivery with Remy

The Orchestrator sends one alert per event. Ask in the original chat first, then send the alert before waiting.

| Scenario | Event | Summary and action | Stable event ID |
| --- | --- | --- | --- |
| A decision, access or manual action is needed | `attention` | Name the Card and the action that unblocks it. Direct the user to the original chat. | `intervention-1`, `intervention-2`, … per distinct request; keep the ID with the request on the Card. |
| A verified candidate needs approval to merge into `main` | `attention` | Give the candidate revision and any automatic deployment triggered by merging or pushing. Ask for approval in the original chat. | `merge-<full-candidate-revision>` |
| The agreed delivery is verified | `completed` | State the delivered outcome and where to find it. Say that no action is required. | `delivery` |

Use the Card ID as `--reference` and `--task`, its module as `--module` and the event ID as `--id`. Put the revision in `--text` for the merge alert. Use the actual chat as `--chat-name`; add `--link` only from a reliable environment-provided link. If approval already covers the candidate, send no merge alert; a changed candidate gets a new revision in its ID.

Send no progress, routine results, recoverable errors, timers or reminders. Intermediate Card completion is not task completion.

## Message

1. Hook: 🔔 Action required or ✅ Work completed.
2. Project (`--project`, defaults to the project name from settings).
3. Card (`--reference`), displayed with its module.
4. Summary (`--text`): at most two sentences on the request and what waits or was verified.
5. Next action (`--next-action`): starts with a verb and says where to act, or "No action required".

Write labels and text in the conversation language, English if unknown. `--language fr` supplies French labels. For another language pass `--label`, `--project-label`, `--reference-label`, `--summary-label` and `--next-action-label`. The tool does not translate free text.

## Commands

Run the wrapper from the project root. It reads the confirmed recipient and enabled events privately and never exposes the token. On Windows use `py -3`.

```sh
python3 orchestrator/tools/configure-telegram.py run -- attention --task CARD-00000042 --id intervention-1 --reference CARD-00000042 --module misc --text "The report is ready; choose its format." --next-action "Choose PDF or CSV in the original chat." --chat-name "Actual application"
```

Without `--send` before `--` this only previews; add it for the authorized send. Never pass `--send-to`. `completed` takes the same arguments with the verified summary and no-action text. `run -- test` previews and `run --send -- test` sends a test message.

## Event identity

Keep the same `--task` and `--id` for resends, including rewording, language changes and resumption in another chat. Use a new ID for a new request; when unsure, prefer a possible extra alert over a missed request.

## Delivery states

| Tool result | Action |
| --- | --- |
| `confirmed delivery` | Confirmed by Telegram, not read by a human. A retry of this event is skipped. |
| `already confirmed` | Nothing new was sent. |
| `event is disabled` / `Nothing was sent` | Keep the request in the chat and say no alert was sent. |
| `not sent, the request was refused` | Not delivered; fix the cause, then retry. |
| `delivery not confirmed and the outcome is unknown` | Tell the user; do not resend automatically. Use `--confirm-retry` only once it is known the alert did not arrive. |

Record the actual result on the Card. Claim notification only with confirmed delivery. A missing configuration or failed send never removes the chat request.
