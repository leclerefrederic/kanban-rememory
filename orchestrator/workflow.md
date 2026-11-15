# Orchestrator workflow

The Orchestrator carries each Card from request to verified publication in the current chat. The user decides scope, acceptance and merge approval; nothing here grants authorization. Run commands from the checkout root with Python 3.9+ and Git. `kr` stands for `python3 orchestrator/tools/kr.py`.

## Rules

1. **Records.** Each module has a Kanban in `project/modules/<module>/`: one folder per stage, and `resources/<card-id>/` for attachments. A Card is one file with a stable ID, and its folder is its stage. Work without a natural owner, including cross-module work that ships together, goes to `misc` with an `affected_modules` list. `project/settings.json` holds the modules and the workflow. `project/rememory/` is the journal, one file per date.
2. **Intake.** Search with `kr show` and `kr path` before creating a Card. Reuse an existing Card and its authorization. Take the oldest eligible backlog Card unless one records an agreed priority. Unmet prerequisites keep a Card in backlog.
3. **Phase.** Execute only in a phase: one branch `<host>/phase-<number>` of the checkout, delivering one or more Cards of one module with one merge approval. One agent runs one phase at a time. Never change deliverables on `main`. Creating a Card is not execution: outside a phase, create it on `main` and commit it there only when it waits in the backlog; a Card started at once goes to the new phase branch uncommitted. During a phase, create Cards on its branch. `kr` refuses records written elsewhere.
4. **Capacity.** WIP counts started, unfinished Cards, blocked ones included. A blocked Card stays in its stage with the date, the cause and the condition that clears it.
5. **Scope.** Apply [the lean principles](../documentation/lean-specifications.md). Ask about ambiguous user-visible behavior instead of inventing it. Record a scope change on the Card before implementing it. Keep suggestions separate. Stop once the criteria are verified.
6. **History.** Completed and cancelled Cards never change. A correction or a rollback is a successor Card that refers to the original.
7. **Tests.** Test only what changes. Run `test-kr.py` when `kr.py` or `kanban/` changes, and `test-telegram.py` when `telegram.py` changes. Documentation and Card changes need only `validate`, which `check` always runs. Add a test only for behavior that can break something and that nothing covers yet.
8. **Context.** Every call resends the whole context. Batch independent calls. Read file ranges. Show only the tail of test output. Give wide reads and audits to a subagent that returns its conclusion. Record the resumption state on the Card before compacting. Never change the user's host settings without agreement.

## Card content

`kr new` fills [the template](templates/card.md). Write in the conversation language. Keep secrets and unnecessary personal data out.

- **Intake:** an action title, the outcome, the scope and authorization, dependencies or none, observable acceptance criteria and the user's decisions.
- **Active:** `State` only when `waiting` or `blocked`, with `Blocker`; History lines only for the user's decisions.
- **Attachments:** a `## Resources` section that links files in `resources/<card-id>/` or existing repository paths.

Do not copy into the Card what git, the journal or the Telegram ledger keep. The tool writes the stage moves and the approval in History, and age and durations come from them.

## Deliver

```sh
kr show                                   # the phase and the boards
kr new "Title" --module MODULE --body <<'CARD'
- Dependencies: None.
## Expected outcome …
CARD
git switch -c claude/phase-NNN            # NNN: the Card number; the new Card comes along uncommitted
kr start CARD-ID                          # opens the phase, Card in development
# implement and commit
kr check -- python3 orchestrator/tools/test-kr.py
# ask the user to approve the verified revision
kr publish --summary "One line" --approval "The user's words" --notify "Chat name" --language fr
```

- **Create.** `--body` reads the whole Card below its title from stdin, so write it complete in one call. Without `--body`, `new` copies the template.

- **Start.** `start` refuses `main`, a second phase and a full WIP. For a further Card of the phase: `kr move CARD-ID completion`, commit, then `kr start NEXT-ID`.
- **Check.** `check` needs a clean checkout that contains `origin/main`: merge it first. It runs `validate`, lists the CI workflows of `.github/workflows`, then each command given after its own `--`. It records the verified revision only when everything passes. A failure or a new commit cancels the verification, so run every required check in one call. Run the acceptance cases you can verify. Guide the user through those that need them and record the verdict.
- **Approval.** Show the user the verified revision, what was checked and what merging or pushing triggers: read the listed workflows, none means nothing runs. The Card stays in Development until the user approves that exact revision. A changed candidate needs a new check and a new approval. An approval already given in the request, such as "do it and merge", covers the candidate once `check` verifies it within the requested scope: publish without asking again and send no merge alert. Ask again when the check fails or the change exceeds the request.
- **Publish.** `publish` needs the verified revision and every criterion checked. It moves the phase Cards to completion, writes the approval on each and the journal milestone with the durations and token totals. It commits them with the candidate's `Co-Authored-By` trailers, pushes to `origin/main` as a fast-forward, ends the phase, fast-forwards `main` and deletes the branch. `--notify` then sends the Remy delivery alert. After an interruption, rerun `publish`: on an existing closing commit it only publishes. The Card is delivered once publication, and any agreed deployment, is verified.

## Recover

- `kr show` names the active phase and its branch. Before taking it over, confirm that the previous session has stopped, then resume on that branch.
- When `origin/main` has moved, merge it, check again and ask for approval again.
- When records disagree, stop the dependent work and report what disagrees.

## Journal

`publish` writes the publication milestone. Add a manual entry only for a decision, a priority change or a resumption note without a Card. Use `## HH:MM — title` in the project timezone, then one to three lines, newest first under the date heading, committed with the phase. Search the journal by Card ID; do not load every day.

## Return control

- **Intervention required.** Ask for the one decision, permission or action only the user can give. Continue the independent authorized work.
- **Work complete.** Report the delivered outcome and where to find it.

Continue between steps without asking again. When Telegram is configured, also follow [notify](notify.md), including for a pending merge approval.
