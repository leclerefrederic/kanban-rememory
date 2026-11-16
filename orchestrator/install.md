# Install or upgrade Kanban Rememory

Installing is approved work like any other: a copied file is not permission to execute product work. Human explanations are in [the user guide](../documentation/guide.md#start-a-project).

Each step has an action, an expected result and what to do when it is not met: **STOP** (tell the user what to fix and to rerun the installation) or **ASK**.

The kit is `orchestrator/`, `documentation/`, `CLAUDE.md`, `AGENTS.md` and `GUARDRAILS.md`. `project/` is not part of it: `kr init` creates it with the user.

## 1. Prerequisites

Any failure: **STOP**. Do not create a repository, a branch or a remote.

- [ ] Python 3.9+ is available
- [ ] Git is available
- [ ] The working directory is a Git repository
- [ ] The branch `main` exists
- [ ] `git ls-remote origin main` answers

## 2. Diagnosis

Result: the gap table.

- [ ] Fill one row per element with its state: absent, identical or different
- [ ] Show the table to the user: it is the plan

| Element | Compare with the kit |
| --- | --- |
| `orchestrator/` | each file |
| `documentation/` | each file |
| `AGENTS.md` | the workflow line is present |
| `CLAUDE.md` | `@AGENTS.md` is present |
| `GUARDRAILS.md` | the file exists |
| `project/` | `settings.json`, `modules/` and `rememory/` exist |
| `.gitignore` | `__pycache__/` is listed |

## 3. Decisions

Result: one approved proposal. No approval: **STOP**.

- [ ] Read the target's existing instructions
- [ ] Agree with the user on:
  - [ ] the modules (lowercase IDs, `misc` included; a small project can use `misc` alone)
  - [ ] the workflow (see below)
  - [ ] the WIP limit (one Card per module for solo work)
  - [ ] the timezone
  - [ ] what counts as delivered
  - [ ] the Git permissions, such as committing on `main` or merging without asking
- [ ] Group the independent questions, suggest defaults from the project's real flow, and ask dependent questions after the answers they rely on
- [ ] Present the proposal: files, settings, checks, and the `__pycache__/` line added to their `.gitignore`
- [ ] Obtain the approval before copying anything

| Workflow | Use when | Stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review precedes delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have their own queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow also has `cancellation` as a terminal stage. `transitions` maps each stage to its permitted destinations; review failures return to development. `version` is the current release number, `0.0.0` for a new project; each published release raises it and tags `vX.Y.Z`. This kit's `project/settings.json` shows the format.

## 4. Application

Act only on the rows of the gap table. Never overwrite an existing `AGENTS.md`, `CLAUDE.md` or `GUARDRAILS.md`. Never copy this kit's Cards, journal or `README.md`.

- [ ] `orchestrator/`, `documentation/`: copy the absent files; for each different file, show the `diff` and let the user keep theirs or take the kit's
- [ ] `AGENTS.md`: add the workflow line, creating the file when absent

  ```markdown
  Act as the Orchestrator and follow the [workflow](orchestrator/workflow.md).
  ```

- [ ] `CLAUDE.md`: add `@AGENTS.md`, creating the file when absent (Claude Code reads it; Codex reads `AGENTS.md`)
- [ ] `GUARDRAILS.md`: copy it when absent, then write the approved Git permissions under `## Overrides`, removing the comment markers around that section
- [ ] `project/`: write the approved settings to a file outside the repository, then run

  ```sh
  python3 orchestrator/tools/kr.py init /path/to/settings.json
  python3 orchestrator/tools/kr.py init /path/to/settings.json --apply
  ```

- [ ] `.gitignore`: add `__pycache__/`
- [ ] Commit the installation. Do not push: pushing follows the normal delivery, with the user's approval

## 5. Verification

Result: the installation is proven. Record it in the journal.

- [ ] `kr validate` passes
- [ ] `kr show` answers
- [ ] A fresh chat in the target names the Orchestrator, the boards and the next authorized action
- [ ] `GUARDRAILS.md` exists

## Option: Telegram

Set it up only if the project approves it, by giving the user [the Telegram guide](../documentation/telegram-setup.md).
