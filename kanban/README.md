# Markdown Kanban

| Column | Entry condition |
| --- | --- |
| [backlog](backlog/) | Defined and accepted work awaiting execution |
| [development](development/) | Authorized work being implemented |
| [code-review](code-review/) | Work awaiting or undergoing review |
| [deployment](deployment/) | Reviewed work awaiting release or delivery verification |
| [completion](completion/) | Acceptance criteria verified and evidence recorded |
| [archive](archive/) | Decision to abandon the work and its rationale recorded |

The folder determines the stage. The optional card state describes whether work is waiting, in progress, or blocked within that stage. See the [task card guide](card-guide.md). Keep each card in one column and preserve its filename and ID when moving it. Link external tickets as references where useful.

## Define and execute work

1. Search all columns for duplicates. Reuse the relevant card or define the new task with the requester. Clarify questions that affect scope or decisions.
2. Once the backlog entry is approved, copy the [template](task-template.md) to `backlog/TASK-0001-topic.md`, using the next ID after the highest one across all columns. Recheck the ID before integrating concurrent contributions. Never reuse a retired ID.
3. Check prerequisites before starting. Unmet dependencies block affected cards, including through intermediate dependencies. Keep work that has yet to start in the backlog and document the dependency chain.
4. When execution is authorized and capacity is available, move the card to the first active stage. Keep interrupted work in its current stage and record the blocker and next action.
5. Verify every criterion before moving a card to Completion. Link the journal and evidence. If user validation is required for closure, keep the card in its current active stage until that validation is recorded. If the work is abandoned, record the reason and move the card to Archive.

## Define the workflow at adoption

The folders above are a starting example. Document the types of work, stages, entry and exit criteria, and the points at which work counts as started and finished. In this example, entering `development` marks the start and entering `completion` marks the finish. Define the order for selecting eligible cards and the rules for exceptions. Record roles and permissions in the project instructions.

## Manage work in progress

Set an explicit work-in-progress (WIP) limit for the whole workflow or for the stages that need one. When capacity becomes available, pull the next eligible card in the agreed order. At the limit, help finish or unblock existing work. Record and justify any exceptions.

If a card is blocked after it starts, keep it visible at its current stage. Record when it became blocked, why, and who or what can unblock it. It counts toward WIP until it is completed or explicitly withdrawn. A backlog card with an unmet prerequisite stays in the backlog and uses no WIP capacity.

## Measure and improve flow

Use actual start and finish dates. This example uses calendar days. Choose a reporting period and review flow at a cadence that suits the project.

| Measure | Calculation in the example workflow |
| --- | --- |
| Work in progress (WIP) | Number of started cards that are still active, including blocked cards |
| Throughput | Number of cards moved to `completion` during the reporting period |
| Work item age | Time elapsed from the start of an active card to today |
| Cycle time | Time elapsed from start to finish for a completed card |

Track discarded work separately from throughput. Use observed cycle times to forecast a duration with a probability. If 85% of comparable cards finished within 10 days, for example, use that benchmark to review cards approaching that age. With insufficient history, state an initial estimate and revise it as data accumulates.

During reviews, look for aging cards, recurring blockers, and changes in throughput. Adjust limits or workflow policies based on the observations and check the effect at a later review.

For software delivery, use the [software development profile](software-development.md) to adapt these rules to implementation, review, and release.

For the flow measures, see [The Kanban Guide](https://kanbanguides.org/the-kanban-guide).

## Validate the repository

Run `python3 kanban/board.py validate` from the repository root with Python 3.9 or later and Git available. The command reads card filenames and local Markdown without changing files. It returns exit code 1 for duplicate task IDs, missing local link targets or Markdown heading anchors, and unchecked items under **Acceptance criteria** on cards in `completion/`. Older cards without checklist criteria are accepted.

Link checks cover inline relative Markdown links and ATX heading anchors (headings written with `#`). External URLs, reference-style links, and HTML anchors are outside this check.

## Show the board

Run `python3 kanban/board.py show` from the repository root with Python 3.9 or later. The limit of one applies to this repository. Set the project limit in `workflow.json` after [guided adoption](adoption.md). Pass `--wip-limit` to override it for a single run. The board lists each stage, counts all active stages toward WIP, and reads age and blockers from the `Actual start` and `Blocker` fields. Write start dates as `YYYY-MM-DD`. Age uses calendar days in the configured time zone. Pass `--timezone` with the project's IANA time zone when needed.
