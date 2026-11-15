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

Review each workspace and the workflow with the User. Finish existing active Cards or Batches before activation. With explicit authorization for the displayed setup, repeat with `--apply`. Existing records keep their paths, IDs and bytes. Keep approval, execution and acceptance authority separate. A fresh session uses the root manifest to select its module and load the corresponding records.

Work concurrently only in worktrees of the same clone. Coordinate separate clones before attempting concurrent execution. For projects without a root manifest, use the [single-project setup](configure-workflow.md).
