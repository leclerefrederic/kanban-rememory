---
type: card
id: "CARD-00000153"
scope: "configuration"
batch: null
specifications: []
---

# CARD-00000153 — Use specifications directories in setup and tools

- Owner: KR Developer
- Dependencies: CARD-00000152 (finish the archive before pickup).

## Expected outcome

New installations use `specifications/` for Specification records. This repository's eight active module workspaces use the same name. Agents and tooling find the records in the chosen layout.

## Scope and authorization

- The User authorized the directory rename and installation-script correction on 2026-11-15. Update the real setup entry points and their instructions for simple and multi-module installs, including the optional Specs/Batch setup.
- Rename the eight active module `specs/` directories to `specifications/`. Resolve that path consistently in the board, Batch selection, approval/resource checks, role permissions and relevant documentation. Keep Spec IDs and the Card front-matter field `specifications`.
- Preserve existing installations and frozen paths. Tools recognize an existing legacy `specs/` workspace without rewriting it. If both paths exist in an active workspace, report the ambiguity before writes. Use only the canonical name for newly created Specification directories. Preserve the local archive and its contents.

## Acceptance criteria

- [x] The supported simple and modular setup paths propose and create `specifications/` wherever Specs are enabled. Existing optional feature choices still apply.
- [x] All eight repository workspaces have `specifications/` and resolve it in normal operation. No new duplicate record folder is created.
- [x] Fixtures prove Spec lookup, Batch approval/resource verification and role limits in the canonical and legacy layouts, plus an explicit refusal for ambiguous paths. Frozen records and local archives keep their bytes.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:
- Verified product revision: `2a422f30cb203d8debd77df106974776c377addb`.
- Reviewed the diff in Development. Seven board scenarios, two module-setup scenarios, one accepted-product guard scenario and 22 role-policy scenarios passed. Python 3.9 syntax, Kanban validation and skill consistency passed. Both setup entry points offer `--with-batches`; the option reuses a legacy root where present. The eight renamed directories contained 48 unchanged placeholders. No archive file changed.

## History

- 2026-11-15T16:57:50+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T17:04:14+01:00 — Stage moved from `development` to `completion`.
