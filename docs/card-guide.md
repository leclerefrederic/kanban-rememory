# Task cards

A card tracks one executable task with a verifiable outcome. Examples include fixing a bug, adding a test, migrating a database, and investigating an alert with a documented finding as the outcome. A requirement may lead to several cards. Split a task when parts can be executed and verified independently.

| When | What the card contains |
| --- | --- |
| At intake | Stable ID, action title, accountable owner or team, expected outcome, scope, dependencies or an explicit statement that there are none, and observable acceptance criteria with a way to check each one. Link relevant requirements or decisions. |
| Before starting | Record authorization, check dependencies and capacity, and add the actual start date. |
| While active | Record the current state and any next action needed for handoff. Use `waiting` for a normal queue, `in-progress` for active execution, and `blocked` for an impediment. For a blocker, record its date, cause, and the action or condition that clears it. |
| At closure | Record the actual finish date, mark criteria verified, and link the revision, checks and delivery evidence. A merged PR is sufficient only when merge is the agreed delivery point. |

The folder identifies the stage. The state describes the task within that stage and does not change its WIP treatment. For example, a PR waiting for its assigned reviewer stays in Code Review with state `waiting`. A CI outage that prevents a required check changes its state to `blocked`. When a reviewer requests a code change, move the same card back to Development and keep its ID and original start date.

Keep the card short enough to act on. Link detailed requirements, design records, test output, PR discussions and Rememory entries. Keep credentials, personal data and copied logs out of the card.

Use the [task template](lot-templates/Card.md) and see the [software example](software-development.md#example).

## Worked example

At start, record the outcome, criteria, and authorization.

```markdown
# TASK-00000042 — Prevent duplicate invoice emails

- Owner: Billing team
- Dependencies: none
- Approval to execute: Billing lead, 2026-11-10

## Expected outcome

A retry sends no second email for an invoice that was already sent.

## Scope

Invoice email retries. Other notification types are outside scope.

## Acceptance criteria

- [ ] The retry regression test confirms one email per invoice.
- [ ] The merged revision passes the required review and checks.

## Execution and evidence

- State: in-progress
- Actual start: 2026-11-10
```

In Code Review, keep the same card and update the execution fields when CI blocks review.

```markdown
- State: blocked
- Actual start: 2026-11-10
- Blocker: CI outage since 2026-11-11. Rerun the required check once CI recovers.
- Evidence: PR #42 in the billing repository.
```

At completion, check the criteria and record the finish and evidence. In this example, merge is the agreed delivery point.

```markdown
## Acceptance criteria

- [x] The retry regression test confirms one email per invoice.
- [x] The merged revision passes the required review and checks.

## Execution and evidence

- Actual start: 2026-11-10
- Actual finish: 2026-11-12
- Delivery evidence: PR #42 merged at revision abc1234. Required review and retry regression test passed.
```

## Specification sheets and Lots

A card can track work independently of a Lot. Record stable IDs in the optional YAML `lot_id` and `fiche_ids` fields. A standalone task can leave both fields empty. The Lot pins its approved Fiche revisions.

Completed cards and closed Lot reports are historical records. Use a card's stable ID when an immutable record needs to refer to a card that can still move. The board refuses a move that would rewrite a completed card or a closed report at `Lots/Lot-XXX/Report.md`. It reports the affected document before changing files.
