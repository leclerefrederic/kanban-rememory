# Install or upgrade Kanban Rememory

Installing is approved work: a copied file is not permission to execute product work. User explanations: [the user guide](../documentation/guide.md#start-a-project).

## Instructions

- Run sections 1 to 5 in order. Finish a section before starting the next. Do not skip, merge or reorder steps.
- A step with no ASK has no choice: do what it says. Never ask the user something the step does not ask.
- STOP = end the installation, tell the user which check failed and what to fix, ask them to rerun it. Do nothing else. Before section 4 nothing has changed.
- ASK = put the question to the user and wait. Never answer for them. An answer that is not one of the allowed answers is no answer: ask again, once per turn.
- TARGET = the repository you run in. Run every command from its root.
- KIT = the unpacked kit ZIP whose path the user gave. If they gave none, ASK for it.
- GUARDRAILS_TEMPLATE = `KIT/kanban-rememory/orchestrator/templates/GUARDRAILS.md`.
- KIT_VERSION = the content of `KIT/kanban-rememory/VERSION`, one release number.
- `kr` = `python3 kanban-rememory/orchestrator/tools/kr.py`.
- CONFIG = `kanban-rememory.json` at the root of TARGET. It holds `name`, `directory`, `modules`, `workflow`, `version` and, installed by this procedure, `kit`.
- DIR = the `directory` in CONFIG; in install mode, the working folder chosen in step 3.
- MODE = `install` when CONFIG is absent, `upgrade` when it exists.
- Write only: `kanban-rememory/`, CONFIG, DIR, `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore`, `.gitattributes`.
- Add-line rule: append the line at the end of the file, on its own line, unless an identical line already exists in it. Create the file if absent.
- NEVER overwrite an existing `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` or `.gitattributes`.
- NEVER create a repository, a branch or a remote. NEVER push.

## Kit contents

| Item | Role | Install action |
| --- | --- | --- |
| `kanban-rememory/` | procedure, tools, templates, user guide, lean principles, Telegram guide | replace with the folder from KIT |
| `AGENTS.md` | agent entry point | add-line rule |
| `CLAUDE.md` | Claude Code bridge to `AGENTS.md` | add-line rule |
| `GUARDRAILS.md` | user rules for the agent | copy GUARDRAILS_TEMPLATE if absent |

`kanban-rememory/` is never edited by the user: replace it as a whole, never merge it.

## 1. Prerequisites

Run each command. A result other than the expected one: STOP.

| Check | Command | Expected |
| --- | --- | --- |
| Python 3.9+ | `python3 -c "import sys; sys.exit(sys.version_info < (3, 9))"` | exit 0 |
| Git repository | `git rev-parse --is-inside-work-tree` | prints `true` |
| Branch | `git branch --show-current` | prints `main` |
| Clean checkout | `git status --porcelain -- . ':(exclude)START.md' ':(exclude)kanban-rememory-kit-*.zip'` | prints nothing |
| Remote readable | `git ls-remote origin main` | exit 0, prints one line |
| Remote writable | `git push --dry-run origin main` | exit 0 |
| KIT is a kit | `test -f KIT/kanban-rememory/orchestrator/tools/kr.py && test -f KIT/kanban-rememory/VERSION && test -f GUARDRAILS_TEMPLATE` | exit 0 |
| KIT is not TARGET | `test "$(cd KIT && pwd -P)" != "$(pwd -P)"` | exit 0 |

## 2. Diagnosis

1. Set MODE.
2. Show the plan, with exactly these lines:
   - `MODE`, and `KIT_VERSION`; in upgrade mode also the installed `kit` from CONFIG, or `none` when CONFIG has no `kit`.
   - `kanban-rememory/`: `replaced` if it exists, `created` if not.
   - For each of `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore`, `.gitattributes`: `created` if absent, `kept, lines appended` if it exists (`kept` alone for `GUARDRAILS.md` in upgrade mode).
   - Install mode: `CONFIG and DIR created after your answers`. Upgrade mode: `CONFIG: only kit changes; DIR left as it is`.
   - `One commit on main. Nothing is pushed.`
3. ASK: `Approve this plan? yes / no`. `yes`: continue. `no`: STOP.

## 3. Decisions

Upgrade mode: skip this section.

1. Read `AGENTS.md`, `CLAUDE.md` and `GUARDRAILS.md` of TARGET if they exist. Use them only to propose defaults; the user's answers win.
2. ASK all questions below in one message. The user may answer `default` for any field that has one.

   | Field | Allowed answer | Default |
   | --- | --- | --- |
   | `name` | one line of text | the name of TARGET's folder |
   | `modules` | unique IDs of letters `a-z`, digits and single `-` or `_` between them; `misc` is always added | `misc` only |
   | workflow | `Short`, `Standard` or `Long` (table below). Ask what counts as delivered to choose: publication only fits Short or Standard; testing or deployment after publication fits Long | `Short` |
   | WIP limit | a positive integer | `1` |
   | timezone | an IANA name such as `Europe/Paris` | none: required |
   | Git permissions | zero or more one-line permissions, such as `Commit on main without asking` | none |
   | working folder (`directory`) | one folder name: letters, digits, `-`, `_`, not starting with `-` or `_`, not `kanban-rememory` | `project` |

3. Working folder, checked after the answer:
   - It does not exist: accept it.
   - It exists as a file: refuse it, ASK for another name.
   - It exists as a folder: ASK `Use another name, or use this folder and keep its content?`.
     - Another name: ASK for the name, then check it again here.
     - Use this folder: list the folders that will be created in it (`rememory/`, and for every module and stage `modules/<module>/<stage>/`, plus `modules/<module>/resources/`), then ASK `Confirm? yes / no`. `yes`: accept. `no`: ASK `Which folder name?` and check it again here.
   - Repeat until a folder is accepted.
4. Build the proposal:
   - The CONFIG content, as JSON in this key order: `name`, `directory`, `modules`, `workflow`, `version`, `kit`. `version` = `0.0.0`. `kit` = KIT_VERSION. `workflow` = `stages`, `active`, `completed` = `completion`, `wip_limit`, `timezone`, `transitions`, from the table below; every transition list ends with `cancellation`. The first stage is `backlog`, and `cancellation` is the last stage and ends the board.
   - The permission lines for `GUARDRAILS.md`.
   - The lines added to `.gitignore` (`__pycache__/`) and `.gitattributes` (`* text=auto`).
5. ASK: `Approve this proposal? yes / no`. `yes`: continue. `no`: STOP.

| Workflow | Stages | Active | Transitions (each also allows `cancellation`) |
| --- | --- | --- | --- |
| Short | backlog, development, completion, cancellation | development | backlog → development; development → completion |
| Standard | backlog, development, code-review, completion, cancellation | development, code-review | backlog → development; development → code-review; code-review → completion, development |
| Long | backlog, refinement, development, code-review, testing, deployment, completion, cancellation | development, code-review, testing, deployment | backlog → refinement; refinement → development; development → code-review; code-review → testing, development; testing → deployment, development; deployment → completion, development |

`version` is the current release of the project: each published release raises it and tags `vX.Y.Z`.

## 4. Application

Run in this order. A failing command: STOP and report the command and its output; do not undo earlier steps.

1. `kanban-rememory/`:

   ```sh
   rm -rf kanban-rememory
   cp -R KIT/kanban-rememory kanban-rememory
   find kanban-rememory -name __pycache__ -type d -prune -exec rm -rf {} +
   ```

   Upgrade mode: then set `kit` in CONFIG to KIT_VERSION, adding the key after `version` if absent. Change nothing else in CONFIG.
2. Install mode: write the approved CONFIG content to `proposal.json` in a new folder outside TARGET (`mktemp -d`). Then run `kr init <that path>` (preview). Expected: exit 0. A non-zero exit: show the message, ASK the user for a corrected answer to the field it names, rebuild the file and rerun the preview until it exits 0.
3. `AGENTS.md`: add-line rule, with:

   ```markdown
   Act as the Orchestrator and follow the [workflow](kanban-rememory/orchestrator/workflow.md).
   ```

4. `CLAUDE.md`: add-line rule, with `@AGENTS.md`.
5. `GUARDRAILS.md`: copy GUARDRAILS_TEMPLATE to `GUARDRAILS.md` if absent. Install mode, when the user approved Git permissions: add each as one line under `## Standing permissions`, after the comment block that follows that heading. If the file has no such heading, append the heading and the lines at the end.
6. `.gitignore`: add-line rule, with `__pycache__/`.
7. `.gitattributes`: add-line rule, with `* text=auto`.
8. Install mode: run `kr init <that path> --apply`. Expected: exit 0 and the last line `Project modules are ready.`
9. Commit. Stage the paths of the write scope that exist, then commit without pushing:

   ```sh
   git add kanban-rememory kanban-rememory.json AGENTS.md CLAUDE.md GUARDRAILS.md .gitignore .gitattributes DIR
   git commit -m "Install Kanban Rememory KIT_VERSION"
   ```

   Replace `DIR` and `KIT_VERSION` by their values. Upgrade mode: the message is `Upgrade Kanban Rememory to KIT_VERSION`.

## 5. Verification

Run each check. A failure: STOP. The commit stays; the user decides what to do with it.

| Check | Command | Expected |
| --- | --- | --- |
| Boards valid | `kr validate` | exit 0 |
| Tools answer | `kr show` | exit 0 |
| Guardrails | `test -f GUARDRAILS.md` | exit 0 |
| Clean checkout | `git status --porcelain -- . ':(exclude)START.md' ':(exclude)kanban-rememory-kit-*.zip'` | prints nothing |

Then:

1. ASK: `Open a fresh chat in TARGET. Does it name the Orchestrator, the boards and the next authorized action? yes / no`. `no`: STOP.
2. Journal: in `DIR/rememory/<date>.md`, `<date>` = today in the project timezone (`YYYY-MM-DD`), add the entry below under the date heading, above older entries. Create the file with the heading `# <date> (<timezone>)` if absent. Commit it with `Record the Kanban Rememory installation`; do not push.

   ```markdown
   ## HH:MM — Kanban Rememory KIT_VERSION installed

   Mode: MODE. `kr validate` passed. Fresh chat check approved by the user.
   ```

3. Report to the user, in this order: MODE, KIT_VERSION, the files written, the commit hashes, and `Nothing is pushed`.

## Option: Telegram

Only if the project approves: give the user [the Telegram guide](../documentation/telegram-setup.md).
