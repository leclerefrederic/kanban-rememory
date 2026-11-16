# Install or upgrade Kanban Rememory

Installing is approved work: a copied file is not permission to execute product work.

User: put this file and `kanban-rememory-kit-<version>.zip` in the root of your repository, which is on `main` with a clean checkout. Open your agent there and tell it: `Follow INSTALL.md.` The user guide is `kanban-rememory/documentation/guide.md#start-a-project` in the kit.

## Instructions

- Run sections 0 to 5 in order. Finish a section before starting the next. Do not skip, merge or reorder steps.
- A step with no ASK has no choice: do what it says. Never ask the user something the step does not ask.
- STOP = end the installation, tell the user which check failed and what to fix, ask them to rerun it. Do nothing else except delete the temporary folders this procedure created. Before section 4 nothing in TARGET has changed.
- ASK = put the question to the user and wait. Never answer for them. An answer that is not one of the allowed answers is no answer: ask again, once per turn. When several answers of one message are invalid, ask again for all of them in one message.
- TARGET = the repository you run in. Run every command from its root.
- KIT = the absolute path of the folder `kanban-rememory-kit-<version>` inside the folder created in section 0. In every command, replace `KIT`, `DIR` and `KIT_VERSION` by their values: shell variables do not persist between commands.
- KIT_VERSION = the content of `KIT/kanban-rememory/VERSION`, one release number.
- `init` = `python3 KIT/installer/init.py`, the installation script. It shares nothing with `kr`.
- `kr` = `python3 kanban-rememory/orchestrator/tools/kr.py`.
- CONFIG = `kanban-rememory.json` at the root of TARGET. It holds `name`, `directory`, `modules`, `workflow`, `version` and, installed by this procedure, `kit`.
- DIR = the `directory` in CONFIG; in install mode, the working folder chosen in step 3.
- MODE = `install` when CONFIG is absent, `upgrade` when it exists.
- Write only: `kanban-rememory/`, CONFIG, DIR, `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore`, `.gitattributes`.
- TEMPLATES = `KIT/kanban-rememory/orchestrator/templates`. `.gitignore` and `.gitattributes` there are hidden files: list with `ls -a`.
- Template rule, for a root file and its template in TEMPLATES: the file is absent: copy the template. The file exists: take the template's lines in order, drop each non-blank line that a line of the file equals, drop the leading and trailing blank lines, and collapse each run of blank lines into one. Nothing left: change nothing. Otherwise append what is left to the file. If the file does not end with a newline, add one first. For `AGENTS.md` and `CLAUDE.md` also add one blank line first when the file is not empty.
- NEVER overwrite an existing `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore` or `.gitattributes`.
- NEVER create a repository, a branch or a remote. NEVER push.

## Kit contents

| Item | Role | Install action |
| --- | --- | --- |
| `kanban-rememory/` | procedure, tools, templates, user guide, lean principles, Telegram guide | replace with the folder from KIT |
| `AGENTS.md` | agent entry point | template rule |
| `CLAUDE.md` | Claude Code bridge to `AGENTS.md` | template rule |
| `GUARDRAILS.md` | user rules for the agent | copy the template if absent |
| `.gitignore` | ignores Python caches | template rule |
| `.gitattributes` | line endings | template rule |

`kanban-rememory/` is never edited by the user: replace it as a whole, never merge it.

## 0. Unpack the kit

1. Exactly one `kanban-rememory-kit-*.zip` is in the root of TARGET: `ls kanban-rememory-kit-*.zip` prints one name. Otherwise STOP and say: keep exactly one kit ZIP in the root of the repository, remove the others, and rerun.
2. Unpack it outside TARGET, never inside:

   ```sh
   W=$(mktemp -d)
   unzip -q kanban-rememory-kit-*.zip -d "$W"
   ```

3. KIT = the one folder `$W/kanban-rememory-kit-*`.

`INSTALL.md` and the ZIP are not repository content: never stage them.

## 1. Prerequisites

Run every command, in order, even after a failure: they only read. If any result differs from the expected one: STOP, and list every failing check with its fix below.

| Check | Command | Expected |
| --- | --- | --- |
| Python 3.9+ | `python3 -c "import sys; sys.exit(sys.version_info < (3, 9))"` | exit 0 |
| Git repository | `git rev-parse --is-inside-work-tree` | prints `true` |
| Branch | `git branch --show-current` | prints `main` |
| Clean checkout | `git status --porcelain -- . ':(exclude)INSTALL.md' ':(exclude)kanban-rememory-kit-*.zip'` | prints nothing |
| Remote readable | `git ls-remote origin main` | exit 0, prints one line |
| Remote writable | `git push --dry-run origin main` | exit 0 |
| KIT is a kit | `test -f KIT/kanban-rememory/orchestrator/tools/kr.py && test -f KIT/kanban-rememory/VERSION && test -f KIT/installer/init.py && test -f KIT/kanban-rememory/orchestrator/templates/GUARDRAILS.md` | exit 0 |
| KIT is not TARGET | `test "$(cd KIT && pwd -P)" != "$(pwd -P)"` | exit 0 |
| No foreign `kanban-rememory/` | `test -e kanban-rememory.json \|\| test ! -e kanban-rememory` | exit 0. Otherwise STOP and say: `kanban-rememory/` is not from this kit; move or remove it yourself, commit that, and rerun |

Fixes to give the user, one per failing check:

- Python: install Python 3.9 or later.
- Git repository: run the installation in a Git repository.
- Branch: switch to `main`.
- Clean checkout: commit or stash your changes.
- Remote readable or writable: fix the access to `origin` and the branch `main` there.
- KIT checks: unpack a valid kit ZIP.
- No foreign `kanban-rememory/`: the message in its row.

## 2. Diagnosis

1. Set MODE.
2. Show the plan, with exactly these lines:
   - `MODE`, and `KIT_VERSION`; in upgrade mode also the installed `kit` from CONFIG, or `none` when CONFIG has no `kit`.
   - `kanban-rememory/`: `replaced` in upgrade mode, `created` in install mode.
   - For each of `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `.gitignore`, `.gitattributes`: `created` if absent, `kept` if it exists. Add `, N lines appended` when the template rule appends N non-blank lines. `GUARDRAILS.md` takes no `N`; in install mode add `, permission lines added after your answers` to its `created` or `kept`.
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
   | `modules` | unique IDs of letters `a-z`, digits and single `-` or `_` between them; `misc` is always in the JSON list, as the last item, even if the user does not name it | none: the list is `["misc"]` |
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
     - Use this folder: run the four checks below from the root of TARGET. A check on `DIR/modules` that prints `No such file or directory` passes: that folder does not exist yet. Any output is a path that `kr validate` would reject: show the paths, then treat the answer as `Another name`: ASK for the name and check it again here, with no `Confirm?`. With no output, list the folders that will be created in it (`rememory/`, and for every module and stage `modules/<module>/<stage>/`, plus `modules/<module>/resources/`), then ASK `Confirm? yes / no`. `yes`: accept. `no`: ASK `Which folder name?` and check it again here.

       | Check | Command (`DIR` = the folder; list the allowed names in the `-name` tests: every module, `misc` included, then every stage of the chosen workflow plus `resources`) | Expected |
       | --- | --- | --- |
       | Only chosen modules | `find DIR/modules -mindepth 1 -maxdepth 1 -not -name '.*' -not -name <module> ...` | no output |
       | Only stages and `resources` | `find DIR/modules -mindepth 2 -maxdepth 2 -not -name '.*' -not -name <stage> ... -not -name resources` | no output |
       | No Markdown file in a stage | `find DIR/modules -mindepth 3 -maxdepth 3 -name '*.md'` | no output |
       | No symbolic link | `find DIR -type l` | no output |
   - Repeat until a folder is accepted.
4. Build the proposal:
   - The CONFIG content, as JSON in this key order: `name`, `directory`, `modules`, `workflow`, `version`, `kit`. `version` = `0.0.0`. `kit` = KIT_VERSION. `workflow` = an object with these keys in this order: `stages` (list), `active` (list), `completed` (the string `completion`), `wip_limit` (integer), `timezone` (string), `transitions` (object: stage → list of the stages it may move to), from the table below. Every list in `transitions` ends with `cancellation`. `completion` and `cancellation` have no key in `transitions`. The first stage is `backlog`, and `cancellation` is the last stage and ends the board.
   - The permission lines for `GUARDRAILS.md`.
   - The lines added to `.gitignore` (`__pycache__/`) and `.gitattributes` (`* text=auto`).
5. Write the CONFIG content to `proposal.json` in a new folder outside TARGET (`mktemp -d`). Run `init <that path>` from the root of TARGET: a preview that writes nothing. Expected: exit 0. A non-zero exit: show the message, ASK the user for a corrected answer to the field it names, rebuild the file and rerun the preview until it exits 0.
6. Show the proposal and the preview output. ASK: `Approve this proposal? yes / no`. `yes`: continue. `no`: STOP.

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

   Upgrade mode: then set `kit` in CONFIG to KIT_VERSION, adding the key after `version` if absent. Edit the text in place: insert or replace that one line and keep every other byte of CONFIG, formatting included. Do not parse and rewrite the file.
2. `AGENTS.md`: template rule, with `TEMPLATES/AGENTS.md`.
3. `CLAUDE.md`: template rule, with `TEMPLATES/CLAUDE.md`.
4. `GUARDRAILS.md`: copy `TEMPLATES/GUARDRAILS.md` to `GUARDRAILS.md` if absent. Install mode, when the user approved Git permissions: add each as one line, with no bullet, under `## Standing permissions`: after the comment block that follows that heading, one blank line, then the lines. If the file has no such heading, append a blank line, the heading, a blank line and the lines at the end.
5. `.gitignore`: template rule, with `TEMPLATES/.gitignore`.
6. `.gitattributes`: template rule, with `TEMPLATES/.gitattributes`.
7. Install mode: run `init <the path of proposal.json> --apply` alone, not piped into another command, so that its exit code is visible. Expected: exit 0 and the last line `Project modules are ready.`
8. Commit. Stage the paths of the write scope that exist, then commit without pushing:

   ```sh
   git add kanban-rememory kanban-rememory.json AGENTS.md CLAUDE.md GUARDRAILS.md .gitignore .gitattributes DIR
   git commit -m "Install Kanban Rememory KIT_VERSION"
   ```

   Replace `DIR` and `KIT_VERSION` by their values. `DIR` includes the `.gitkeep` files that `init` creates in empty folders: they are tracked. Upgrade mode: the message is `Upgrade Kanban Rememory to KIT_VERSION`.

## 5. Verification

Run each check. A failure: STOP. The commit stays; the user decides what to do with it.

| Check | Command | Expected |
| --- | --- | --- |
| Boards valid | `kr validate` | exit 0 |
| Tools answer | `kr show` | exit 0 |
| Guardrails | `test -f GUARDRAILS.md` | exit 0 |
| Clean checkout | `git status --porcelain -- . ':(exclude)INSTALL.md' ':(exclude)kanban-rememory-kit-*.zip'` | prints nothing |

Then:

1. ASK: `Open a fresh chat in TARGET. Does it name the Orchestrator, the boards and the next authorized action? yes / no`. `no`: STOP.
2. Journal: in `DIR/rememory/<date>.md`, `<date>` = today (`YYYY-MM-DD`) and `HH:MM` = now (24 hours), both in the project timezone: `TZ=<timezone> date +%F` and `TZ=<timezone> date +%H:%M`, add the entry below under the date heading, above older entries. Create the file with the heading `# <date> (<timezone>)` if absent. Commit it with `Record the Kanban Rememory installation`; do not push.

   ```markdown
   ## HH:MM — Kanban Rememory KIT_VERSION installed

   Mode: MODE. `kr validate` passed. Fresh chat check approved by the user.
   ```

3. ASK: `Delete INSTALL.md and the kit ZIP? yes / no`. `yes`: delete both files. `no`: leave both.
4. Delete the two temporary folders this procedure created outside TARGET: the one of section 0 and the one of `proposal.json`.
5. Report to the user, in this order: MODE, KIT_VERSION, the files written, the commit hashes, and `Nothing is pushed`.

## Option: Telegram

Only if the project approves: give the user `kanban-rememory/documentation/telegram-setup.md`.
