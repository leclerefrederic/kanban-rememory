---
type: specification
id: "SPEC-022"
---
# Show KR Orchestrator progress in the chat

## Expected outcome

The User can tell at a glance whether a Card or Batch is advancing, what stage is in progress and when their input is needed. Routine progress is visible in the original chat while the work runs.

Requested on 2026-11-15. Draft for User review.

## Scope

- When authorized work starts, show its first stage. At each meaningful stage change, post one short, visible line in the original chat before starting or waiting for the step. Use the conversation language. Examples: “Breaking Batch into tasks”, “Calling KR Developer”, “Running regression tests”, “Publishing”. Show only the stages that actually occur.
- Keep progress visible during delegated or long-running stages. At a meaningful checkpoint, show the verified progress in one line. If the step is still running after about a minute with no new checkpoint, confirm its current stage briefly. Use counts only when observed. A tool call or a note in Rememory does not replace a visible update.
- Distinguish work in progress, waiting for the User and blocked work. Ask for the User's decision or action with the necessary context, options, and consequences. When the User asks for details, answer and then return to the concise progress style.
- At completion, report the outcome briefly. Keep routine implementation details, individual checks and successful notification receipts in the work records. Surface a failure in the chat when it affects the result or requires intervention. Keep the existing acceptance, publication and Telegram rules.

## Acceptance criteria

1. **Card.** Start a Card and delegate work. Before the Developer returns, the User can see the current stage in the original chat. Later stages appear when they start, in the conversation language, with one line each.
2. **Long Batch step.** Delegate a step that runs for over a minute. The User sees a short checkpoint or ongoing status during the wait without asking. The displayed stage and any counts match observed progress.
3. **Decision or blocker.** Stop on a blocking finding or required User decision. The chat states what is waiting, why it matters and what the User needs to decide or do. Resume concise progress once work restarts.
4. **Completion.** Finish a Card or Batch with technical checks and a successful notification. The chat states the outcome briefly. Check results and delivery evidence remain available in the records.

## Resources

- [Orchestrator procedure](../../../../../agents/actions/orchestrate-work.md) defines stages, delegation and User decisions.
- [Notification procedure](../../../../../agents/actions/notify-user.md) defines Telegram events and delivery handling.
