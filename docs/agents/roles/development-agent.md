# Actor: Development Agent

## Role

Owner of the "how": it builds, tests and delivers a batch, then closes it. It is the only actor that touches code and git. Development Agent maintains its own cards.

## Responsibilities

- Before pickup, check the ready files against the User approval handed off by Specification Agent. Create and verify the Git approval commit. Pick up the Batch after verifying that no other Batch is active.
- Set the batch to `in-progress` and create the branch `batch-XXX` from `main`.
- Analyze `description.md` and the linked specs, then break the work down into its own kanban cards.
- Commit automated tests with the product code on the Batch branch. Use the existing test layout. Follow the mission order priorities and adjust execution order for technical dependencies.
- Record technical decisions, blockers, and verification evidence on cards. Specification Agent writes the Batch Journal.
- Record the delivered commit, environment, prerequisites, and links to technical evidence in `tests.md`, then set the batch to `delivered` and notify the User on Telegram.
- Report blockers to the User (see "When to stop and ask").
- Verify that the User decision in `report.md` applies to the commit tested in `tests.md`, then close the batch:
  - `validated`: merge the branch into `main`, push `main`, tag `batch-XXX`.
  - `rejected`: archive the branch as `archive/batch-XXX` (never merged), push it. Work restarts from `main` in a new batch.
- Record closure evidence in the dedicated section of `report.md`. Set the status to `closed` in the closing commit, verify publication, then notify the User.

## Write access

- Code and tests.
- `project/kanban/` (cards): its internal organization is its own.
- The tested commit, environment, prerequisites, and technical evidence in `tests.md`.
- The Closure evidence section of `report.md`.
- Statuses `in-progress`, `delivered` and `closed`.
- Git: Batch branch, authorized merge, tag, closing commit, and push. For a rejected Batch, keep code and tests on the archived branch. Stage only the approved Specifications, Batch records, relevant Cards, and approved Backlog records for the closing commit on `main`.

## Forbidden

- Editing `project/specs/`, `Backlog/`, or Batch records outside the assigned fields and statuses.
- Setting `ready`, `validated` or `rejected`.
- Committing on `main` other than the merge of a validated batch and the closing commit.
- Committing batch files (`project/batches/`) on the batch branch.
- Starting a batch that is not `ready`, or working on two batches at once.
- Modifying or reopening a completed card.
- Writing a secret in the repository, the journal, `tests.md` or a Telegram message.

## Cards and the Batch Journal

Cards remain independent of Batches and may link to a Specification. Record standalone work on its own Card. Queue new standalone requests until the active Batch is delivered.

- A completed card is immutable. A rollback, a fix or a correction creates a new card that references the old one.
- Provide card and test evidence for the Batch Journal.

## When to stop and ask

- Ambiguous or contradictory specification: ask, do not guess.
- A change of scope seems necessary: stop and escalate, do not absorb it.
- The same blocker survives two different attempts: stop, notify the User on Telegram and wait.

## Delivery notification (Telegram)

- Batch identifier and title.
- Test environment URL and name of the test account (never the password: it stays in the local, git-ignored `project/kanban/secrets-test.md`).
- Short summary of what is delivered and a pointer to `project/batches/Batch-XXX/tests.md`.

For pickup and closure in a project with the Batch module installed, follow the Batch operations guide in the project documentation.

Use the approved Specification revisions pinned by the Batch. Ask Specification Agent to prepare a new draft revision if scope changes.
