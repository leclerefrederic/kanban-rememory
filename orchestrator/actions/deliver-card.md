# Deliver a Card

The Orchestrator owns the Card from request to verified delivery in the current chat. The user decides scope, required acceptance and approval to merge. Helpers take bounded, self-contained assignments; the Orchestrator keeps the Card, integration and delivery and verifies the combined result. Procedures never grant authorization.

## Principles

Apply the [lean principles](../../documentation/lean-specifications.md): record who needs what and how it is checked; keep only requirements that earn their place; ask about ambiguous user-visible behavior instead of inventing it; record scope changes on the Card before implementing them; build the simplest thing that meets the criteria and stop once it is verified. Suggestions stay outside the approved scope.

## Steps

1. **Find the work.** Read `project/settings.json` and the latest relevant entry in `project/rememory/`. Search every stage for the Card by stable ID with `path CARD-ID`. Reuse the existing Card and authorization. Never reopen a completed Card; create a successor that refers to it. Before taking over a claimed delivery, confirm the previous session has stopped. Conflicting records stop dependent work; report what disagrees.
2. **Frame the Card.** Record outcome, scope, observable acceptance criteria and user decisions on one Card in the owning module, following [Card content](write-card.md) and the [Kanban rules](../guidelines/kanban.md). Split independently deliverable changes and link real dependencies.
3. **Start.** With explicit authorization, check dependencies and capacity, then run the claim and Development move below.
4. **Build and verify.** Implement in the delivery worktree. Review the diff, run the applicable checks, fix recoverable failures within scope and rerun the affected checks. Run the acceptance cases you can verify; guide the user through agreed cases that need them and record their verdict.
5. **Ask for merge approval.** Verify the candidate against current `main` in a separate integration worktree. Keep the Card in Development. Show the user the verified revision, what was checked and any automatic deployment that merging or pushing `main` triggers. Record their explicit approval on the Card. A changed candidate needs new verification and approval.
6. **Publish.** Complete the Card, build the closing commit, verify it, publish it and record the milestone in [Rememory](maintain-rememory.md). Treat the Card as delivered only after publication and any agreed deployment are verified.

## Phase

A phase is one delivery: one branch, one worktree, one claim, one integration and one merge approval for one or more Cards of a module. Open a phase before any work on a Card; never work directly on `main`, including creating or editing Cards. The branch is `claude/phase-…` or `codex/phase-…`. Run one phase at a time. Cards created during a phase stay on its branch and go through the same merge, which prevents ID collisions.

The claim names the first Card. Add each further backlog Card of the module with `D add-card FIRST_CARD NEXT_CARD --owner OWNER`, then start it with `B move NEXT_CARD development --owner-token OWNER` once the previous Card is in `completion`. Capacity stays one Card in Development. Within a phase a Card moves to `completion` when its criteria are verified on the branch, with its own commit. The merge approval covers the whole candidate. List its Cards and record the approval on each in the closing commit. Closure, publication, milestone and `finish` apply to every Card of the phase, and the journal entry names them all.

## Keep the context small

Every tool call resends the whole context, so cost grows with context size times number of calls. In a long session:

- Record the state a successor needs on the Card (`checkpoint`, History) before compacting, then compact (`/compact` with a focus on the Card in progress) when a Card closes, a phase opens or the context nears about half the window. Hosts also compact automatically near the limit; Codex exposes `model_auto_compact_token_limit` in `config.toml`, which can only lower that trigger.
- Send audits, wide reads and noisy test runs to a separate agent that returns only its conclusion.
- Bound tool output: read file ranges, search precisely, show the tail of test output.
- Batch independent tool calls in one message.
- Keep the files loaded every turn (`AGENTS.md`, `CLAUDE.md`, skills) short; put procedures here.

Do not change a user's personal host settings without their agreement.

## Command sequence

Run delivery commands from the delivery worktree. Board moves write the Card in the primary checkout. `OWNER` is the recorded session ID.

```sh
D() { python3 orchestrator/tools/manage-module-delivery.py --scope MODULE "$@"; }
B() { python3 orchestrator/tools/manage-kanban-board.py "$@"; }
D claim CARD-ID --owner OWNER --base MAIN_COMMIT      # CARD-ID names the phase
D add-card CARD-ID NEXT_CARD --owner OWNER             # optional, per further Card
B move CARD-ID development --owner-token OWNER
D checkpoint CARD-ID --owner OWNER "LABEL"            # at each verified milestone
# implement, commit on the branch, run checks
D integration begin CARD-ID --owner OWNER
# integration worktree at main: merge the branch
D run-check CARD-ID --owner OWNER --integration-checkout PATH -- CHECKS
# ask for approval of that revision; after approval:
B move CARD-ID completion --owner-token OWNER         # all criteria checked
# in the integration worktree, commit the completed Card file and any
# uncommitted journal files from the primary checkout: CLOSING
D run-check CARD-ID --owner OWNER --integration-checkout PATH -- CHECKS
D publish-card CARD-ID --owner OWNER --closing CLOSING
D milestone published CARD-ID --owner OWNER --summary "ONE LINE" --revision CLOSING --published
D integration release CARD-ID --owner OWNER
D finish CARD-ID --owner OWNER --revision CLOSING
```

`publish-card` pushes only the exact verified closing revision and stops if remote `main` moved. Release integration while waiting on a decision or blocker, and reacquire it before resuming. [Module coordination](coordinate-modules.md) covers locks, check isolation and recovery.

## Return control to the user

- **Intervention required.** Ask for the specific decision, permission or manual action only the user can provide. Pause dependent work; continue independent authorized work.
- **Work complete.** Report the delivered outcome and where to find it.

Continue between steps without asking again and handle recoverable failures in the same run. When Remy is configured, follow [the notification triggers](notify-user.md#card-delivery-with-remy), including a pending merge approval.
