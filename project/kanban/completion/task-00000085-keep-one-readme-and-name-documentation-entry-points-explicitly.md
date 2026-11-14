---
type: card
id: "TASK-00000085"
batch: null
specifications: []
---

# TASK-00000085 — Keep one README and name documentation entry points explicitly

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User approval of the README simplification.

## Expected outcome

Keep a single README at the repository root. Rename the reader and agent contents pages to `index.md`, remove the redundant documentation landing page, and move Rememory operating instructions under `docs/agents/maintain-rememory.md`.

Scope: approved document relocations/deletion, live and historical links, installation instructions and fixtures. Keep human guides and agent procedures separate. Update historical link destinations under the User-authorized documentation cleanup without changing their substantive records. Do not create redirects.

## Acceptance criteria

- [x] Keep only the root README; use explicit index and procedure filenames elsewhere.
- [x] Preserve useful navigation and Rememory instructions with corrected links and anchors, without redirect files.
- [x] Update installation paths and the directory template; keep historical changes limited to reference destinations and unrelated local files untouched.
- [x] Verify local links, fresh installation and the diff before closure and publication.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `5e896d2`. The root README is the only remaining README document. The [reader index](../../../docs/guides/index.md) and [agent index](../../../docs/agents/index.md) retain separate audiences. Rememory instructions now live in [maintain-rememory.md](../../../docs/agents/maintain-rememory.md); the redundant documentation landing page is removed without a redirect.
- Updated navigation, the installation package and directory template. Verified that the three changes to historical TASK-00000082 are link destinations only; its substantive record remains intact. Preserved the Rememory procedure with only its title and template link adjusted.
- `python3 tools/test-kanban-board.py`: all 15 tests passed, including fresh core and Batch installation. Board validation and whitespace checks passed. Verified that no link targets a removed README and that all 32 documentation files remain reachable from the root README.
- Reviewed the documentation and installation diff. No application behavior changed. Unrelated local files remain untouched. Flow review: no active Batch or competing Card, no blocker. Next action: publish under standing authorization.

## History

- 2026-11-14 — User approved keeping one root README, renaming both audience indexes, deleting the intermediate documentation index and moving Rememory instructions into the agent directory. No other Card or Batch is active.

- 2026-11-14T01:46:20+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:47:44+01:00 — Stage moved from `development` to `completion`.
