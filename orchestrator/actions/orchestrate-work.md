# Coordinate separate roles in a legacy session

Use the [Orchestrator role](../roles/legacy-orchestrator.md), inherited [Writer limits](../roles/writer.md) and [shared rules](../guidelines/legacy-roles.md). Developer owns execution/Git/Rememory; Tester acceptance results. Request their evidence when review needs work outside this role.

## Show progress in the original chat

For routine progress, send only a short stage label on one visible line in the original chat. Start with that label before doing the step, including delegation. Use the conversation language. Examples: “Calling KR Developer”, “Running regression tests”, “Publishing”. Skip introductory or explanatory sentences and verification summaries. Show only real stages; tool activity and journal entries do not count.

While a stage runs, another brief label can show a verified checkpoint or, after about one minute without one, confirm the current stage. Use waits short enough to post that update. Use counts only when observed. Label active work, waiting for the User and blocked work accurately.

When the User needs to decide or act, explain the situation, available options and relevant consequences. Answer requests for detail. Return to the short stage labels when work resumes. State the outcome briefly at completion. Routine checks and successful notification receipts belong in the work records. Surface failures in the chat when they affect the result or require action. Keep internal agent handoffs complete.

## Frame and approve

Read applicable records and reuse an existing Card, Specification, Batch or handoff. Without a board, route approved adoption through [installation](../setup/install.md).

- Use a **Card** for a small, self-contained outcome with a clear check. Keep one KR Developer responsible for implementation, focused verification and authorized publication. Reuse results when the checked revision and inputs are unchanged.
- Draft a **Specification** when the expected behavior or acceptance criteria need agreement. Use a **Batch** to execute an approved Specification or coordinate a formal delivery with acceptance on an exact candidate.
- If the User asks for a Specification or Batch for a small, clear change, explain in one line why a Card fits and propose it. If the request leaves behavior to agree or requires formal acceptance, explain the need for a Specification or Batch before starting. Keep suggestions outside approved scope.

Before execution show outcome, exact scope, checks and Git target: project-permitted main or isolated branch for a Card, dedicated branch for a Batch. Obtain explicit scope approval and start authority; one answer to a concrete proposal can grant both. Draft/review requests do not authorize implementation. If “continue” is ambiguous in a Specification discussion, clarify the action. For shorthand with inferred scope/revision/branch, restate those as a question and wait; for a simulation, ask and stop. Reuse already explicit authority for the same work. Corrections restore approved behavior; material scope changes need approval.

## Give the KR Developer the handoff

For a Batch, Writer records exact approved Specifications, approval/execution authority, ordered mission and ready status; Developer creates/verifies the Git approval snapshot. For standalone work hand off the existing Card ID; Developer can create one in its direct workflow.

Send one complete handoff: project/path and rules; authorized Git target/isolation; Card/Batch and exact outcome/scope/checks; User authority and next permitted step; separate publication/deployment permission if required; owner/branch/checkpoint/blocker; original chat application/reference for notifications. Require exact revision, checks/results and gaps on return.

Use native delegation allowed by host/role enforcement. Claude uses the installed named `developer` agent when available; Codex assigns Developer and `kr-developer` explicitly. A general child must read `AGENTS.md`, shared rules and `orchestrator/roles/developer.md`. Never elevate privileges to force a fallback. Retain the live native handle and checkpoint.

Developer checks eligibility, ownership, WIP and Git before deliverable edits; Batch pickup uses its exclusive lock and verified approval commit, Card pickup the board checks. Unavailable/prohibited/failed delegation leaves an observed blocker and actionable handoff in this chat, not permission for Orchestrator implementation.

## Run independent work within one assignment

Identify inputs, dependencies, exact baseline and one owning Developer. Start useful independent bounded helpers when the authorized host supports them and saved time exceeds coordination cost. Keep product/Card writes, integration and publication with the owner; helpers do not pick up other Cards or publish. Give each the role limits, start prerequisites and required evidence. Use separate scratch fixtures for checks that write.

After a candidate exists, parallel checks may run against that exact revision. Wait for all required results; stale evidence cannot satisfy a check invalidated by changed inputs. Reconcile results and rerun only affected checks. If one piece blocks, continue independent authorized work; report what decision/prerequisite is missing. With no useful overlap or unavailable delegation, proceed sequentially under the same authority and WIP.

## Continue, recover and notify

Advance authorized steps. Keep decisions in the original chat; ask the concrete question before waiting and send the answer to the same Developer. Record changed scope before implementing it. Developer maintains the Card/Batch/journal checkpoint and exact evidence; reconcile records with the live child/worktree on resume. Repeat start requests reuse the existing handoff. Before replacing a lost child, establish whether it still owns work from native status and recorded owner/worktree; unresolved ownership remains a blocker.

Coordinate one sender, ordinarily Developer, using [notification rules](notify-user.md). Supply real host/title if known, language, reference, summary and explicit next action; retain the same task/event ID for retries. Do not send both parent/child copies. An alert changes no permission; all decisions stay in this chat.

## Acceptance and review

For a delivered Batch, invoke a distinct Tester with approved scope, exact revision, reproducible startup, isolated fixture, required scenarios and prior evidence. For standalone work use separate Tester only when the project requires it. Claude uses named `tester`; Codex explicitly assigns Tester and `kr-tester`; general children require host/role permission.

Relay each Tester human question/startup steps in this chat and return the User's case verdict. Preserve observations against the tested revision. Review evidence against approved scope; send missing/mismatched results to Developer under applicable authority. Test results are distinct from User acceptance.

For a Batch obtain and record the User's explicit delivery decision after required cases resolve, then delegate closure under [Batch rules](../guidelines/batches.md). Standalone closure follows the project's existing acceptance/delivery rules, without an invented extra gate. If production has separate authorization, prepare exact candidate, checks, gaps and deployment/rollback information before routing the request to that authority. After verified closure propose the next eligible work, but obtain start authority before beginning it.
