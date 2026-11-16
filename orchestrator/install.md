# Install or upgrade Kanban Rememory

Installing is approved work: a copied file is not permission to execute product work. User explanations: [the user guide](../documentation/guide.md#start-a-project).

## Instructions

- Execute steps 1 to 5 in order. Finish a step before starting the next.
- STOP = end the installation, report what the user must fix, ask them to rerun it. Modify nothing.
- ASK = ask the user, wait for the answer.
- Act only on the gaps listed in step 2 and approved in step 3.
- Write only: kit items, `project/`, lines added to `.gitignore` and `.gitattributes`.
- NEVER overwrite an existing `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` or `.gitattributes`. Append the proposal's lines.
- NEVER create a repository, a branch or a remote. NEVER push.

## Kit contents

| Item | Role | Install action |
| --- | --- | --- |
| `orchestrator/` | procedure, tools, templates | copy |
| `documentation/` | user guide, lean principles, Telegram guide | copy |
| `AGENTS.md` | agent entry point | append workflow line |
| `CLAUDE.md` | Claude Code bridge to `AGENTS.md` | append `@AGENTS.md` |
| `GUARDRAILS.md` | user rules for the agent | copy if absent |

## 1. Prerequisites

Any check fails: STOP.

- Python 3.9+ available.
- Git available.
- Working directory is a Git repository.
- Branch `main` exists.
- `git ls-remote origin main` answers.

## 2. Diagnosis

Build the gap table, one row per element, state = `absent` | `identical` | `different`. Show it to the user: it is the plan.

| Element | Compare with the kit |
| --- | --- |
| `orchestrator/`, `documentation/` | each file |
| `AGENTS.md` | workflow line present |
| `CLAUDE.md` | `@AGENTS.md` present |
| `GUARDRAILS.md` | file exists |
| `.gitignore` | `__pycache__/` listed |
| `.gitattributes` | `* text=auto` present |

## 3. Decisions

1. Read the target's existing instructions.
2. ASK the user for: modules, workflow, WIP limit, timezone, what counts as delivered, Git permissions (for example: commit on `main`, merge without asking).
   - Group independent questions. Suggest defaults from the project's real flow. Ask a dependent question after the answer it depends on.
   - Module IDs: lowercase, `misc` always included; `misc` alone is valid.
   - WIP limit: 1 Card per module for solo work.
3. Present one proposal: files to copy or append, settings, checks, lines added to `.gitignore` (`__pycache__/`) and `.gitattributes` (`* text=auto`).
4. No approval: STOP. Copy nothing before approval.

Workflows:

| Workflow | Use when | Stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review precedes delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have their own queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow ends with `cancellation` as a terminal stage. `transitions` maps each stage to its allowed destinations; review failures return to development. `version` = current release, `0.0.0` for a new project; each published release raises it and tags `vX.Y.Z`. Format: this kit's `project/settings.json`.

## 4. Application

Run in this order, for the rows of the gap table only:

1. `orchestrator/`, `documentation/`: copy absent files. For each `different` file, show the `diff`; the user keeps theirs or takes the kit's.
2. `AGENTS.md`: append, creating the file if absent:

   ```markdown
   Act as the Orchestrator and follow the [workflow](orchestrator/workflow.md).
   ```

3. `CLAUDE.md`: append `@AGENTS.md`, creating the file if absent.
4. `GUARDRAILS.md`: copy if absent. Write the approved Git permissions under `## Overrides` and remove the comment markers around that section.
5. `.gitignore`: append `__pycache__/`, creating the file if absent.
6. `.gitattributes`: append `* text=auto`, creating the file if absent.
7. `project/` (not in the kit, changes over time): generate once, last. Write the approved settings to a file outside the repository, then run:

   ```sh
   python3 orchestrator/tools/kr.py init /path/to/settings.json
   python3 orchestrator/tools/kr.py init /path/to/settings.json --apply
   ```

8. Commit the installation. Do not push: pushing follows normal delivery with the user's approval.

## 5. Verification

Record the result in the journal.

- `kr validate` passes.
- `kr show` answers.
- A fresh chat in the target names the Orchestrator, the boards and the next authorized action.
- `GUARDRAILS.md` exists.

## Option: Telegram

Only if the project approves: give the user [the Telegram guide](../documentation/telegram-setup.md).
