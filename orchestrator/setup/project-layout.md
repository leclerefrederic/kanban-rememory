# Installed project layout

This is the resulting layout, not a copy list. [Installation](install.md) owns copying/configuration and [workflow setup](configure-workflow.md) creates the approved stage folders. Keep existing product code/tests alongside it.

```text
project/
  settings.json
  rememory/
    YYYY-MM-DD.md
  modules/
    notifications/
      backlog/
      cancellation/
      completion/
      development/
      resources/
    misc/
      backlog/
      cancellation/
      completion/
      development/
      resources/
```

The `workflow` section of `settings.json` defines stage names and order. Cards use one project-wide ID sequence. Attachments live under the owning module's `resources/<card-id>/`. Dated files in `rememory/` form one project journal.

Historical Batch layout:

```text
project/
  specifications/
    draft/, ready/, approved/, retired/
    resources/active/, resources/archived/
  batches/
    batch-001/
      description.md
      tests.md
      report.md
      evidence/                   Create with the first attachment
```

A ready Batch pins the approved Specifications by their stable IDs and paths. Specs travel from draft to ready to approved, then retire when their Batch closes. Existing workspaces using `specs/` retain that name and their frozen paths. IDs are `SPEC-001`, `Batch-001`; paths remain lowercase. Cards reference Batch/Spec IDs, never the reverse. Local guards belong in the shared Git directory. Each adopting project starts with its own workflow, Cards, Specs, Batches and dated records.

## Migrate existing journals

From the primary worktree, use the journal migration tool to preview. Review the moves and link updates, then apply the approved plan.

```sh
python3 orchestrator/tools/migrate-rememory.py
python3 orchestrator/tools/migrate-rememory.py --apply
```

Resolve reported collisions before applying. Validate the project board and rerun the preview to confirm that the migration is complete. Coordinate the apply step with other worktrees so journal writers use the same layout.
