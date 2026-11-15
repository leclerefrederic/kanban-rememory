# Understand the framework

Kanban Rememory gives AI agents a shared working method and a project memory kept beside the code. You describe the result you want and make product decisions. The agents turn those decisions into organized work and preserve the evidence needed to review it or resume later.

## Who does what

| Participant | Responsibility |
| --- | --- |
| You | Explain needs and priorities, agree on scope, authorize work, try the delivered result, and decide whether to accept it. |
| KR Orchestrator | Keep work and decisions in the same chat, delegate approved implementation and coordinate acceptance. |
| KR Writer | Clarify the need, write Specifications and backlog Cards, and prepare Batches and acceptance criteria. |
| KR Developer | Implement authorized work, maintain Card execution records, run technical checks and perform authorized Git operations. |
| KR Tester | Run and guide acceptance for the exact delivered candidate and return the evidence for your verdict. |

These are responsibilities, independent of the AI vendor. Roles apply independently to the primary session and its assigned agents. The distinction keeps the expected behavior, implementation and acceptance decision clear.

Each agent reads and writes only what its role needs. KR Writer prepares backlog Cards. KR Developer owns stage changes, implementation, Rememory and Git. KR Tester owns acceptance evidence, including the case answers you give it. You retain the final delivery decision. You can inspect the board, ask about a task, or change its priority through conversation. The agent records your request and checks its effect on current work.

## What the records mean

A **Specification** describes an outcome, the agreed behavior and how to check it. It can refer to a mockup or another resource. A draft is still being prepared; a ready Specification can be proposed for approval; an approved revision records the exact scope selected for a Batch. Changes to approved behavior require a new revision and agreement.

A **Batch** is a delivery agreement covering one or more approved Specifications. It records priorities, tests and a report. Its approved scope stays fixed during execution. A new idea can be recorded for later work without expanding the active delivery.

A **Card** records an executable task and its completion evidence. Cards can refer to a Specification or Batch, but remain independent: a Batch groups Specifications, not Cards. A standalone task can have a Card without a Batch.

**Tests and reports** distinguish what was expected, what was observed, which revision was tested and what you decided. They also preserve defects, screenshots and tests still owed. Automated tests stay with the product code; acceptance records explain the delivery you reviewed.

**Rememory** is the concise project journal: decisions, verified milestones and the next action. Git preserves file history. Together, they allow another agent session to recover both the current state and the reasons behind it.

## Telegram alerts

If you enable Telegram, the KR Developer alerts you in two cases only: **Intervention needed**, as soon as it needs a decision, an answer or an action from you, and **Task completed**, once the outcome you asked for is verified. It sends no progress updates and no reminders. Each alert names the project, the task and the chat to return to, and appears once. The chat stays where you answer and decide: a reply in Telegram changes nothing. If Telegram is off or a send fails, the request or result stays in the chat and the agent says that no alert was sent.

## Reading progress

The Card's folder identifies its stage. The core stages are Backlog, Development, Completion and Cancellation. A project can add stages when they represent real work or waiting, such as a separate review. Inside a stage, a Card can be progressing, waiting or blocked.

The work-in-progress limit keeps the agent from starting more work than the project can finish. Blocked work remains visible and still counts toward that limit. Completion means the required checks and evidence have been recorded. Cancellation means the task was explicitly abandoned, with its reason retained.

## Understanding the limits of autonomy

Agents can organize and execute authorized work. They ask when the expected behavior is ambiguous, a scope change is needed, or a decision belongs to you. The affected task waits while independent authorized work can continue within the capacity limit.

The repository provides instructions, memory and tools. An agent session performs the work. Automatic dispatch of Batches still needs implementation; having these files in a repository does not itself start a background development service.

Next: [start a project](start-a-project.md), or read the [guiding principles](lean-specifications.md).
