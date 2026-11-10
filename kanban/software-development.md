# Kanban for software development

This profile applies [Kanban University's Official Guide to the Kanban Method](https://kanban.university/kanban-guide/), which builds on David J. Anderson's *Kanban: Successful Evolutionary Change for Your Technology Business* (2010). The workflow and engineering checks below are examples to adapt to the team's current delivery process.

## Visualize the work and make policies explicit

Track a feature, fix, or maintenance change as a card with an observable outcome. Split large changes into independently verifiable slices where possible. Use the existing folders for official status and record the current delivery stage on cards in `in-progress`. Make queues and blockers visible, including work waiting for a reviewer or a release.

| Folder | Example stage | Entry or exit policy |
| --- | --- | --- |
| `backlog` | Ready when eligible | The outcome and acceptance checks are understood, prerequisites are met, and execution is authorized before pull. |
| `in-progress` | Implementing | Pull when there is capacity. Move to review when the change and its verification instructions are available. |
| `in-progress` | In review | Record the PR or revision and required checks. Return to implementation if changes are requested, keeping the original start date. |
| `in-progress` | Ready to release, if applicable | Required checks and approvals have passed. Keep the card here when release or deployment is required for closure. |
| `done` | Delivered | Acceptance criteria and the agreed delivery point are verified. Record the revision and evidence. |
| `discarded` | Withdrawn | Record the reason and exclude the card from completed throughput. |

Agree on what delivery means for each kind of work. A documentation change may finish at merge, while a fix may require deployment and a production check. Record tests, merge, publication, deployment, and user validation separately as applicable. A required check still pending keeps the card open.

## Limit work in progress and manage flow

Set an overall limit and add stage limits where queues need control. Count cards waiting in review or for release, including blocked cards. Pull the highest-ranked eligible card only when the relevant capacity is available. If review is full, help review or unblock work before pulling another change. If the team allows urgent exceptions, record who authorized them, why, and how the team will return within the limit.

During replenishment, order eligible work and clarify the next items. During flow reviews, start with blocked and aging cards and look at the queues nearest delivery. Use the [flow measures](README.md#measure-and-improve-flow) to identify recurring delays. Keep the original start date through handoffs, rework, and blockers.

## Use feedback to improve the workflow

Choose review intervals that fit the team. Review the board with the people doing the work, and review delivery results and expectations with the people receiving it. Agree on one change to try, such as reserving reviewer capacity, and record the expected effect and review date in Rememory. Compare the observed result with the expectation and decide whether to keep or revise the policy.

## Example

A fix starts on Monday. On Tuesday, its PR awaits a required reviewer and occupies a WIP slot. A failed check sends it back to implementation with Monday as its start date. The fix merges on Wednesday, but the card stays open because its acceptance criteria require a production check. After deployment and that check on Thursday, record the evidence and move the card to `done`. It contributes one completed item and three calendar days of cycle time.
