# Orchestrate work from the current chat

The [KR Orchestrator role](roles/orchestrator.md) owns the conversation and sequencing. It follows [KR Writer duties](roles/specification-agent.md) and delegates [KR Developer duties](roles/development-agent.md). It may prepare backlog Cards within KR Writer limits. It delegates execution, stage changes, implementation and Git. If the project requires evidence outside its role, ask the KR Developer for that evidence. The [shared instructions](work-in-a-project.md) and project permissions apply to both.

## Frame and approve

Read the applicable project records first. Reuse an existing record or handoff if it describes the request.

- Propose a standalone Card when the outcome and checks are clear. Prepare or revise the proposed scope and verification in the backlog Card, then present it for approval. Ask one targeted question if a missing detail can make the proposed work executable.
- Draft or revise a Specification when a decision about scope or behavior would change what ships or how it is accepted. Keep suggestions outside agreed scope. After the user approves a Specification, offer to draft another or prepare a Batch if no direction is already recorded.
- Propose a Batch when Specifications need a shared candidate and acceptance decision. Show the exact revisions, mission order, constraints and checks. Ask whether to approve and start or add another Specification. When the Batch module is installed, the `agents/batches/batch-workflow.md` owns the record states and the `agents/batches/start-and-close-batches.md` owns pickup and closure.

Before execution, show the outcome, exact scope, checks and proposed Git target. For a Card, use main or an isolated branch as the project permits. Use isolation to protect concurrent work when needed. Propose a dedicated branch for a Batch. Get explicit approval of scope and authorization to start. One answer to the concrete proposal can grant both. A request to draft or review, or to prepare a Batch, does not by itself authorize development.

If the user says “Continue with the next step” in a Specification discussion, ask which action they mean, such as another Specification, Batch preparation or approval and development of the proposed scope. With shorthand such as “Start dev on 16,” restate the exact revision, proposed scope, preparation, branch and delegated development, review and acceptance as a question. Wait if those details were inferred. If the user's instruction is a simulation, give the question and stop. If the proposal was already explicit and the user authorizes it, record the decision and proceed. Material scope changes need new approval. For a correction restoring approved behavior, use the existing authorization and the applicable correction procedure.

## Give the KR Developer the handoff

For a Batch, record the exact approved revisions, scope, approval and execution authorization in the Batch records and set `ready` only after approval. The KR Developer makes and verifies the Git approval snapshot. For standalone work, pass the prepared Card ID so KR Developer picks up the same Card. The direct KR Developer workflow can still create a Card from the approved handoff.

Send the following in one handoff:

- Project path and applicable project rules, including the authorized Git target and isolation requirement.
- Card or Batch reference, exact approved outcome and scope, Specification revisions where applicable, and the checks.
- The user's authorization and the next permitted action. State any separate approval needed for publication, integration or deployment.
- Known owner, branch and checkpoint, any open blocker, and the original chat reference to use in notifications. Request the exact revision, executed checks, outcomes and gaps on return.

Use the host's native subagent command or tool within the approved session. In Claude Code use the Agent tool with the project's KR Developer definition if installed. The kit provides the definition through the optional `agents/configure-claude-role-hook.md`. In Codex use the available subagent mechanism and explicitly assign the KR Developer role and its `kr-developer` skill. When using a general subagent, tell it to read `AGENTS.md`, `agents/work-in-a-project.md` and `agents/roles/development-agent.md` before acting. Use that route only if the project's role enforcement and the host permit it. Never elevate privileges to obtain a fallback.

The KR Developer checks eligibility, existing ownership, work in progress and Git state before any implementation changes. Its first response identifies the role, current state and target. For a Batch it uses the existing exclusive pickup lock and a verified approval commit. For a Card it uses the board commands and their existing work in progress checks. Retain the returned native agent handle with the handoff while it is live. If delegation is unavailable, prohibited or fails to start, state the observed blocker and give the actionable handoff in the chat. If pickup is blocked, preserve the handoff and state what must change before retrying.

## Continue, recover and notify

The Orchestrator completes authorized steps and asks for the next decision at each milestone. When a decision blocks development, ask the concrete question in the original conversation, say what depends on it and let independent authorized work continue. Send the answer back to the same KR Developer when reachable. If the scope changes, get new approval first.

Ask the KR Developer to keep the approved scope, Git target, known revision, owner, blocker and next authorized action in the existing Card or Batch records and Rememory according to role. On resume, reconcile that checkpoint with the child and the actual work through the KR Developer. Repeated start requests use the existing handoff. Before replacing a lost subagent, establish whether it still owns the work using the saved owner, recorded worktree or state, and native status when available. If ownership cannot be resolved, preserve the handoff and report that blocker. Resume a stopped execution from the last verified state on the same assignment. Reuse recorded authorization when it still covers the next action.

Update the chat after material changes, on intervention and at delivery or completion. Keep routine progress in the work records. When Telegram is configured, coordinate one sender for the applicable event, ordinarily the KR Developer. Use the existing `agents/configure-telegram.md`, stable event ID and original wording for retries so an alert from the Orchestrator and child cannot count as separate events. For Batch delivery use the existing delivery event and exact tested revision. Keep the question in the original chat and the decision there even when delivery fails. Follow the existing retry rules for uncertain sends.

## Hand off to KR Tester and review

After a conforming delivery, invoke a distinct KR Tester with the approved scope, exact delivered revision, reproducible startup instructions, scratch fixture, required cases and evidence already recorded. For an authorized standalone change, use this handoff only when the project requires separate acceptance. In Claude Code use the named `tester` agent when installed. In Codex assign the [KR Tester role](roles/tester.md) to a native subagent and give it the `kr-tester` skill. Use a general child only if the host and role rules allow it. Explicit assignments prevail over project startup defaults.

Send a Tester question and its startup steps to the original chat, return the User's case verdict to the Tester, and preserve its evidence against the exact candidate. Once the required cases are resolved, review gaps and obtain the User's delivery decision. A test result alone cannot authorize closure.

Compare the returned evidence and revision to the approved scope and checks. Send missing or mismatched evidence and discrepancies back to the KR Developer under applicable authorization. Record conformity and distinguish technical checks from the user's verdict. Present the result, executed checks, revision, gaps and next decision in the original chat.

- For a conforming standalone Card, hand off closure to Development when the project permits it.
- For a conforming Batch candidate, coordinate the KR Tester handoff, present the recorded evidence and obtain and record the explicit verdict before delegating closure. Publication and final integration follow the existing Batch rules.
- If the project separately requires production authorization, assemble the tested revision, verification evidence and any required deployment and rollback information. Route the request to the project's designated authority for the target environment, including its hotfix route where applicable. Report that deployment is waiting until approval is recorded for that revision and environment, then hand off to the authorized role.
- After closure, identify and propose the next eligible work. Obtain authorization before starting it.
