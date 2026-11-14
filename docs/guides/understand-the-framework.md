# Understand the framework

Kanban Rememory gives AI agents a shared working method and a project memory kept beside the code. You describe the result you want and make product decisions. The agents turn those decisions into organized work and preserve the evidence needed to review it or resume later.

## Who does what

| Participant | Responsibility |
| --- | --- |
| You | Explain needs and priorities, agree on scope, authorize work, try the delivered result, and decide whether to accept it. |
| Specification Agent | Clarify the need with you, write Specifications, prepare Batches and acceptance scenarios, record your verdicts, and maintain the delivery report. |
| Development Agent | Implement authorized work, maintain Cards, run technical checks, prepare delivery candidates, and perform authorized Git operations. |

These are responsibilities, independent of the AI vendor. One AI can perform both agent roles at different stages. The distinction keeps the expected behavior, implementation and acceptance decision clear.

Only the Development Agent creates, writes, moves, and closes Cards. You can inspect the board, ask about a task, or change its priority through conversation. The agent records your request and checks its effect on current work.

## What the records mean

A **Specification** describes an outcome, the agreed behavior and how to check it. It can refer to a mockup or another resource. A draft is still being prepared; a ready Specification can be proposed for approval; an approved revision records the exact scope selected for a Batch. Changes to approved behavior require a new revision and agreement.

A **Batch** is a delivery agreement covering one or more approved Specifications. It records priorities, tests and a report. Its approved scope stays fixed during execution. A new idea can be recorded for later work without expanding the active delivery.

A **Card** records an executable task and its completion evidence. Cards can refer to a Specification or Batch, but remain independent: a Batch groups Specifications, not Cards. A standalone task can have a Card without a Batch.

**Tests and reports** distinguish what was expected, what was observed, which revision was tested and what you decided. They also preserve defects, screenshots and tests still owed. Automated tests stay with the product code; acceptance records explain the delivery you reviewed.

**Rememory** is the concise project journal: decisions, verified milestones and the next action. Git preserves file history. Together, they allow another agent session to recover both the current state and the reasons behind it.

## Reading progress

The Card's folder identifies its stage. The core stages are Backlog, Development, Completion and Cancellation. A project can add stages when they represent real work or waiting, such as a separate review. Inside a stage, a Card can be progressing, waiting or blocked.

The work-in-progress limit keeps the agent from starting more work than the project can finish. Blocked work remains visible and still counts toward that limit. Completion means the required checks and evidence have been recorded. Cancellation means the task was explicitly abandoned, with its reason retained.

## Understanding the limits of autonomy

Agents can organize and execute authorized work. They ask when the expected behavior is ambiguous, a scope change is needed, or a decision belongs to you. The affected task waits while independent authorized work can continue within the capacity limit.

The repository provides instructions, memory and tools. An agent session performs the work. Automatic dispatch of Batches still needs implementation; having these files in a repository does not itself start a background development service.

Next: [start a project](start-a-project.md), or read the [guiding principles](lean-specifications.md).
