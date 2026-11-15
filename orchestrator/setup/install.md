# Install or upgrade a project

Output: the approved setup, verified in the target repository. Reader explanations begin at [start a project](../../documentation/start-a-project.md). A procedure, preview or copied file is not permission to execute product work.

## Inspect and agree

1. Check Python 3.9+, Git, the target path, existing code and instructions, any installed kit version and the requested hosts. Use an existing Git repository or obtain authorization to initialize one. If a prerequisite is missing, report it, the recovery action and the untouched state.
2. A target with `project/settings.json` is already installed; upgrade it in place. A target with another Kanban Rememory layout needs a separately approved migration.
3. Agree on the modules, the workflow, WIP limit, timezone, delivery evidence, selection policy and Git permissions using [project modules](project-modules.md). A small project can start with `misc` alone.
4. Present one concrete proposal: target files, settings, workflow and checks. Obtain approval before copying or configuring. Reuse an approval that is already explicit.

## Copy and configure

Keep project code, root instructions, records and unrelated settings. Copy these paths unchanged:

| Path | Contents |
| --- | --- |
| `documentation/` | Reader guides. |
| `orchestrator/` | `index.md`, `VERSION`, `actions/`, `guidelines/`, `setup/`, `templates/`. |
| `orchestrator/tools/` | `manage-kanban-board.py`, `manage-module-delivery.py`, `configure-project-modules.py` and the `kanban/` package. |

Do not copy this kit's Cards, journal or root project policy. Merge this entry into the target's `AGENTS.md` without removing existing instructions, then record the project's ownership and Git permissions there:

```markdown
Act as the Orchestrator and follow the [Card delivery workflow](orchestrator/actions/deliver-card.md).
```

For Claude Code, add `@AGENTS.md` to root `CLAUDE.md`; Codex reads `AGENTS.md`. Apply the approved settings with [project modules](project-modules.md). [Layout](project-layout.md) shows the result.

## Option

| Option | Benefit | Setup |
| --- | --- | --- |
| Telegram | Alerts when an intervention is needed or work completes. | [Telegram](telegram.md) |

Do not infer an opt-in the project has not approved.

## Upgrade and verify

Inventory installed paths and `VERSION` before copying. Compare installed files with the distributed revision; merge approved changes instead of overwriting a directory, and preserve project customizations. Remove distributed files the new version no longer ships only after checking they are unchanged.

Run `validate` and `show` on the board. Open a fresh chat in the target and confirm it identifies the Orchestrator, the layout and the next authorized action. Record each result in Rememory as verified, awaiting user action or blocked, with recovery steps.
