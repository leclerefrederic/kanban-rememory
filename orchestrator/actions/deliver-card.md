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

## Command sequence

Run delivery commands from the delivery worktree. Board moves write the Card in the primary checkout. `OWNER` is the recorded session ID.

```sh
D() { python3 orchestrator/tools/manage-module-delivery.py --scope MODULE "$@"; }
B() { python3 orchestrator/tools/manage-kanban-board.py "$@"; }
D claim CARD-ID --owner OWNER --base MAIN_COMMIT
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
