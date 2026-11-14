---
type: card
id: "TASK-00000088"
batch: null
specifications: []
---

# TASK-00000088 — Remove the obsolete local docs directory

- Owner: Development Agent
- Dependencies: TASK-00000087 (completed).
- Priority: Explicit User request to trash docs after the directory migration.

## Expected outcome

Remove the obsolete local `docs/` directory from the working tree by moving it to the macOS Trash. The User explicitly includes its remaining local Obsidian configuration after being informed of its contents.

Scope: local directory cleanup and its execution record. The framework already lives in `agents/` and `documentation/`; preserve those files and unrelated local content.

## Acceptance criteria

- [x] Confirm docs contains no tracked framework files, then move the directory to the macOS Trash without overwriting other items.
- [x] Verify the source directory is absent, its files are preserved in Trash, and board validation still passes.
- [x] Record the cleanup evidence and prepare the closed Card for authorized publication.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `994b67d`.
- Verified: no tracked files remained under docs. Moved its 5 local files to the macOS Trash with a unique destination name and compared their contents before and after the move. The source directory is absent.
- Recovery location: `~/.Trash/kanban-rememory-docs-20261114-020008/`.
- Board validation passed after removal. No application code, maintained documentation, or unrelated local file changed; the existing 15-test and isolated-build results remain applicable to the migration.
- Flow review: no active Batch, competing Card or blocker. Ready for authorized publication of this cleanup record.

## History

- 2026-11-14 — User explicitly authorized trashing the residual local docs directory. Supersedes TASK-00000087's local retention of Obsidian configuration.

- 2026-11-14T02:00:03+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T02:00:31+01:00 — Stage moved from `development` to `completion`.
