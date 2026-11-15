# Understand the framework

Kanban Rememory gives AI agents a shared working method and a project memory kept beside the code. You describe the result you want and make product decisions. The agents turn those decisions into organized work and preserve the evidence needed to review it or resume later.

## Who does what

You explain the need, decide scope and acceptance, and authorize work. One agent carries the Card through implementation, automated checks and authorized publication.

## What the records mean

A **Card** holds the outcome, decisions, dependencies and delivery evidence. Its module's Kanban shows its state. Cards without a natural owner go to `misc`. A Card can link to attachments and existing repository files.

**Rememory** is the project journal for shared decisions and verified milestones. It links to Cards for delivery details.

**Specifications and Batches** are historical records of earlier deliveries. Their resources and approval evidence stay at their recorded locations.

## Telegram alerts

If you enable Telegram, the agent alerts you in two cases only: **Intervention needed**, as soon as it needs a decision, an answer or an action from you, and **Task completed**, once the outcome you asked for is verified. It sends no progress updates and no reminders. Each alert names the project, the task and the chat to return to. Confirmed alerts are tracked to avoid duplicate sends. The chat stays where you answer and decide: a reply in Telegram changes nothing. If Telegram is off or a message was certainly not sent, the agent says so in the chat. If delivery is uncertain, it reports that uncertainty and checks before any retry.

## Reading progress

The Card's folder identifies its stage. The core stages are Backlog, Development, Completion and Cancellation. A project can add stages when they represent real work or waiting, such as a separate review. Inside a stage, a Card can be progressing, waiting or blocked.

The work-in-progress limit keeps the agent from starting more work than the project can finish. Blocked work remains visible and still counts toward that limit. Completion means the required checks and evidence have been recorded. Cancellation means the task was explicitly abandoned, with its reason retained.

## Understanding the limits of autonomy

Agents can organize and execute authorized work. They ask when the expected behavior is ambiguous, a scope change is needed, or a decision belongs to you. The affected task waits while independent authorized work can continue within the capacity limit.

The repository provides instructions, memory and tools. An agent session performs the work. Adding the framework to a repository starts no background service.

Next: [start a project](start-a-project.md), or read the [guiding principles](lean-specifications.md).
