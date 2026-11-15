# Prepare Card content

Search the board for matching work first. Create the Card with the [board command](manage-board.md#create); it fills the [template](../templates/card.md). The user supplies requests and decisions in conversation; the agent maintains the Card. Exclude secrets and unnecessary personal data.

A Card describes one executable outcome, including an investigation whose deliverable is a finding. Keep detailed designs, logs and test outputs in linked evidence.

| Point | Required record |
| --- | --- |
| Intake | Action title, exactly one `module` field, owner, expected outcome, scope, dependencies or none, observable acceptance criteria, relevant decisions. |
| Before start | Explicit execution authorization, prerequisites and capacity checked, actual start. |
| Active | State and next action; blocker date, cause and clearing condition; revision and evidence at milestones. |
| Closure | Checked criteria, merge approval, actual finish, exact revision and delivery evidence, journal reference. |

Use `waiting` for a normal queue and `blocked` for an impediment; both stay in WIP.

Link required files from a `## Resources` section with their purpose. Store attachments under the owning module's `resources/<card-id>/`; reference repository files at their existing paths. For a `misc` Card with cross-module impact, list the module IDs in an `affected_modules` header field.
