# Markdown Kanban

The AI Development Agent creates, writes, moves, and closes every Card. The procedures and commands below are for that agent. The User provides requests, priorities, authorizations, and verdicts through conversation; the agent records them on the board.

| Column | Entry condition |
| --- | --- |
| `backlog` | Defined and accepted work awaiting execution |
| `development` | Authorized work being implemented |
| `code-review` | Work awaiting or undergoing review |
| `deployment` | Reviewed work awaiting release or delivery verification |
| `completion` | Acceptance criteria verified and evidence recorded |
| `cancellation` | Decision to abandon the work and its rationale recorded |

The folder determines the stage. The optional card state describes whether work is waiting, in progress, or blocked within that stage. See the [task card guide](write-task-cards.md). Keep each card in one column and preserve its filename and ID when moving it. Link external tickets as references where useful.

## Define and execute work

1. Search all columns for duplicates. Reuse the relevant card or define the new task with the requester. Clarify questions that affect scope or decisions.
2. Once the backlog entry is approved, copy the [template](../../templates/kanban-card.md) to `project/kanban/backlog/task-00000001-topic.md`, using the next number after the highest numeric suffix across all stages for the configured prefix. Use exactly eight digits with leading zeros, from `TASK-00000001` to `TASK-99999999`. After `TASK-00009999`, use `TASK-00010000`. Stop and agree on a numbering migration before exceeding the range. Recheck the ID before integrating concurrent contributions. Never reuse a retired ID.
3. Check prerequisites before starting. Unmet dependencies block affected cards, including through intermediate dependencies. Keep work that has yet to start in the backlog and document the dependency chain.
4. When execution is authorized and capacity is available, move the card to the first active stage. Keep interrupted work in its current stage and record the blocker and next action.
5. Verify every criterion before moving a card to Completion. Link the journal and evidence. If user validation is required for closure, keep the card in its current active stage until that validation is recorded. If the work is abandoned, record the reason and move the card to Cancellation.

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

For software delivery, use the [software development profile](software-development-workflow.md) to adapt these rules to implementation, review, and release.

For the flow measures, see [The Kanban Guide](https://kanbanguides.org/the-kanban-guide).

## Validate the repository

Run `python3 tools/manage-kanban-board.py validate` from the repository root with Python 3.9 or later and Git available. The command reads card filenames and local Markdown without changing files. It returns exit code 1 for invalid task filenames, duplicate task IDs, missing local link targets or Markdown heading anchors, and unchecked items under **Acceptance criteria** on cards in `completion/`. Older cards without checklist criteria are accepted.

Link checks cover inline relative Markdown links and ATX heading anchors (headings written with `#`). External URLs, reference-style links, and HTML anchors are outside this check.

## Show the board

Run `python3 tools/manage-kanban-board.py show` from the repository root with Python 3.9 or later. The limit of one applies to this repository. Set the project limit in `project/kanban/workflow.json` after [guided adoption](../configure-a-project.md). Pass `--wip-limit` to override it for a single run. The board lists each stage, counts all active stages toward WIP, and reads age and blockers from the `Actual start` and `Blocker` fields. Write start dates as `YYYY-MM-DD`. Age uses calendar days in the configured time zone. Pass `--timezone` with the project's IANA time zone when needed.

## Legacy task references

To look up a reference published before the eight-digit migration, left-pad its numeric suffix to eight digits. For example, the former `TASK-0015` is now `TASK-00000015`. The numeric value and filename slug stay the same.

## Move a card

Run `python3 tools/manage-kanban-board.py move TASK-00000019 code-review` with the ID and destination for your card. Starter workflows include forward moves, returns to Development for rework, and withdrawal to Cancellation. For a custom or existing board, add a `transitions` object to `project/kanban/workflow.json`. Each key is a source stage and its value is the list of permitted destinations. Stages with no outgoing moves can be omitted.

The command checks capacity when a card enters an active stage, and requires a nonempty, fully checked acceptance checklist before completion. It moves the same file and preserves its original start date. It also updates relative inline Markdown links to the card, including section anchors, and adjusts relative links within the moved card. Record authorization, dates, evidence, and state on the card as work progresses. For links outside the repository or formats outside the inline Markdown check, update references separately. Then run `python3 tools/manage-kanban-board.py validate`. See the [worked card example](write-task-cards.md#worked-example).

## Create a card

Preview a card with `python3 tools/manage-kanban-board.py new "Verify retries" --owner "Billing team"`. After backlog approval, run the same command with `--apply`. The command uses the card template and assigns the next eight-digit `TASK` number across every stage, including Cancellation. The ID shown in a preview can change if another card is created first.

The first configured stage is the intake folder by default. Set `intake` in `project/kanban/workflow.json` to use a different configured stage outside active and completed work. Fill in the outcome, scope, and acceptance criteria before starting the card with `move`.
