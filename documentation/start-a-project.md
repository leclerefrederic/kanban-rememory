# Start a project

Begin by telling your agent which repository you want to use and that you want to adopt Kanban Rememory. The agent handles the installation and configuration. Your part is to describe how you want work to move and agree on the resulting setup.

## Agree on the workflow

The agent offers short, standard and long starting workflows, or helps define a custom one. Choose according to the work you actually do. A separate review or deployment stage is useful when it represents a distinct activity or queue that you need to see.

Agree on the work-in-progress limit, who authorizes execution, how priorities and dependencies are handled, and what counts as a completed task. Also establish Git permissions: permission to develop, accept a delivery and publish are distinct decisions. An explicit instruction can grant several permissions together, and recorded standing permissions remain usable.

The agent presents the setup for approval, applies it and checks that it is consistent. You do not need to create stage directories or write Cards yourself.

## Choose the amount of structure you need

Cards and Rememory are the basic workflow. They give an agent a task record, evidence and a handoff for standalone work.

The optional Specification and Batch workflow adds an explicit agreement about a delivery and its acceptance. Use it when you want to review the intended behavior before development and decide on a complete delivery afterward. The agent helps you choose the appropriate approach for the request.

## Give the first request

Describe who needs to achieve what and what gets in the way today. Relevant examples, screenshots or mockups help explain the outcome. Your agent clarifies the request and uses the agreed standalone or Batch workflow. When a Specification is needed, Specification Agent records attachments with their purpose; for a mockup, agree which aspects must be reproduced.

You review the proposed behavior and acceptance criteria. Suggestions remain suggestions until agreed. The Development Agent creates its own implementation Cards when authorized work is ready to be tracked.

Before work starts, you should be able to explain the expected result, the agreed scope, how it will be checked and what the agent is authorized to do. The agent should be able to recover those decisions from the project records. [Assign a task](assign-a-task.md) shows how to phrase the request and follow its progress.

## Resume an existing project

If the repository already uses Kanban Rememory, follow [Resume work](resume-work.md). The agent recovers the existing records and next authorized action instead of repeating setup.

Next: [assign a task](assign-a-task.md), or [deliver a Batch](deliver-a-batch.md) when you need an agreed delivery scope.
