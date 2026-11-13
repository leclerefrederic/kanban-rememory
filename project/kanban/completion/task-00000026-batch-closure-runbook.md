# TASK-00000026 — Verify Lot pickup and closure procedures

- Owner: Kanban Rememory maintainers
- Dependencies: TASK-00000025

## Acceptance criteria

- [x] Document approval evidence, exclusive pickup, and closure recovery.
- [x] Exercise an accepted Lot and a rejected Lot interrupted after archiving.
- [x] Verify that retrying closure preserves the decision and avoids a duplicate commit.

## Evidence

- Git base: `ed47035`.
- Accepted fixture: delivered revision `cdcc4820` was merged and tagged. Closure `85680630` was unchanged on retry.
- Rejected fixture: archived revision `21e23423` was excluded from main. Closure resumed after archival at `79c1fbc6` and was unchanged on retry.
- In both fixtures, a second lock acquisition failed while the first held the lock.
