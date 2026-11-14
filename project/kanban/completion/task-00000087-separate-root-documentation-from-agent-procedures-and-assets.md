---
type: card
id: "TASK-00000087"
batch: null
specifications: []
---

# TASK-00000087 — Separate root documentation from agent procedures and assets

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User approval of the six-step root layout change.

## Expected outcome

Place agent instructions at root `agents/`, their executable tools at `agents/tools/`, and templates at `agents/templates/`. Move reader guides to root `documentation/`. Remove `docs/` only if empty, preserving the User's local Obsidian configuration.

Scope: directory moves, executable root/template lookup, build bundling, installation package, current documentation and reference migration. Update historical link destinations only under the User-authorized cleanup. Preserve application behavior, common principles and unrelated local content.

## Acceptance criteria

- [x] Apply the requested directory layout without redirects; preserve file contents except necessary path and documentation changes.
- [x] Update repository-root and template discovery, current commands, installation paths and KRR validator bundling.
- [x] Update live and historical links without changing historical decisions; leave local configuration untouched and remove docs only if empty.
- [x] Verify links, all adoption tests, relocated commands and a full isolated KRR build with its bundled validator before closure and publication.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `21c5d3e`.
- Verification: all 15 adoption/regression tests passed after relocation, covering installed framework paths and Card creation from the relocated template. Board validation and whitespace checks passed.
- Reviewed the path migration and root lookup changes. All 32 maintained documentation files remain reachable, historical record edits are link-only, and the shared manifesto is unchanged.
- Full isolated macOS compilation, strict signature, icon/executable checks and bundled-validator execution passed. The validator also works when invoked outside the repository. Removed the temporary verification bundle; existing app builds were preserved and no app was launched.
- Preserved all four local Obsidian configuration files byte-for-byte. `docs/` remains locally because it contains that configuration and ignored macOS metadata; the framework no longer uses it. Unrelated untracked files remain excluded from publication.
- Flow review: no active Batch, competing Card or blocker. Standalone publication is authorized by the repository owner.

## History

- 2026-11-14 — User requested root agents and documentation directories, tools and templates inside agents, and conditional removal of docs. No active Batch or other Card. Local docs/.obsidian configuration remains outside the framework and must be preserved.

- 2026-11-14T01:53:45+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:59:14+01:00 — Stage moved from `development` to `completion`.
