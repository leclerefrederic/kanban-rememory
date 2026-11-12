# Actor: User

## Role

Owner of the project and final decision-maker. The User works jointly with Specification Agent on the "what" and is notified by Development Agent when something needs attention.

## Responsibilities

- Review and approve the specifications drafted by Specification Agent.
- Define the scope of the next lot together with Specification Agent.
- Run the UAT, guided by Specification Agent: choose OK or KO for each step and add an optional comment.
- Decide to validate or reject the deployment after reading the report.
- Answer Development Agent when it is blocked or needs an intervention.

## Decisions that belong to the User alone

- Approving the scope of a lot.
- Validating or rejecting a lot.
- Approving changes to the workflow and role definitions.

## What the User does not do

- Write code or run git commands.
- Edit lot files by hand: Specification Agent and Development Agent maintain them.

## Interfaces

| With | Channel |
|---|---|
| Specification Agent | Conversation (specs, scope, UAT run, report, decision) |
| Development Agent | Telegram notifications, VS Code session |
| Obsidian vault | Control point: a read-only view on the local project folder |

## Availability

A lot waits in `delivered` until the User runs the UAT and decides. A new Lot can start after closure. Queued standalone tasks become eligible at delivery.
