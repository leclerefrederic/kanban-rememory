# Install or upgrade Kanban Rememory

Installing is approved work like any other: a copied file is not permission to execute product work. Human explanations are in [the user guide](../documentation/guide.md#start-a-project).

## Agree

1. Check that Python 3.9+ and Git are available and that the working directory is a Git repository. If it is not, ask for agreement to create one.
2. Read the target's existing instructions and any installed `project/settings.json`. Agree on the modules, the workflow, the WIP limit, the timezone, what counts as delivered and the Git permissions (such as committing on `main` or merging without asking). Group unresolved independent questions and suggest defaults based on the project's actual flow. Ask dependent questions after the answers they rely on. Module IDs are lowercase and include `misc`; a small project can use `misc` alone.
3. Present one proposal (files, settings, checks) and obtain approval before copying anything.

| Workflow | Use when | Stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review precedes delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have their own queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow also has `cancellation` as a terminal stage. `transitions` maps each stage to its permitted destinations; review failures return to development. Suggest a WIP limit of one Card per module for solo work. `version` is the current release number, `0.0.0` for a new project; each published release raises it and tags `vX.Y.Z`. This kit's `project/settings.json` shows the format.

## Install

Copy these, and nothing else from this kit: `documentation/`, `orchestrator/` and `GUARDRAILS.md`, the last only when the target has none. Never copy this kit's Cards, journal, `README.md` or `AGENTS.md`. Add this line to the target's `AGENTS.md`, keeping its instructions:

```markdown
Act as the Orchestrator and follow the [workflow](orchestrator/workflow.md).
```

Write the approved Git permissions as lines under `## Overrides` in the target's `GUARDRAILS.md`, removing the comment markers around that section. For Claude Code, add `@AGENTS.md` to `CLAUDE.md`; Codex reads `AGENTS.md`. Add `__pycache__/` to `.gitignore`. Write the approved settings to a file outside the repository, preview them, then apply the unchanged proposal:

```sh
python3 orchestrator/tools/kr.py init /path/to/settings.json
python3 orchestrator/tools/kr.py init /path/to/settings.json --apply
python3 orchestrator/tools/kr.py validate
```

Then put Git in order: `git branch -m main` when the branch has another name, commit the installation, `git remote add origin URL` when it is missing, and `git push -u origin main`.

Telegram is an option: set it up only if the project approves it, by giving the user [the Telegram guide](../documentation/telegram-setup.md).

## Upgrade

The kit owns `documentation/` and `orchestrator/`; the project owns `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md` and `project/`. Compare the installed kit files with the commit recorded in the journal at the last install or upgrade, and keep any local change. Replace the rest with the new version, remove files the new version no longer ships once unchanged, and leave the project's files alone except for merging a new rule the user approves. Record the new kit commit in the journal.

## Verify

Run `kr validate` and `kr show`. Open a fresh chat in the target and confirm that it names the Orchestrator, the boards and the next authorized action. Check that `GUARDRAILS.md` exists and that `git ls-remote origin main` answers. Record the result and the kit's commit in the journal.
