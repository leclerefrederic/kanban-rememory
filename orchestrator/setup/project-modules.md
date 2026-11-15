# Configure project modules

Use `project/settings.json` for the project identity, module workspace paths, execution policy and embedded `workflow`. Use lowercase module IDs and include `misc` for work without a natural owner. Each module has its stage directories and `resources/` directly in its workspace. The project journal is flat under `project/rememory/`.

Keep the workflow aligned with the stage directories. Set `last_card_id` to zero for a new project, or to the last previously assigned number if old Cards were removed during a reset. The allocator also checks IDs on the current boards.

Verify the board with `python3 orchestrator/tools/manage-kanban-board.py validate` and inspect it with `python3 orchestrator/tools/manage-kanban-board.py show --scope misc`.

For a fresh target, preview from its primary checkout with `python3 orchestrator/tools/configure-project-modules.py /path/to/proposed-settings.json`. Repeat with `--apply` after approval. Keep earlier project records in Git or an archive if they are needed after a reset.

The separate `--workflow` file is supported for legacy manifests.
