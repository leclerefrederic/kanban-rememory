# Kanban rules

The configured workflow defines stages, active stages, completion, transitions, WIP and timezone. Read it from the selected module workspace, or from `project/kanban/workflow.json` in single-project mode. Example workflows are not additional project stages. The folder is the Card stage; the optional state is `waiting`, `in-progress` or `blocked` within it. Keep one file and stable ID through moves/rework. Use [board commands](../actions/manage-board.md) and [Card content](../actions/write-card.md).

## Intake and execution

Search every stage for matching work before proposing a Card. Writer prepares backlog outcome/scope/checks under project intake policy; Developer may prepare standalone work and owns pickup, stage moves, execution evidence and closure. The User supplies decisions in conversation; agents maintain the records.

Before starting, verify approved scope, execution authorization, dependencies (including intermediate blockers), owner and capacity. Pull the oldest eligible ID unless the project has recorded another priority. Unmet prerequisites keep unstarted work in backlog. Move authorized work to the first active stage before changing deliverables. Preserve the original actual start date through handoffs and rework.

Keep interrupted/blocked work in its current stage. Record when, why and the action/condition that clears the blocker. It counts toward WIP. At capacity, help finish/unblock existing work; urgent exceptions need project-authorized rationale and a return plan. In single-project mode, new standalone work waits until the active Batch is delivered and preserves its candidate. In multi-module mode, a module accepts a new delivery only after its current delivery closes. Independent modules can progress.

## Finish and preserve evidence

Verify all acceptance criteria and the agreed delivery point before completion: applicable tests, review, merge, publication, deployment and User validation are separate facts. A merged PR suffices only when merge is the agreed finish. Keep pending required checks open; return to Development for rework. Record the exact revision/artifact, evidence, actual finish and journal link. On abandonment record the reason and move to Cancellation.

Completed Cards and closed Batch reports are immutable. Corrections/rollback create a successor Card referring to the original. Use stable Card IDs while a Card can move. Cards may link to Batches/Specs; Batch records never reference Cards. The move tool refuses a move that would rewrite frozen Card/report links.

## Measure and improve flow

Count started, unfinished Cards (including blocked) as WIP. Throughput is completed Cards per period, excluding cancellations. Work-item age is today minus actual start; cycle time is actual finish minus actual start, in project calendar days/timezone. Write dates `YYYY-MM-DD`.

At closure or the project's review cadence, inspect blockers, aging work and delivery queues; compare throughput and cycle time. Use historical percentiles to forecast only when comparable data supports them; otherwise label an estimate. Agree one improvement and record its expected effect/review date in Rememory. The [human guide](../../documentation/understand-the-framework.md) explains examples.

Adoption owns stage conditions, selection policy, exceptions and WIP: use [workflow setup](../setup/configure-workflow.md). The [Kanban Guide](https://kanbanguides.org/the-kanban-guide) provides background, not additional local authorization.
