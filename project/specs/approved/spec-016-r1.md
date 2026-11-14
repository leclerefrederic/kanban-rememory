---
type: specification
id: "SPEC-016"
revision: "1"
---
# Hand off approved development work from the same chat

## Expected outcome

The user can frame a standalone Card or a Batch in Codex or Claude Code, approve what will be done and ask for development to start in one message. The session delegates to a Development Agent and returns its result in the same chat. The user makes scope and acceptance decisions without directing each workflow step.

## Scope

- The KR Orchestrator proposes a Card when the outcome and its checks are clear. It drafts a Specification when an unresolved decision about behavior or scope would change what ships or how it is accepted. If a single detail can settle the question, ask it and continue with the appropriate record. Reuse existing records. Decide separately whether Specifications need a shared Batch candidate and acceptance decision.
- Show the outcome, scope, checks and proposed Git target before execution. A response such as “Approved, start development” explicitly authorizes both the displayed scope and delegation. A request to draft, revise or review stays in preparation. Existing publication permissions and Batch acceptance requirements still apply.
- Use the host's subagent mechanism where available and authorized. The main chat handles specifications and user decisions. The Development Agent owns Cards, implementation, technical checks and Git. For a standalone Card, the Development Agent creates or updates the Card from the approved handoff. For a Batch, the Specification Agent prepares the scope and records the user's approval before the Development Agent performs its pickup checks.
- Both routes use the same handoff: the approved outcome and checks, the Card or Batch reference (or the agreed Card description if it has yet to be created), relevant project rules, Git target and authorized next action. In either route the developer verifies eligibility and work in progress before changing files.
- A standalone Card follows the repository's rules for work on main or an isolated branch. Choose an isolated branch when needed to preserve concurrent work. A Batch uses its designated branch for the candidate and waits for the user's verdict before final integration.
- The developer proceeds through routine steps on its own. If a decision blocks work, the same chat surfaces the question, its impact and any work that can proceed. The user's reply supplies the next handoff without requiring a new chat or a restatement of the scope. Retries and repeated requests reuse the existing handoff or run rather than launching duplicate development.
- The KR Orchestrator checks the delivered revision and evidence against the approved scope. It records conformity or sends missing checks and discrepancies back to Development. The final result identifies what changed, the checks run, the revision and what the user still needs to decide or verify. Use existing notification rules if Remy is configured. If the host cannot delegate or the safeguards prevent pickup, explain the actual blocker and leave the approved handoff usable by a Development Agent.
- This workflow runs from a work session. It requires no KR app, scheduler or Terminal window automation.

## Confirm what the user wants to start

Every Batch development run and every standalone change requires explicit user approval of the identified scope and authorization to start. The user can give both in one message when replying to a concrete proposal. Approval of a Specification or of Batch preparation alone does not authorize development. Record the exact approved Card scope or list of Specification revisions, the Batch scope where applicable, and the agreed Git target. Return any material scope change to the user for approval. Under an existing execution authorization, route a correction that restores the approved behavior back to Development using the applicable correction procedure.

- An ambiguous instruction such as “Continue with the next step” prompts a targeted question. Offer the applicable options, such as drafting another Specification, preparing a Batch for review, or approving the proposed scope and starting development. Wait for the answer before taking any of those paths.
- A shorthand instruction such as “Start dev on 16” identifies a likely intent. Restate it as a question covering the exact Specification revision, the Batch scope, preparation, delegation on the dedicated branch and the return for testing and user acceptance. Wait for the user to confirm when those steps and scope were inferred rather than already explicitly agreed.
- Once the user has explicitly approved the scope and authorized starting, record the decision and proceed through the agreed steps without further routine confirmations. Integration and any deployment follow the applicable project rules.
- For a simulation, ask the same question as a rehearsal and stop there.

## Production authorization

Assignment, acceptance and production authorization are separate decisions. The Development Agent supplies the tested revision, verification evidence and any deployment or rollback information required by the project. The KR Orchestrator routes the request to the project's designated change authority (for example, a Change Advisory Board or an emergency change authority for a hotfix) when the project requires production approval. The authority's decision must cover the revision and target environment. Approval to develop or merge by itself does not grant permission to deploy.

If production approval is required and missing, present the evidence and the request to the user and report that deployment is waiting for approval. Once valid approval is recorded, hand off the deployment to the role authorized by the project. A project may designate its owner as the authority. This workflow does not require a separate board for projects that have no production approval gate.

## Keep the work moving

The session owns the workflow. After each milestone, it checks the recorded state, completes the next steps already authorized and brings the user only the choice that determines what happens next. Every question names the concrete options available and uses the context already agreed. It does not ask for a decision already given.

| Milestone | What the session does next |
| --- | --- |
| Specification approved | Offer to draft another Specification or prepare a Batch. If the user has already chosen a route, proceed with it. |
| Batch prepared | Present its proposed Specifications, mission order and checks. Ask whether to approve and start development or add another Specification. Update the existing proposal if scope changes. |
| Standalone change framed | Present the proposed Card and checks. Ask whether to approve and start development or adjust the scope. |
| Development authorized | Delegate and carry the work through routine steps. Ask only when an unresolved decision affects the work or a required authorization is missing. |
| Candidate delivered | Review scope and evidence. Route discrepancies to Development. If user acceptance is required, present the tested revision, guide the checks and record each result. |
| Acceptance checks complete | Present the evidence and ask for the delivery decision. Once it is recorded, hand off the authorized closure steps. |

## Cadence and recovery

- Keep the approved scope, Git target, latest known revision, blocker and next authorized action in the existing project records. On resumption, reconcile those records with the current work and check whether an execution already owns it. Continue from the last verified state without duplicating the assignment or requesting approval already recorded.
- Update the user when their intervention is needed, when a material change affects the expected outcome or next step, and when the work is ready for review or complete. Keep routine progress in the work records. When Telegram is configured, use Remy for the applicable existing intervention and delivery or completion events. Use one alert per event. Keep the request actionable in the original chat even if Telegram delivery fails.
- If the Orchestrator finds a standalone Card conforming, hand off closure when permitted by the project rules. Present a conforming Batch candidate for the user's acceptance. After closure, propose the next eligible work and obtain authorization before starting it.

## Acceptance criteria

Exercise the same workflow in Codex and Claude Code using a scratch project. Record the host and verify the real subagent invocation and its Git target.

1. Ask for a draft and then a review. No implementation starts. Approve the displayed scope and request development in one message. A Development Agent receives the handoff without separate instructions to create a Card, start work or run checks.
2. For a standalone Card, the developer creates or reuses the Card, works on the authorized Git target, verifies the change and reports the outcome in the same chat. Repeat with a project that requires a separate branch.
3. For a Batch, the developer uses the designated branch and delivers a tested candidate. The chat presents the exact revision for acceptance. Final integration requires the user's verdict and the applicable publication authorization.
4. Trigger a missing decision. The user answers in the same chat and work resumes with the approved context. Repeat the start request while work is active and verify that only one execution owns the work.
5. Exercise an unavailable subagent or a blocked pickup. The chat explains why work did not start and provides the handoff. Role boundaries and the project's work in progress limit are preserved.

6. Approve a Specification without asking for the next step. The session offers another Specification or Batch preparation. Choose Batch preparation. The session prepares the proposal and asks whether to approve it or add a Specification. Choose to add one and verify that no development starts. Then approve and authorize development in one message. The session delegates, guides acceptance after delivery and presents the delivery decision when checks are complete.

7. In a project that requires production approval, accept a tested candidate and verify that deployment waits for the designated authority. Record approval for that revision and environment, and verify that the authorized role can proceed. Repeat using the project's hotfix approval route.

8. Compare a bounded request with a request that leaves material behavior undecided. Route the first to a Card and the second to a Specification. On delivery, present evidence for a different revision and verify that the Orchestrator requests correction before presenting the candidate for acceptance.

9. During a Specification discussion, say “Continue with the next step.” Verify that the Orchestrator asks which path is intended and that no Batch is prepared or development started before the answer. Say “Start dev on 16” without prior agreement on the Batch scope. Verify that the Orchestrator asks for confirmation of the full proposed path and waits. Confirm it and verify that the recorded approval leads to delegation without another routine confirmation. Repeat as a simulation and verify that only the question is produced.

10. After approval, add a Specification to the proposed Batch. Verify that development of the changed scope waits for a new approval. Report a discrepancy within the original scope and verify that the correction follows the existing authorized route.
11. Interrupt the chat with development in progress, then resume in a new session. Verify that the session retrieves the recorded scope, revision and next action without creating a duplicate execution or asking for approval again.
12. With Remy configured, trigger an intervention twice for the same event. Verify that only one alert is sent and that the answer is given in the original chat. Simulate a Telegram failure and verify that the request remains actionable there.
13. Verify the closure route for a conforming standalone Card and the user acceptance route for a conforming Batch. After closure, verify that the next eligible work is proposed and awaits approval.

## Resources

- [Project working instructions](../../../agents/work-in-a-project.md) define role boundaries and the standalone flow.
- [Batch workflow](../../../agents/batches/batch-workflow.md) defines the Batch gates.
