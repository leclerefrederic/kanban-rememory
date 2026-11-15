# Assign a task

Tell your agent what you want to achieve in the project. The agent creates the Card in the owning module's Kanban and follows it through delivery.

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

The agent looks for an existing Card, checks dependencies and records the agreed scope. Work that has no natural module owner belongs in `misc`. A Card can include repository attachments and link to related Cards.

## Follow progress and completion

Once authorized, the agent updates the Card, carries out the work, resolves issues within scope, runs the applicable automated checks and completes the agreed delivery. It hands control back when it needs a decision or action only you can provide, or when the work is complete. The project's Rememory links published milestones to the relevant Cards.

Before merging into `main`, the agent asks you to approve the verified revision and tells you if merging or pushing will trigger an automatic production deployment. After your approval it finishes the authorized delivery.

If a session ends before completion, use [resume work](resume-work.md). If you discover a problem with delivered behavior, use [report a defect](report-a-defect.md).
