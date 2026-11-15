---
type: card
id: "CARD-00000143"
batch: null
specifications: []
---

# CARD-00000143 — Make parallel delegation explicit for KR Developer

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

The KR Developer instructions make parallel delegation and ownership of integration explicit for Cards and Batches.

## Scope and authorization

The User requested and authorized this role instruction update on 2026-11-15.

For each authorized Card or Batch, KR Developer breaks work into bounded tasks, identifies dependencies and delegates useful independent tasks in parallel when the host and permissions allow. KR Developer remains responsible for integration and verification. Follow the existing orchestration procedure and WIP limits.

## Acceptance criteria

- [x] The KR Developer role explicitly requires this for Cards and Batches.
- [x] The role states who integrates and verifies contributions and links to existing delegation guidance.
- [x] The relevant board and documentation checks pass, with pre-existing local issues recorded.


## Execution and evidence

- State: complete
- Actual start:
- Actual finish: 2026-11-15
- Blocker: None.

- Evidence: Reviewed the Developer role diff and delegation link. Board validation, skill synchronization, and 36 board tests passed in an isolated copy of ad8c0c8 with the proposed change. The shared worktree has pre-existing deletions of the Runner guide and VERSION, which cause two historical link failures and prevent the local skill check. Those deletions were left intact.

## History

- 2026-11-15T12:51:30+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T12:52:28+01:00 — Stage moved from `development` to `completion`.
