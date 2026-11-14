# Deliver a Batch

This guide describes a delivery using Specifications and a Batch. For standalone work, see [Assign a task](assign-a-task.md): its outcome and checks live directly on a Card maintained by Development Agent, under the project's agreed delivery rules.

## From a request to an approved scope

You explain the desired outcome to the Specification Agent. It writes the Specification and prepares observable acceptance criteria. You can clarify or revise the proposal while it is being prepared.

A Batch selects one or more exact Specification revisions and records their priority. You approve that scope and authorize execution. Once approved, the Batch baseline stays fixed. Correcting an implementation restores agreed behavior; changing that behavior requires a new approved Specification revision and a delivery plan that preserves the active baseline.

The mission order expresses priority. Development Agent may adjust the technical execution order to respect dependencies in the code.

## During development

Development Agent organizes the work into its own Cards, implements the changes and runs applicable checks. It records progress, decisions and blockers. You can ask for status without having to maintain those records yourself.

An unclear requirement produces a question. A blocking dependency remains visible. A new request is recorded for later work rather than silently added to the approved scope. Standalone requests wait until the active Batch is delivered and must preserve the candidate under acceptance.

## What each Batch state means

| State | Meaning for you |
| --- | --- |
| Draft | The delivery is being prepared and can still be discussed. |
| Ready | Scope is approved and the delivery is eligible for authorized pickup. |
| In progress | Development Agent is implementing or correcting the approved behavior. |
| Delivered | A specific candidate is available for acceptance; this is not yet an accepted delivery. |
| Validated | You explicitly accepted the tested revision after the required checks passed. |
| Rejected | You explicitly rejected the tested revision. |
| Closed | The agent completed the relevant Git and record-preservation procedure and verified publication. |

A delivered Batch can return to development for an authorized correction of a blocking defect. It then produces a new candidate for acceptance. A closed Batch stays closed.

## Review the delivery

Specification Agent guides you through the prepared tests. Development Agent identifies the candidate, environment and technical evidence. You give the verdict for each case; the agent records it and guides the next one.

A failed case may leave other cases runnable. A blocking defect prevents acceptance and triggers correction or a rejection decision. See [Test and accept a Batch](test-and-accept-a-batch.md) for the detailed rules.

## Accept or reject

Acceptance applies to the revision you tested. Required scenarios must pass and blocking debt must be resolved. Any nonblocking debt being deferred needs an explicit decision. Development Agent then merges the tested work and completes closure under the project's Git permissions.

On rejection, the candidate code and its automated tests are archived. A separate closing record preserves the Specifications, findings, debt and outstanding acceptance tests without adding rejected implementation to the accepted baseline. The previous main history is preserved.

Unchanged approved Specifications can be selected again for another Batch. Their earlier defects and outstanding tests remain relevant: a successor carries those obligations forward. A rejected delivery is therefore still useful evidence for the next attempt.

## Interruptions and handoffs

An interrupted session resumes the existing work and evidence. An interrupted closure is completed before a new Batch starts. Earlier test results remain tied to their original candidate; they are not silently transferred to changed code.

You should be able to ask what is approved, what is running, what has been verified and what decision comes next. The agent uses the project records to answer. [Resume work](resume-work.md) explains what to expect after a break or a change of agent.
