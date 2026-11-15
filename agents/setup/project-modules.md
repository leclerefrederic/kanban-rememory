# Configure project modules

For multi-module adoption only. Keep shared sources in the repository. Describe the solution and its module workspaces in a proposed `project.json`. Set schema version 1 and the four execution values below. Use distinct lowercase module IDs and local paths.

```json
{
  "schema_version": 1,
  "project": {"id": "sample", "name": "Sample solution"},
  "shared": {"memory": "project/rememory", "sources": ["src"]},
  "modules": {
    "a": {"workspace": "project/modules/a"},
    "b": {"workspace": "project/modules/b"}
  },
  "execution": {
    "active_deliveries_per_module": 1,
    "branch_required": true,
    "worktree_required": true,
    "concurrent_integrations": 1
  }
}
```

From the principal worktree, preview the proposed layout with an approved workflow file:

```sh
python3 agents/tools/configure-project-modules.py /path/to/proposed-project.json --workflow /path/to/workflow.json
```

Include `--with-batches` in both commands if the approved setup includes [Specifications and Batches](batches.md) in each module. Review the shared project Kanban, project journal, module workspaces and workflow with the User. Finish active work and account for unfinished backlog in an approved plan before activation. With authorization for the displayed setup, repeat with `--apply`. Keep frozen paths, IDs and bytes. An existing setup with old per-module boards requires a separate approved cutover plan. A fresh session uses the manifest and assignment to resolve its scope, then uses the project board and the corresponding journal and optional Batch records.

Work concurrently only in worktrees of the same clone. Coordinate separate clones before attempting concurrent execution. For projects without a root manifest, use the [single-project setup](configure-workflow.md).
