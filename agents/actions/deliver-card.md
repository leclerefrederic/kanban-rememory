# Deliver a Card

1. Read `project/settings.json` and the latest relevant project Rememory entry. Use the module's Kanban to find existing work and check capacity. Reuse its Card and authorization when resuming.
2. Put the outcome, scope, acceptance criteria and user decisions on one Card. Adjust detail to the work. Use a Card in the owning module when ownership is clear. Use `misc` for work without an owner, including cross-module changes that ship together. List affected modules in `affected_modules` and refer to the Card by stable ID. Use separate Cards for independently deliverable changes and link actual dependencies.
3. For attachments, add a `## Resources` section with a relative link and purpose for each file. Store linked attachments in the module's `resources/<card-id>/` directory. Reference files already in the repository at their existing paths.
4. Once authorized, carry the Card through implementation, diff review and applicable automated checks in the current chat. Investigate failures, fix recoverable issues within scope and rerun the affected checks. Use the relevant skills as guides. Delegate independent work or a focused review only when useful and permitted, with a self-contained handoff.
5. Verify the proposed integration with current `main` in a separate integration worktree. Keep the Card in `development` while waiting for merge approval. Before merging into `main`, show the user the verified revision, what was checked and any automatic production deployment that the merge or push will trigger. Obtain explicit approval for that candidate and record it on the Card. If the proposed integration changes while waiting, verify the updated candidate and obtain approval for it.
6. After approval, carry out the authorized delivery and verify publication and any agreed deployment. Treat the Card as delivered once these steps are verified. Use the [module coordination commands](coordinate-modules.md) to include its closure in the verified publication candidate. Record the verified publication in [Rememory](maintain-rememory.md) when publication is part of delivery.

## Return control to the user

- **Intervention required.** Ask for the specific decision, permission or manual action that only the user can provide. Explain what depends on it and continue independent authorized work where possible. An acceptance decision is an intervention when it was explicitly agreed as part of the delivery.
- **Work complete.** Report the delivered outcome and where to find it after the agreed checks and delivery steps are complete.

Use the existing authorization throughout. Continue directly between steps and handle recoverable failures within the same run. When Remy is configured, follow [the notification triggers](notify-user.md#card-delivery-with-remy) for both kinds of handoff, including a merge approval that is still needed.

Earlier Specs and Batches can be found in the archived project or Git history. Use a Card for new work.
