# Actor: User

## Role

Owner of the project and final decision-maker. The User works jointly with Specification Agent on the "what" and is notified by Development Agent when something needs attention.

## Responsibilities

- Review ready Specifications using the [Lean Specifications approval test](../../lean-specifications.md#the-approval-test) and approve the exact revisions when approving Batch scope.
- Define the scope of the next batch together with Specification Agent.
- Run acceptance tests guided by Specification Agent: choose OK or KO for each case. For a KO, explain what happened and supply a screenshot or state that it is unavailable.
- Decide to accept or reject the tested delivery after reading the report.
- Answer Development Agent when it is blocked or needs an intervention.

## Decisions that belong to the User alone

- Approving the scope of a batch.
- Validating or rejecting a batch.
- Approving changes to the workflow and role definitions.

## Work delegated to agents

- The User communicates requests and decisions; only the AI Development Agent creates, writes, moves, and closes Cards. The User can inspect the board and request changes through conversation.
- Agents implement the code, maintain project records according to their roles, and perform authorized Git operations. If external edits occur, check them against the approved baseline before work resumes.

## Interfaces

| With | Channel |
|---|---|
| Specification Agent | Conversation (specs, scope, acceptance tests, report, decision) |
| Development Agent | The project's chosen agent session; optional configured notifications |

No particular editor or document viewer is required. Personal tools for viewing the repository are outside the framework's workflow.

## Availability

A batch waits in `delivered` until the User runs acceptance tests and decides. A new Batch can start after closure. Queued standalone tasks become eligible at delivery.

## Debt and delivery decisions

Use the procedure under “Record debt and resume acceptance” in `docs/batches/start-and-close-batches.md` to review defects and outstanding tests. When a blocking defect remains, request correction in the open Batch or reject the delivery. Accept only after required tests pass and explicitly decide whether to defer any remaining nonblocking defects.
