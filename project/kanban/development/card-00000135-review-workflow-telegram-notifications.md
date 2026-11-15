---
type: card
id: "CARD-00000135"
batch: null
specifications: []
---
# CARD-00000135 — Review workflow Telegram notifications

- Owner: KR Developer — card135_developer
- Dependencies: Batch-010 Orchestrator workflow. Schedule execution under the existing Batch and work-in-progress rules.

## Expected outcome

When Remy is enabled, the user receives the applicable Telegram alert when their intervention is needed, when a developed Batch is delivered for acceptance, and when a standalone Card's requested work is finished and verified. The user can rely on alerts without asking the agent to send them.

## Authorization

- 2026-11-15 — After consolidating SPEC-014 and approving the message structure and language rules, the User authorized execution: “ok lance la carte en dev.” Implement the consolidated scope below; preserve cadence. Publication to origin/main follows repository standing authorization after verified closure.
- CARD-00000128 awaits an approved Specification revision; CARD-00000135 is the oldest eligible Card and is explicitly selected by the User.

## Scope

Review the existing rules and their execution across the Orchestrator and Development Agent handoff. Check who sends each alert, when they send it, and how delivery and duplicate prevention are checked. Preserve the distinction between a candidate delivered for acceptance, a completed standalone request, and a verified Batch closure. Record any discrepancy and propose a follow-up if correction would change agreed notification behavior.

### Consolidated deduplication scope (formerly SPEC-014)

The User requested merging SPEC-014 revision 1 into this Card on 2026-11-15. This Card now owns that scope; the former draft is retained only as a traceability pointer. The merge initially authorized consolidation only; the subsequent execution authorization above covers this scope.

- Preserve option C, chosen by the User on 2026-11-14: the agent declares a resend by retaining the identifier and a new request by choosing a new identifier. The tool does not infer meaning from text. When unsure, the agent uses a new identifier; an extra alert is preferable to a missed request.
- Approved sameness rule: project, event kind, task and declared identifier identify an alert. Rewording a confirmed resend must not send it again, including after resuming in another session. Different requests, tasks, projects and corrected candidates requiring acceptance remain independently notifiable.
- Review the agent instructions, Telegram procedure and compatibility with the existing receipt registry. The current documented key includes text; identify the changes needed to meet the proposed rule rather than assuming instructions alone are sufficient. Implement the necessary correction within this approved rule.
- Preserve the existing triggers. No periodic reminders, Telegram command interface or new channel are included.
- Context: [SPEC-011](../../specs/approved/spec-011-r1.md), duplicate-alert requirements; Batch-008-DEBT-01, corrected by candidate `65b02a5`. Keeping text in the key was rejected because rewording duplicates alerts; using an identifier alone was rejected because it can suppress distinct requests.

### Message clarity under review

The User's 2026-11-15 screenshot shows messages with inconsistent structure and insufficient references or expected actions. Keep the User's conversation language. Review whether each alert identifies the relevant Card or Batch, the requested work, the exact action expected or verified result, and the chat to resume. The User approved the message layout below on 2026-11-15.

### Approved message structure

The User approved this structure on 2026-11-15:

1. An emoji and short hook: 🔔 Action required, 🧪 Ready to test, or ✅ Work completed, matching the event.
2. Project name.
3. Relevant Card or Batch ID.
4. Brief summary: at most two sentences describing what awaits attention or the verified outcome.
5. Next action: a concrete action beginning with a verb, stating where to act. If nothing is required, say so explicitly.

Translate the hook, field labels and prose into the User's conversation language. Use English only when that language is unknown. Keep identifiers unchanged. When referring to the conversation, use its actual application and available title; Codex is an example, never a fixed value or assumed host. Include a direct chat link only when available and reliable; never invent an application, title or URL.

Sending Telegram is an external notification tool action. It does not replace the original chat for questions, answers, authorizations or acceptance decisions. Preserve the existing configured recipient, send authorization and delivery-confirmation rules. The approved structure does not change notification cadence; execution is authorized above.

## Acceptance criteria

- [ ] Walk through an intervention that requires user authorization. The actionable question is posted in the original chat and one alert is sent before waiting.
- [ ] Walk through a developed Batch delivered for acceptance. One delivery alert identifies the tested candidate and the next action. An additional generic intervention alert is not sent for the same delivery.
- [ ] Walk through a standalone Card whose requested work is finished and verified. One completion alert reports the outcome. When a User action is still required, the alert reflects that instead.
- [ ] Verify that a report relayed between Developer and Orchestrator, repeated milestones and a resumed session do not produce duplicate alerts. Verify that a disabled or failed Telegram send leaves the next action visible in the original chat.
- [ ] Record findings and evidence, including any gaps between written rules and behavior on Codex and Claude Code.

- [ ] In an isolated project, resend a confirmed alert with identical identifiers and text, then with reworded text from a fresh session: neither resend produces a second alert under the approved rule. Record any current mismatch.
- [ ] Verify that a different request with a new identifier, the same wording on another task or project, and a corrected candidate remain notifiable; uncertainty leads the agent to use a new identifier.
- [ ] Verify that Batch closure and completion produce one alert for the same outcome, and that an earlier receipt registry retains its receipts without unexpected duplicates.
- [ ] Verify that intervention, acceptance and completion examples follow the approved five-part structure, identify the relevant Card or Batch and state the expected action or explicitly that none is required.
- [ ] Verify French conversation output, English fallback when the language is unknown, and actual chat references for Codex and Claude Code without a hardcoded host or invented link.

## Execution and evidence

- State: in-progress
- Actual start: 2026-11-15
- Actual finish:
- Blocker: none
- Target: origin/main

### Legacy receipt decision

On 2026-11-15 the User chose: “Oui, privilégier une alerte en cas de doute”. Earlier receipts retain only a hash of task and text. Preserve them; recognize an exact original-text match and migrate its confirmed or uncertain state to the stable key. An agent can supply the known original text when resending a reworded old alert. Without a provable match, use a new identifier when in doubt; a possible duplicate is accepted rather than suppressing a legitimate request. No claim of universal automatic migration of old reworded receipts is made.

## History

- 2026-11-15 — User requested a review after the Batch-010 publication decision was posted without its intervention alert. User confirmed receipt after the alert was sent. The review covers both intervention and delivery or completion triggers.

- 2026-11-15 — User requested “Merge spec 14 avec notre carte”. Consolidated SPEC-014 scope, prior decision and scenarios here, alongside the message-clarity review. No implementation or acceptance verdict is recorded by this merge.

- 2026-11-15 — User approved the five-part message structure and clarified that Codex must not be hardcoded; use the User's language, otherwise English. This records the content decision, not implementation or test evidence.

- 2026-11-15T11:02:58+01:00 — Stage moved from `backlog` to `development`.
