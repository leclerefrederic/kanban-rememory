# Prepare Card content

Search the board for matching work first. Writer prepares/revises backlog scope and checks; Developer owns execution and stage moves. The User supplies requests/decisions through conversation and never maintains the file. Apply the [Kanban rules](../guidelines/kanban.md) and use the [board command](manage-board.md#create) with the [blank template](../templates/card.md).

A Card describes one executable outcome, including an investigation whose deliverable is a finding. Split independently verifiable work when useful. Keep detailed designs, logs and test outputs in linked evidence, not the Card. Exclude secrets and unnecessary personal data.

| Point | Required record |
| --- | --- |
| Intake | Stable ID/action title; owner; expected outcome; scope; dependencies or none; observable acceptance checks; relevant decisions/requirements. |
| Before start | Explicit execution authorization, prerequisites/capacity checked, actual start. |
| Active | State and next action; blocker date/cause/unblocking condition; revision and evidence at milestones. |
| Closure | Verified criteria, actual finish, exact revision/artifact and agreed delivery evidence, journal reference. |

The folder determines stage; state describes progress inside it. Use `waiting` for a normal queue and `blocked` for an impediment. Neither removes active work from WIP. Keep the original start through rework.

A standalone Card may leave YAML `batch: null` and `specifications: []`. Otherwise use stable IDs; a Batch-linked Specification must be selected by that Batch, and Developer references approved Specs only. Do not copy Card IDs into Batch records. See the [filled Card](../../documentation/examples/card.md) for evidence and authorization fields, rather than maintaining another worked example here.
