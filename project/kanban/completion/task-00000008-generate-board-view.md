# TASK-00000008 — Generate a board view from stage folders

- Owner: Kanban Rememory maintainers
- Priority: follows TASK-00000007 in backlog order
- Dependencies: none. Both tools read the same repository layout and can ship independently.
- Backlog approval: requester, 2026-11-10

## Expected outcome

Generate a read-only board view that shows where work sits, what is blocked, and whether there is capacity to pull another card.

## Scope

Read the stage folders and card metadata. Show each stage, including empty stages, and derive each card's stage from its folder. A persistent board file or editing interface is out of scope.

## Acceptance criteria

- [x] A documented command lists cards under their actual stage, with IDs, titles, and paths. Moving a card changes its displayed stage on the next run.
- [x] Active cards show recorded blockers and age from their actual start date. Missing dates are reported as unknown.
- [x] The view counts all active cards toward WIP, including blocked cards and those awaiting review or release. It reports available slots against the configured limit, or reports that the limit is unknown when none is configured.
- [x] The command leaves the cards and working tree untouched.

## Execution and evidence

- Actual start: 2026-11-10
- Actual finish: 2026-11-10
- Verified locally against Git base `c2df064` with an isolated fixture and the repository itself.
- [Milestone log](../../rememory/2026-11-10.md)
