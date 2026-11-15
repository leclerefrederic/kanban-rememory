---
type: card
id: "CARD-00000142"
batch: null
specifications: []
---

# CARD-00000142 — Remove historical documentation redirects

- Owner: KR Developer
- Dependencies:

## Expected outcome

## Scope and authorization

Record the approved boundary and permission to execute.

Remove the 11 historical Markdown redirects from agents/ and any equivalent redirects in documentation/. Remove the empty legacy agents/claude directory if present, preserving the active agents/hosts/claude adapters and any local files. Update active references and routing text. The User accepts broken links in completed Cards and closed Batches; preserve those records. Keep validation strict for active references and handle only the accepted historical exceptions if necessary.

## Acceptance criteria

- [x] Historical redirects and the empty legacy Claude directory are gone.
- [x] Active documentation, host discovery and role checks still resolve.
- [x] Any remaining missing links are limited to authorized historical cases or separately documented pre-existing local changes.


## Execution and evidence

- State:
- Actual start:
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15T12:43:38+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T12:44:43+01:00 — User requested removal of historical redirects and accepted dangling historical links. Removed 11 redirects and Finder metadata from the empty legacy Claude directory. Frozen records kept intact. Validation permits only 14 exact retired links. Isolated candidate: board validation, skill sync, 36 Kanban and 14 role migration tests passed; an identical broken link in an active Card was rejected. Live checkout retains unrelated pre-existing removals.

- 2026-11-15T12:44:43+01:00 — Stage moved from `development` to `completion`.
