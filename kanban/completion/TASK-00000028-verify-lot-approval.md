# TASK-00000028 — Verify Lot approval before pickup

- Owner: Kanban Rememory maintainers
- Dependencies: TASK-00000027

## Acceptance criteria

- [x] Check a ready Lot and its frozen Fiches against a trusted approval commit.
- [x] Reject modified Fiches, replaced digests, and mission changes without writing files.
- [x] Document the check in the pickup procedure and cover it with a regression test.
