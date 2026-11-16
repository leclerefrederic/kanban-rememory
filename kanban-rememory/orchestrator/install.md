# Install or upgrade Kanban Rememory

Installing is approved work: a copied file is not permission to execute product work. User explanations: [the user guide](../documentation/guide.md#start-a-project).

## Instructions

- Execute steps 1 to 5 in order. Finish a step before starting the next.
- STOP = end the installation, report what the user must fix, ask them to rerun it. Modify nothing.
- ASK = ask the user, wait for the answer.
- `kr` = `python3 kanban-rememory/orchestrator/tools/kr.py`, run from the repository root.
- KIT = the kit checkout the user names. Its `kanban-rememory/` folder is the kit; its `AGENTS.md`, `CLAUDE.md` and `GUARDRAILS.md` are the root templates. The `version` in its CONFIG is the kit version.
- CONFIG = `kanban-rememory.json` at the repository root: the project settings (`name`, `modules`, `workflow`, `version`), `directory` (the working folder, `project` by default) and, optional, `kit`.
- DIR = the `directory` in CONFIG; in install mode, the folder chosen in step 3.
- Write only: `kanban-rememory/`, CONFIG, DIR, and lines added to `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` and `.gitattributes`.
- NEVER overwrite an existing `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` or `.gitattributes`. Append the proposal's lines.
- NEVER create a repository, a branch or a remote. NEVER push.

## Kit contents

| Item | Role | Install action |
| --- | --- | --- |
| `kanban-rememory/` | procedure, tools, templates, user guide, lean principles, Telegram guide | replace with the folder from KIT |
| `AGENTS.md` | agent entry point | append workflow line |
| `CLAUDE.md` | Claude Code bridge to `AGENTS.md` | append `@AGENTS.md` |
| `GUARDRAILS.md` | user rules for the agent | copy if absent |

`kanban-rememory/` is never edited by the user: replace it as a whole, never merge it.

## 1. Prerequisites

Any check fails: STOP.

- Python 3.9+ available.
- Git available.
- Working directory is a Git repository.
- Branch `main` exists.
- `git ls-remote origin main` answers.
- `git push --dry-run origin main` succeeds: write access.

## 2. Diagnosis

Set MODE, show the plan to the user and get approval.

- CONFIG absent → MODE = install.
- CONFIG present → MODE = upgrade: an installation exists, and CONFIG gives DIR, the modules and the workflow. The plan says: `kanban-rememory/` is replaced as a whole, or installed when missing; CONFIG and DIR are left as they are, except `kit`.
- List which of `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` and `.gitattributes` exist.
- ASK for approval of the plan. No approval: STOP. Change nothing before approval.

## 3. Decisions

Skip this step when CONFIG exists.

1. Read the target's existing instructions.
2. ASK the user for: project name, modules, workflow, WIP limit, timezone, what counts as delivered, Git permissions (for example: commit on `main`, merge without asking).
   - Group independent questions. Suggest defaults from the project's real flow. Ask a dependent question after the answer it depends on.
   - Module IDs: lowercase, `misc` always included; `misc` alone is valid.
   - WIP limit: 1 Card per module for solo work.
   - Working folder (`directory`): propose `project`. When `project/` or the chosen folder already exists, ASK the user to decide: another name, or that folder, with its content kept. For a merge, first list the folders that will be created in it (`rememory/`, and `modules/<module>/<stage>/` plus `resources/` per module), then ASK to confirm. Repeat until the user names the folder.
3. Present one proposal: the CONFIG content, with `kit` = the `version` in KIT's CONFIG and `directory`, plus the lines added to `.gitignore` (`__pycache__/`) and `.gitattributes` (`* text=auto`).
4. ASK for approval of the proposal. No approval: STOP.

Workflows:

| Workflow | Use when | Stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review precedes delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have their own queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow ends with `cancellation` as a terminal stage. `transitions` maps each stage to its allowed destinations; review failures return to development. `version` = current release, `0.0.0` for a new project; each published release raises it and tags `vX.Y.Z`. Format: this kit's CONFIG.

## 4. Application

Run in this order:

1. `kanban-rememory/`: delete it if present, then copy the folder from KIT, without any `__pycache__/`. In upgrade mode set `kit` in CONFIG to the `version` in KIT's CONFIG.
2. `AGENTS.md`: append, creating the file if absent:

   ```markdown
   Act as the Orchestrator and follow the [workflow](kanban-rememory/orchestrator/workflow.md).
   ```

3. `CLAUDE.md`: append `@AGENTS.md`, creating the file if absent.
4. `GUARDRAILS.md`: copy from KIT if absent. In install mode write the approved Git permissions under `## Overrides`: uncomment that section in the copy, or append it to the user's existing file.
5. `.gitignore`: append `__pycache__/`, creating the file if absent.
6. `.gitattributes`: append `* text=auto`, creating the file if absent.
7. CONFIG and DIR (not in the kit, change over time): generate once, last, only when CONFIG is absent. Write the approved CONFIG content to a file outside the repository, then run:

   ```sh
   python3 kanban-rememory/orchestrator/tools/kr.py init /path/to/proposal.json
   python3 kanban-rememory/orchestrator/tools/kr.py init /path/to/proposal.json --apply
   ```

8. Commit the installation. Do not push: pushing follows normal delivery with the user's approval.

## 5. Verification

Record the result in the journal.

- `kr validate` passes.
- `kr show` answers.
- ASK the user to open a fresh chat in the target and check that it names the Orchestrator, the boards and the next authorized action.
- `GUARDRAILS.md` exists.

## Option: Telegram

Only if the project approves: give the user [the Telegram guide](../documentation/telegram-setup.md).
