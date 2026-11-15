# Install or upgrade a project

Output: approved core setup and selected options, verified in the target repository. This procedure coordinates adoption; linked setup documents own their commands. Maintain the project records under the applicable workflow and permissions. Reader explanations begin at [start a project](../../documentation/start-a-project.md).

## Inspect and agree

1. Check Python 3.9+, Git, target path, existing code/instructions, board, kit version and requested hosts. Use an existing Git repository or obtain authorization to initialize one. If a prerequisite is absent, report the exact missing dependency, recovery action and untouched state; resume after it is available.
2. Identify the installed mode. `project/settings.json` selects the current module layout. A root `project.json` or a separate `project/kanban/workflow.json` identifies an older layout. Preserve the installed mode and workflows on upgrades unless the User explicitly requests and approves a migration.
3. On initial installation, offer express or custom setup. Agree on the module names and workspaces. A simple project can start with the `misc` module alone.
4. Use [workflow setup](configure-workflow.md) to agree on stages, transitions, WIP, journal owner/timezone, delivery evidence and selection policy for the selected layout. Establish project Git permissions.
5. Present one concrete proposal with the selected mode, target files/configuration, workflow, options and checks. Obtain approval before copying/configuring. Reuse an already explicit approval. A procedure, preview or copied file is not permission to execute product work.

## Copy and configure the core

Developer performs approved filesystem/Git work. Keep project code, root instructions, records, customizations and unrelated settings. Copy this reusable static package, preserving paths:

| Package | Contents |
| --- | --- |
| `documentation/` | All reader guides and the single connected example set. |
| `agents/` | `index.md`, `VERSION`; canonical `guidelines/`, `actions/`, `setup/`, `roles/`, `templates/`. In roles copy `orchestrator.md`, `writer.md`, `developer.md`, `tester.md`. |
| `agents/tools/` | `manage-kanban-board.py`, `configure-project-modules.py`, `manage-module-delivery.py`, `migrate-rememory.py` and the `kanban/` package. |

Optional procedures ship as reference material; this does not activate tools, agents, alerts or scheduling. Do not copy the kit's project board, Cards, Specs, Batches, dated journals or root project-specific policy.

Merge this entry into the target's `AGENTS.md` without removing its existing instructions:

```markdown
Follow the [Card delivery workflow](agents/actions/deliver-card.md) and [shared working rules](agents/guidelines/working-rules.md). One agent follows authorized Card work in the current chat.
```

Record the approved project ownership, journal conventions and Git permissions there. For Claude Code merge `@AGENTS.md` into root `CLAUDE.md`; Codex reads `AGENTS.md`. [Layout](project-layout.md) describes the resulting structure.

- **Current projects:** configure the module layout in [project settings](project-modules.md). Include `misc` and keep the workflow in the same settings file.
- **Existing single-board projects:** see the [legacy workflow setup](configure-workflow.md).

The Batch setup applies to legacy projects.

For a new setup, apply the preview when it matches the approved proposal. Stop on a discrepancy or changed scope. For upgrades, verify the installed layout. Use the separate [journal migration](project-layout.md#migrate-existing-journals) after reviewing and approving its preview. Record configuration and actual validation results in Rememory.

## Add selected options

| Option | Benefit and dependency | Setup |
| --- | --- | --- |
| Host skills | Explicit KR role discovery in Codex/Claude; core instructions first. | [Skills](skills.md) |
| Batch records/guard | Exact approved scope, candidate acceptance and closure; Git and core board first. | [Batches](batches.md) |
| Claude role check | Best-effort native named-agent path restrictions; shared roles and core Python package first. | [Claude check](claude-role-check.md) |
| Telegram | Alerts when human action is needed or work completes; private confirmed account setup and network. | [Telegram](telegram.md) |

Options can be added later. Run each option's own preview/check before application and verify its result. Do not infer Telegram opt-in/default policy or Codex enforcement that the project has not approved. Copying the scheduled-job procedure installs no scheduler.

## Upgrade and verify

Inventory current paths/version before copying. Compare source and installed bytes with the known distributed revision; preserve custom roles, instructions, adapters, skills, extra files and settings. Merge approved changes deliberately rather than overwrite a directory. Old launch IDs resolve to canonical policies. Never keep competing customized policies unnoticed: reconcile them before claiming successful role migration.

Run board validate/show for the project board and verify its scope filters when modules exist. Check the selected options; a second setup review should recognize the installed mode and require no layout changes. Open a fresh target-project chat and confirm the installed layout, applicable scope and next authorized action. Record each result as verified, awaiting User action, or blocked, with exact recovery steps. Automated tests and simulated alerts do not prove native discovery or real delivery.
