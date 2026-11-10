# Markdown Kanban

| Column | Entry condition |
| --- | --- |
| [backlog](backlog/) | Defined and accepted work awaiting execution |
| [in-progress](in-progress/) | Authorized work that has started, including interrupted work with a clear next step |
| [done](done/) | Acceptance criteria verified and evidence recorded |
| [discarded](discarded/) | Decision to abandon the work and its rationale recorded |

The folder determines the official status. Keep each card in one column and preserve its filename and ID when moving it. Link external tickets as references where useful.

## Define and execute work

1. Search all four columns for duplicates. Reuse the relevant card or define the new task with the requester. Clarify questions that affect scope or decisions.
2. Once the backlog entry is approved, copy the [template](task-template.md) to `backlog/TASK-0001-topic.md`, using the next ID after the highest one across all columns. Recheck the ID before integrating concurrent contributions. Never reuse a retired ID.
3. Check prerequisites before starting. Unmet dependencies block affected cards, including through intermediate dependencies. Keep work that has yet to start in the backlog and document the dependency chain.
4. When execution is authorized and capacity is available, move the card to in progress. Keep interrupted work there and record the blocker and next action.
5. Verify every criterion before moving a card to done. Link the journal and evidence. Flag any outstanding user validation explicitly. If the work is abandoned, record the reason and move the card to discarded.

## Define the workflow at adoption

The four folders above are a starting example. Document the types of work, stages, entry and exit criteria, and the points at which work counts as started and finished. In this example, entering `in-progress` marks the start and entering `done` marks the finish. Define the order for selecting eligible cards and the rules for exceptions. Record roles and permissions in the project instructions.

## Manage work in progress

Set an explicit work-in-progress (WIP) limit for the whole workflow or for the stages that need one. When capacity becomes available, pull the next eligible card in the agreed order. At the limit, help finish or unblock existing work. Record and justify any exceptions.

If a card is blocked after it starts, keep it visible at its current stage. Record when it became blocked, why, and who or what can unblock it. It counts toward WIP until it is completed or explicitly withdrawn. A backlog card with an unmet prerequisite stays in the backlog and uses no WIP capacity.

## Measure and improve flow

Use actual start and finish dates. This example uses calendar days. Choose a reporting period and review flow at a cadence that suits the project.

| Measure | Calculation in the example workflow |
| --- | --- |
| Work in progress (WIP) | Number of started cards that are still active, including blocked cards |
| Throughput | Number of cards moved to `done` during the reporting period |
| Work item age | Time elapsed from the start of an active card to today |
| Cycle time | Time elapsed from start to finish for a completed card |

Track discarded work separately from throughput. Use observed cycle times to forecast a duration with a probability. If 85% of comparable cards finished within 10 days, for example, use that benchmark to review cards approaching that age. With insufficient history, state an initial estimate and revise it as data accumulates.

During reviews, look for aging cards, recurring blockers, and changes in throughput. Adjust limits or workflow policies based on the observations and check the effect at a later review.

For software delivery, use the [software development profile](software-development.md) to adapt these rules to implementation, review, and release.

For the flow measures, see [The Kanban Guide](https://kanbanguides.org/the-kanban-guide).
