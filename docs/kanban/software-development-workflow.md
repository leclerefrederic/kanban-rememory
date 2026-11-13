# Kanban for software development

This profile applies [Kanban University's Official Guide to the Kanban Method](https://kanban.university/kanban-guide/), which builds on David J. Anderson's *Kanban: Successful Evolutionary Change for Your Technology Business* (2010). The workflow and engineering checks below are examples to adapt to the team's current delivery process.

## Visualize the work and make policies explicit

Track a feature, fix, or maintenance change as a card with an observable outcome. Split large changes into independently verifiable slices where possible. Each stage has its own folder. Move the same card between folders as work advances or returns for rework. The folder identifies the current stage. Use the [card guide](write-task-cards.md) for required fields and states. Make queues and blockers visible, including work waiting for a reviewer or a release.

| Folder | Example stage | Entry or exit policy |
| --- | --- | --- |
| `backlog` | Backlog | The outcome and acceptance checks are understood, prerequisites are met, and execution is authorized before pull. |
| `development` | Development | Pull when there is capacity. Move to review when the change and its verification instructions are available. |
| `code-review` | Code Review | Record the PR or revision and required checks. Return to Development if changes are requested, keeping the original start date. |
| `deployment` | Deployment, if applicable | Checks and approvals required before release have passed. Keep the card here while release or delivery verification is pending. |
| `completion` | Completion | Acceptance criteria and the agreed delivery point are verified. Record the revision and evidence. |
| `cancellation` | Cancellation | Record the reason and exclude the card from completed throughput. |

Agree on what delivery means for each kind of work. A documentation change may finish at merge, while a fix may require deployment and a production check. Record tests, merge, publication, deployment, and user validation separately as applicable. A required check still pending keeps the card open.

## Limit work in progress and manage flow

Set an overall limit and add stage limits where queues need control. Count cards waiting in review or for release, including blocked cards. Pull the highest-ranked eligible card only when the relevant capacity is available. If review is full, help review or unblock work before pulling another change. If the team allows urgent exceptions, record who authorized them, why, and how the team will return within the limit.

During replenishment, order eligible work and clarify the next items. During flow reviews, start with blocked and aging cards and look at the queues nearest delivery. Use the [flow measures](board-guide.md#measure-and-improve-flow) to identify recurring delays. Keep the original start date through handoffs, rework, and blockers.

## Use feedback to improve the workflow

Choose review intervals that fit the team. Review the board with the people doing the work, and review delivery results and expectations with the people receiving it. Agree on one change to try, such as reserving reviewer capacity, and record the expected effect and review date in Rememory. Compare the observed result with the expectation and decide whether to keep or revise the policy.

## Example

A fix for duplicate invoice emails starts in Development on Monday. Its acceptance criterion requires one email per invoice even when the job is retried. The developer adds a regression test and opens a PR. On Tuesday the card moves to Code Review with state `waiting`. A CI outage blocks the required check, so the state changes to `blocked` and the card stays in Code Review. After CI recovers, a reviewer requests a code change. Move the card back to Development and keep Monday as its start date.

On Wednesday the revised PR passes review and the regression test. If merge is the agreed finish, record the merged revision and test evidence, then move the card to Completion. If delivery requires a production check, move it to Deployment after merge. On Thursday, verify the deployed revision and confirm a retry sends one email, then record the evidence and move the card to Completion. The two paths have cycle times of two and three calendar days respectively.
