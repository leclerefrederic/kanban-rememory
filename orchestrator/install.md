# Install or upgrade Kanban Rememory

Installing is approved work like any other: a copied file is not permission to execute product work. Human explanations are in [the user guide](../documentation/guide.md#start-a-project).

## Agree

1. Check Python 3.9+, Git, the target repository or the authorization to create one, its existing instructions and the `schema_version` of any installed `project/settings.json`.
2. Agree on the modules, the workflow, the WIP limit, the timezone, what counts as delivered and the Git permissions. Group unresolved independent questions and suggest defaults based on the project's actual flow. Ask dependent questions after the answers they rely on. Module IDs are lowercase and include `misc`; a small project can use `misc` alone.
3. Present one proposal (files, settings, checks) and obtain approval before copying anything.

| Workflow | Use when | Stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review precedes delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have their own queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow also has `cancellation` as a terminal stage. `transitions` maps each stage to its permitted destinations; review failures return to development. Suggest a WIP limit of one Card per module for solo work. `version` is the current release number, `0.0.0` for a new project; each published release raises it and tags `vX.Y.Z`. `last_card_id` is the floor of new Card IDs: zero for a new project, or the last assigned number when Cards were removed. This kit's `project/settings.json` shows the format.

## Install

Copy `documentation/` and `orchestrator/`, not this kit's Cards, journal or `AGENTS.md`. Add this line to the target's `AGENTS.md`, keeping its instructions, and record the project's Git permissions there:

```markdown
Act as the Orchestrator and follow the [workflow](orchestrator/workflow.md).
```

For Claude Code, add `@AGENTS.md` to `CLAUDE.md`; Codex reads `AGENTS.md`. Add `__pycache__/` to `.gitignore`. Write the approved settings to a file outside the repository, preview them, then apply the unchanged proposal:

```sh
python3 orchestrator/tools/kr.py init /path/to/settings.json
python3 orchestrator/tools/kr.py init /path/to/settings.json --apply
python3 orchestrator/tools/kr.py validate
```

Telegram is an option: set it up only if the project approves it, by giving the user [the Telegram guide](../documentation/telegram-setup.md).

## Upgrade

Inventory the installed paths. Merge the approved changes without overwriting project customizations. Remove files the new version no longer ships only after checking that they are unchanged.

From settings schema 1, finish the active delivery first. Then rewrite `project/settings.json` as schema 2: `name` from `project.name`, the module IDs as the `modules` list, `workflow` and `last_card_id` unchanged, `version` set to `0.0.0`, without `board_layout`, `shared` and `execution`. The boards stay in `project/modules/<module>/`.

## Verify

Run `kr validate` and `kr show`. Open a fresh chat in the target and confirm that it names the Orchestrator, the boards and the next authorized action. Record the result in the journal.
