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

Describe who needs to achieve what and what gets in the way today. Relevant examples, screenshots or mockups help explain the outcome. The Specification Agent clarifies the request and records any attachments with their purpose. For a mockup, agree which aspects must be reproduced.

You review the proposed behavior and acceptance criteria. Suggestions remain suggestions until agreed. The Development Agent creates its own implementation Cards when authorized work is ready to be tracked.

Before work starts, you should be able to explain the expected result, the agreed scope, how it will be checked and what the agent is authorized to do. The agent should be able to recover those decisions from the project records.

## Resume an existing project

Ask the agent to recover the current state before starting new work. It reads the records and checks the repository. You should receive the current delivery or task, any blocker, the latest verified result and the next authorized action.

If an existing Batch is awaiting acceptance, that is the delivery to review. If a record conflicts with the actual files, the agent reports the discrepancy before proceeding. External edits can happen; they need to be reconciled with the approved baseline.

Next: [deliver a change](deliver-a-change.md).
