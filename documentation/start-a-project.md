# Start a project

Begin by telling your agent which repository you want to use and that you want to adopt Kanban Rememory. The agent handles the installation and configuration. Your part is to describe how you want work to move and agree on the resulting setup.

## Choose the modules

Name the modules you want to track. Each has a Kanban. The `misc` module holds Cards without a natural owner and can be enough for a small project. Project settings and the shared workflow live in `project/settings.json`. The journal lives in `project/rememory/`.

## Agree on the workflow

The agent offers short, standard and long starting workflows, or helps define a custom one. Choose according to the work you actually do. A separate review or deployment stage is useful when it represents a distinct activity or queue that you need to see.

Agree on the work-in-progress limit, who authorizes execution, how priorities and dependencies are handled, and what counts as a completed task. Also establish Git permissions: permission to develop, accept a delivery and publish are distinct decisions. An explicit instruction can grant several permissions together, and recorded standing permissions remain usable.

The agent presents the setup for approval, applies it and checks that it is consistent. You do not need to create stage directories or write Cards yourself.

## Give the first request

Describe who needs to achieve what and what gets in the way today. Relevant examples, screenshots or mockups help explain the outcome. Your agent clarifies the request, links useful resources from the Card and carries the agreed work through delivery. You review scope and acceptance criteria and authorize execution.

Before work starts, you should be able to explain the expected result, the agreed scope, how it will be checked and what the agent is authorized to do. The agent should be able to recover those decisions from the project records. [Assign a task](assign-a-task.md) shows how to phrase the request and follow its progress.

## Resume an existing project

If the repository already uses Kanban Rememory, follow [Resume work](resume-work.md). The agent recovers the existing records and next authorized action instead of repeating setup.

Next, [assign a task](assign-a-task.md).
