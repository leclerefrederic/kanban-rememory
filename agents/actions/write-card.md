# Prepare Card content

Search the board for matching work first. The agent maintains the Card throughout delivery. The User supplies requests and decisions in conversation. Apply the [Kanban rules](../guidelines/kanban.md) and use the [board command](manage-board.md#create) with the [blank template](../templates/card.md).

A Card describes one executable outcome, including an investigation whose deliverable is a finding. Split independently verifiable work when useful. Keep detailed designs, logs and test outputs in linked evidence, not the Card. Exclude secrets and unnecessary personal data.

| Point | Required record |
| --- | --- |
| Intake | Stable ID/action title; `module`; owner; expected outcome; scope; dependencies or none; observable acceptance checks; relevant decisions/requirements. |
| Before start | Explicit execution authorization, prerequisites/capacity checked, actual start. |
| Active | State and next action; blocker date/cause/unblocking condition; revision and evidence at milestones. |
| Closure | Verified criteria, actual finish, exact revision/artifact and agreed delivery evidence, journal reference. |

The folder determines stage; state describes progress inside it. Use `waiting` for a normal queue and `blocked` for an impediment. Neither removes active work from WIP. Keep the original start through rework.

Use a `## Resources` section to link required files and describe their purpose. Store attachments under the owning module's `resources/<card-id>/`. For a Card in `misc` with cross-module impact, list the affected module IDs in the `affected_modules` header so the Card appears in those views.

Keep existing Spec and Batch links on historical Cards.
