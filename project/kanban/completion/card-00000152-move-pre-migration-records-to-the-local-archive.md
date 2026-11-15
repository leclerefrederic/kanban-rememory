---
type: card
id: "CARD-00000152"
scope: "configuration"
batch: null
specifications: []
---

# CARD-00000152 — Move pre-migration records to the local archive

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

Move pre-migration Cards, Specifications and Batches to local ignored `Archives/`. Retain the project Kanban, project Rememory and all eight module workspaces.

## Scope and authorization

On 2026-11-15 the User authorized moving the old records into repository-root `Archives/` and ignoring it in Git. Keep the project Kanban and Rememory at their existing paths. Move archived Cards to `Archives/kanban/`, legacy Specs to `Archives/specifications/` and legacy Batches to `Archives/batches/`. Preserve frozen bytes and local draft changes. Repair only the project journal link targets for relocated records.

Record the approved boundary and permission to execute.

## Acceptance criteria

- [x] Move old Cards and legacy Specification/Batch folders to ignored `Archives/`, preserving files and local changes.
- [x] Keep the board, workflow, project journal and eight module workspaces. Verify the tracked configuration from a clean clone without the local archive.
- [x] Keep the relocated tracked history accessible at its exact pre-move Git revision. Verify the revised journal links.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

- Reviewed candidate `9bb175059c4c3b9df7403ecc573c8ca96b042cb3` in Development. An independent clone with the local archive out of its working tree passed Kanban validation and diff checks. Changes remove 235 legacy tracked paths and redirect 100 journal links to verified Git objects at `e6ab823dff666070cf22c5a43906c13f2cf5f356`.
- A fast-forward rehearsal preserved modified and untracked draft fixtures and an intentional deletion. The actual local archive move preserved same-file identity for all 151 old Cards, both legacy repositories of records, and the two local draft files. Archived file contents were left intact. The shared board, project journal and eight module workspaces stay live.
- The verified publication milestone is recorded in [project Rememory](../../rememory/2026-11-15.md).

## History

- 2026-11-15T16:52:02+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T16:55:32+01:00 — Stage moved from `development` to `completion`.
