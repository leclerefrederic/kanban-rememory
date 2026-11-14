---
type: card
id: "TASK-00000084"
batch: null
specifications: []
---

# TASK-00000084 — Replace historical documentation redirects with direct links

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User authorization to remove obsolete documentation redirects.

## Expected outcome

Use direct links to the maintained documentation and remove redirect-only files and their empty directories.

Scope: the seven documentation redirects, references targeting them, and current index descriptions. The User explicitly authorizes updating link destinations inside closed historical records for this migration. Preserve their substantive content, decisions and evidence. This exception does not change the general immutability rule.

## Acceptance criteria

- [x] Update all affected documentation links, including historical references and anchors, to their maintained destination.
- [x] Delete the seven redirect-only files and the three obsolete directories once empty; remove current documentation statements describing those redirects.
- [x] Keep historical edits limited to link destinations and preserve unrelated local files.
- [x] Verify documentation links, installation and the diff before closing and publishing.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `c359f46`. Under the User's explicit migration exception, updated eight link destinations across five historical documents and retained their anchors. Compared each changed document with its prior revision after only the expected link substitutions; all substantive content is unchanged.
- Deleted seven redirect-only files and the now-empty former Batch, Kanban and Runner documentation directories. Removed obsolete redirect descriptions from the current documentation indexes.
- Updated one additional reference in the existing untracked scheduler draft so it remains usable locally. That draft is excluded from the commit; unrelated local configuration remains untouched.
- `python3 tools/test-kanban-board.py`: all 15 tests passed. `python3 tools/manage-kanban-board.py validate` and `git diff --check` passed. Verified that no redirect placeholder or Markdown link to a removed path remains, including in local drafts.
- Flow review: no active Batch or competing Card, no blocker. This is a documentation migration; no application behavior changed. Next action: publish the closed Card and verified changes under standing authorization.

## History

- 2026-11-14 — User explicitly authorized rewriting historical documentation links and removing the obsolete redirect files and directories. No Batch or other Card is active.

- 2026-11-14T01:41:27+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:42:58+01:00 — Stage moved from `development` to `completion`.
