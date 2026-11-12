# Actor: User

## Role

Owner of the project and final decision-maker. The User works jointly with Cowork on the "what" and is notified by Claude Code when something needs attention.

## Responsibilities

- Review and approve the specifications drafted by Cowork.
- Define the scope of the next lot together with Cowork.
- Run the UAT, guided by Cowork: choose OK or KO for each step and add an optional comment.
- Decide to validate or reject the deployment after reading the report.
- Answer Claude Code when it is blocked or needs an intervention.

## Decisions that belong to the User alone

- Approving the scope of a lot.
- Validating or rejecting a lot.
- Approving changes to the workflow and role definitions.

## What the User does not do

- Write code or run git commands.
- Edit lot files by hand: Cowork and Claude Code maintain them.

## Interfaces

| With | Channel |
|---|---|
| Cowork | Conversation (specs, scope, UAT run, report, decision) |
| Claude Code | Telegram notifications, VS Code session |
| Obsidian vault | Control point: a read-only view on the local project folder |

## Availability

A lot waits in `delivered` until the User runs the UAT and decides. A new Lot can start after closure. Queued standalone tasks become eligible at delivery.
