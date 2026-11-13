# Actor: User

## Role

Owner of the project and final decision-maker. The User works jointly with Specification Agent on the "what" and is notified by Development Agent when something needs attention.

## Responsibilities

- Review ready Specifications and approve the exact revisions when approving Batch scope.
- Define the scope of the next batch together with Specification Agent.
- Run the UAT, guided by Specification Agent: choose OK or KO for each step and add an optional comment.
- Decide to validate or reject the deployment after reading the report.
- Answer Development Agent when it is blocked or needs an intervention.

## Decisions that belong to the User alone

- Approving the scope of a batch.
- Validating or rejecting a batch.
- Approving changes to the workflow and role definitions.

## What the User does not do

- Write code or run git commands.
- Edit batch files by hand: Specification Agent and Development Agent maintain them.

## Interfaces

| With | Channel |
|---|---|
| Specification Agent | Conversation (specs, scope, UAT run, report, decision) |
| Development Agent | Telegram notifications, VS Code session |
| Obsidian vault | Control point: a read-only view on the local project folder |

## Availability

A batch waits in `delivered` until the User runs the UAT and decides. A new Batch can start after closure. Queued standalone tasks become eligible at delivery.

## Debt and delivery decisions

Use the procedure under “Record debt and resume acceptance” in `docs/batches/start-and-close-batches.md` to review defects and outstanding tests. When a blocking defect remains, request correction in the open Batch or reject the delivery. Accept only after required tests pass and explicitly decide whether to defer any remaining nonblocking defects.
