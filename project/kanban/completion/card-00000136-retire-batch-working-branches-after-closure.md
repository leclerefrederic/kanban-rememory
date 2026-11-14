---
type: card
id: "CARD-00000136"
batch: null
specifications: []
---
# CARD-00000136 — Retire Batch working branches after closure

- Owner: Development Agent
- Approval and priority: the User said “passe la carte” immediately after CARD-00000136 was presented on 2026-11-15. Execute this targeted Card before other backlog work.

## Expected outcome

Closing a Batch includes retiring its temporary working and recovery branches after its closing records and exact candidate are safely published. The user can still reconstruct the delivery and roll back accepted changes from Git history.

## Scope

Update the Batch closure and recovery instructions. Record the working, recovery, and durable archive references. For an accepted Batch, verify the closing commit on main, the tested revision in its ancestry and the accepted tag at that revision. For a rejected Batch, verify the closing records on main and the durable archive ref at the rejected revision. Retire only the temporary refs, preserve approval evidence and leave any branch or workspace with unrelated work untouched.

## Acceptance criteria

- [x] In an isolated remote, verify that accepted and rejected closures retire their temporary branches only after confirming the exact published closing and archive refs. The candidate and approval evidence remain accessible.
- [x] Retry after a partial cleanup. Missing temporary branches count as already retired. A branch that moved, an unverified archive, or an occupied local worktree is reported and preserved.
- [x] The instructions cover remote working and recovery branches, local cleanup when safe, and the distinct archive used for accepted and rejected deliveries.

## History

- 2026-11-15 — User requested a closure rule after obsolete working and recovery branches accumulated on the remote.

- 2026-11-15T00:54:05+01:00 — Stage moved from `backlog` to `development`.

## Verification

- Actual finish: 2026-11-15.
- Reviewed the documentation diff in Development. Tested accepted and rejected closures in separate local bare remotes: missing archive, moved ref, lease refusal, successful cleanup, retry, preserved archive and approval, and occupied local worktree. Board validation, skill synchronization and whitespace checks passed.
- Flow reviewed. No blockers remain. The Telegram review remains in Backlog.

- 2026-11-15T00:55:30+01:00 — Stage moved from `development` to `completion`.
