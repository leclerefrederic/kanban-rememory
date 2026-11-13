# TASK-00000007 — Add a read-only Kanban validator

- Owner: Kanban Rememory maintainers
- Priority: first eligible change by task ID
- Dependencies: none
- Backlog approval: requester, 2026-11-10

## Expected outcome

Run one documented command from the repository root to catch structural and documentation errors before publishing.

## Scope

Check card IDs across all stage folders, local Markdown links and heading anchors, and acceptance criteria on completed cards. Report findings to the caller. Network checks and automatic fixes are out of scope.

## Acceptance criteria

- [x] The command exits successfully on the current valid repository and leaves its files untouched.
- [x] Duplicate IDs, missing local targets or anchors, and unchecked acceptance criteria on cards in `done/` produce a nonzero exit code and diagnostics that identify the affected files and issues.
- [x] Existing historical cards without a checkbox-based acceptance section remain readable and do not fail solely for using another format.
- [x] The guide documents the command, its prerequisites, and what each failure means.

## Execution and evidence

- Actual start: 2026-11-10
- Actual finish: 2026-11-10
- Verified locally against Git base `c2df064` with an isolated fixture and the repository itself.
- [Milestone log](../../rememory/2026-11-10.md)
