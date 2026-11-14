---
type: card
id: "CARD-00000112"
batch: null
specifications: []
---

# CARD-00000112 — Fix the push check for rejected Batches and for the pushed commit

- Owner: Development Agent
- Dependencies:

## Expected outcome

The optional push check from CARD-00000101 handles two cases it got wrong, found by an independent review of 2026-11-14 and confirmed by reading the code. (1) A push that closes a rejected Batch with a guard record was refused, because `publish` required an accepted decision. A rejected closure must pass when the User's rejection of the exact revision is recorded and the revision stays out of the published history. (2) The check read the pushed commit but the guard compared the candidate with `HEAD`, so a push such as `other:main` checked the wrong history. The guard now receives the pushed commit. The two cases were not covered by the tests. Shared core: the same for ChatGPT/Codex and Claude; the check is an optional Git hook.

## Acceptance criteria

- [x] `guard-batch-work.py publish` accepts `--revision` and checks ancestry against that commit; without it, it uses `HEAD`.
- [x] A recorded decision `rejected` for the exact frozen revision passes `publish` when the revision is not an ancestor of the published commit, and fails when it is, or when the decision names another revision.
- [x] The push check passes the pushed commit to the guard.
- [x] Tests cover a rejected closure, an accepted closure pushed from another branch, and the existing cases.
- [x] `agents/batches/start-and-close-batches.md` describes both cases.
- [x] The adoption tests pass, board validation passes, and skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:30:04+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:32:39+01:00 — Stage moved from `development` to `completion`.
