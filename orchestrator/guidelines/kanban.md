# Kanban rules

The `workflow` section of `project/settings.json` defines the stages, transitions, WIP limit and timezone. Each module has its own Kanban and WIP count. The folder is the Card stage; the optional state is `waiting`, `in-progress` or `blocked` within it. Keep one file and a stable project-wide ID. The `module` field names the owning module. Use [board commands](../actions/manage-board.md) and [Card content](../actions/write-card.md).

## Intake and execution

Search every stage for matching work before proposing a Card. Before starting, verify approved scope, execution authorization, dependencies, owner and capacity. Pull the oldest eligible ID unless the Card records another agreed priority. Unmet prerequisites keep unstarted work in backlog. Move authorized work to the first active stage before changing deliverables. Keep the original actual start through rework.

Keep interrupted or blocked work in its current stage. Record when, why and the condition that clears the blocker. It counts toward WIP. At capacity, finish or unblock existing work first; an urgent exception needs a recorded rationale and return plan. Independent modules can progress in parallel.

## Finish and preserve evidence

Before completion verify every acceptance criterion and the agreed delivery point. Tests, review, merge, publication, deployment and user validation are separate facts. Return failed work to Development. Record the exact revision, evidence, actual finish and journal link. On abandonment record the reason and move to Cancellation.

Completed Cards are immutable. Corrections and rollbacks create a successor Card that refers to the original. Refer to Cards by stable ID while they can move.

## Measure flow

WIP counts started, unfinished Cards, including blocked ones. Throughput is completed Cards per period, excluding cancellations. Age is today minus actual start; cycle time is actual finish minus actual start, in project calendar days. Write dates as `YYYY-MM-DD`. At closure or resumption, review blockers and aging work; record one agreed improvement and its review date in Rememory.
