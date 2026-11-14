---
type: specification
id: "SPEC-011"
revision: "1"
---
# Telegram alerts for attention and task completion

## Expected outcome

The User can leave the Development Agent working and do something else without monitoring the chat. Telegram tells them when their help or an action is required, or when their requested task is finished. They can identify the project, understand why they were notified, and return to the right chat.

The User agreed to this notification model in conversation on 2026-11-14 and requested this Specification. This records the requested behavior; implementation has not been authorized by this writing request.

## Scope

### When to notify

- Apply the same behavior to Development Agent work with or without a Batch, using the project's enabled Telegram destination. A task means the outcome requested by the User, which may require several Cards. Completing an intermediate Card does not by itself complete that request.
- Send **Intervention needed** as soon as the agent needs a decision, clarification, authorization, acceptance test, or manual action from the User. Present the request in the chat and send the alert when that need is identified, before waiting for the answer. Do not wait for two failed attempts when a human action is already necessary.
- Pause the work that depends on that answer. Continue independent, already authorized work when the workflow and execution environment allow it. Silence or elapsed time is not approval.
- Send **Task completed** only after the requested outcome is achieved, its required checks pass, and its agreed delivery steps are verified. Claim publication or deployment only if it was required and actually verified. If User validation or another required action is still pending, send **Intervention needed** instead.
- Send no progress updates, routine intermediate results, or alerts for errors the agent can resolve without the User. A later, distinct need for intervention and the eventual completion remain separate notification events.

### What the message contains

- Use the User's conversation language. Make the two message types immediately distinguishable; wording and optional icons may follow that language.
- Identify the project and the requested task in human-readable terms. Include the chat title or another reliable way to identify the conversation to resume, plus a direct link when the environment provides one. If no usable link is available, identify the application and chat without inventing a URL.
- For intervention, state briefly what is waiting and the specific question, decision, or action required. The User must be able to understand why they need to return without opening technical records first.
- For completion, summarize the verified result and state that no required User action remains for that task.
- Telegram is an alert channel. The existing chat remains the place for answers, permissions, and acceptance decisions. Receiving an alert does not authorize an action, and this version does not process Telegram replies as agent commands.

### Avoid duplicate alerts and preserve delivery evidence

- Send one confirmed notification per intervention request or completed task. Retrying an event or resuming the same work in another session of the same project must not repeat an already confirmed alert. Distinct projects, tasks, requests, or new candidates requiring fresh acceptance must remain independently notifiable.
- Reuse the existing Telegram configuration and Batch notification flow. A Batch delivery awaiting acceptance is an intervention event; the same event must not generate both a legacy alert and an additional attention alert. An enabled closure alert and task-completion alert must likewise not duplicate the same completed outcome.
- Respect disabled notifications. If Telegram is unconfigured, disabled, or an attempted send fails, retain the request or result in the chat and make the notification status visible there. Do not claim the User was notified when delivery was not confirmed. After an ambiguous delivery failure, preserve that uncertainty rather than silently treating it as success or blindly resending.
- Keep existing permissions and secret-handling rules. This feature adds no scheduler, periodic reminder, Telegram command interface, or automatic approval.

## Acceptance criteria

Use an isolated project and a confirmed test Telegram destination for delivery checks. Exercise the notification triggers from an actual Development Agent session, not only by invoking a sender directly. Development Agent supplies the exact candidate revision and environment. The scenarios below are acceptance requirements, not recorded results.

1. **Immediate intervention:** With a standalone task running and Telegram enabled, make further work require a User decision, then separately a manual action. Each case produces one actionable Telegram alert at the point of waiting, without requiring two failed attempts. The matching request is present in the chat; dependent work does not proceed without the answer.
2. **Independent work:** While one action waits for the User, leave another authorized action that can proceed within the workflow limits. Verify that it can continue, while the blocked action remains paused and no reminder is sent merely because time passes.
3. **Completion at the requested outcome:** Give the agent one request requiring two Cards. Complete the first Card, then complete the whole request and its required checks and delivery steps. No completion alert is sent for the first Card; exactly one is sent for the finished request, summarizing only verified results.
4. **Acceptance is still required:** Deliver a Batch candidate that awaits User testing or a verdict. Verify that the User receives one intervention alert, no task-completed claim, and no duplicate legacy delivery alert. After the required decision and verified delivery, the completed outcome generates one completion alert.
5. **Resume and distinct events:** Retry a confirmed intervention and completion, then resume the same work in a fresh agent session. Neither alert repeats. A different intervention on the task, a corrected candidate requiring new acceptance, and a task with the same title in another project each remain notifiable.
6. **Find the right chat:** Exercise an intervention and a completion with a usable chat link, then without one. Each message identifies the project, task, and chat, uses the conversation language, and states either the required action or verified result. A supplied link opens the intended chat; without a link, the application and chat identification are sufficient to find it.
7. **Quiet autonomous work:** Exercise ordinary progress, an intermediate Card completion, and a transient failure resolved by the agent. None produces an attention or completion alert. If human help subsequently becomes necessary, the intervention is notified.
8. **Configuration and delivery failure:** Exercise disabled notifications, missing configuration, a definite send failure, and an ambiguous send outcome. The chat retains the request or result and accurately reports the notification state. No disabled send occurs, no unconfirmed delivery is claimed as successful, and ambiguous delivery is not blindly resent. A confirmed retry is subsequently deduplicated.
9. **Chat remains authoritative:** Reply to an alert in Telegram. Verify that it does not approve, resume, or alter agent work. Provide the required answer in the original chat and verify that work resumes under the existing authorization rules.

## Resources

No mockup or external attachment is required. The message content and observable behavior are defined above.
