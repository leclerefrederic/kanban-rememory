# Assign a task

Tell your agent what you want to achieve in the project. You do not create a Card or choose its filename: Development Agent finds the relevant work, records the request and maintains its progress.

## Describe the result

Give the repository or relevant part of the project, the problem, the expected result and any constraints that matter. Add an example, screenshot or reference when it makes the request clearer. The agent uses the context already available and asks about missing decisions that affect the result.

For example:

> In this repository, fix the broken navigation links in the setup guide. Keep the instructions themselves unchanged. Check that every local link opens the intended section, then report the result. You can execute this task; use the project's existing publication permissions.

That request supplies an outcome, a boundary, a way to verify success and authorization to act. It does not ask you to write the tracking record.

## Make the intended next step clear

| You want to… | A useful way to ask |
| --- | --- |
| Explore an idea | “Compare the options and recommend an approach before implementation.” |
| Keep a request for later | “Record this in the backlog; do not start it yet.” |
| Start agreed work | “Execute this task within the agreed scope.” |
| Change priority | “Prioritize this request and tell me what it means for the work already in progress.” |

These are examples, not required wording. Existing authorization remains valid. Agreement about an outcome, permission to implement and permission to publish are distinct; one instruction can grant several together.

## How the agent organizes it

The agent checks for existing work before creating another record. A bounded standalone task can use a Card containing its outcome, scope and checks. If the request needs the project's Specification and Batch workflow, the agent prepares that scope with you before development. See [deliver a Batch](deliver-a-batch.md).

Only Development Agent writes and moves Cards. A Card can reference a Specification or Batch, but it remains independent. You can inspect the [Card example](examples/kanban-card.md) without maintaining one yourself.

Priority does not remove dependencies or the work-in-progress limit. If another Batch is active, a new request does not silently join its approved scope. The agent records it for later; standalone work waits until that Batch is delivered and must preserve its acceptance candidate.

## Follow progress and completion

Ask what has been verified, what is blocked and what comes next. A status request alone does not change scope or priorities. If work needs your decision, the agent explains the specific question and keeps the affected task visible.

At completion, expect the result, the checks actually run, any remaining limitation and the publication status. A completed standalone Card follows the project's agreed delivery rules. For Batch work, technical completion leads to [your acceptance tests and decision](test-and-accept-a-batch.md).

If a session ends before completion, use [resume work](resume-work.md). If you discover a problem with delivered behavior, use [report a defect](report-a-defect.md).
