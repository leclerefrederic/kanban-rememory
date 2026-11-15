# Deliver a Card

1. Read `project/settings.json` and the latest relevant project Rememory entry. Use the module's Kanban to find existing work and check capacity. Reuse its Card and authorization when resuming.
2. Put the outcome, scope, acceptance criteria and user decisions on one Card. Adjust detail to the work. Use a Card in the owning module when ownership is clear. Use `misc` for work without an owner, including cross-module changes that ship together. List affected modules in `affected_modules` and refer to the Card by stable ID. Use separate Cards for independently deliverable changes and link actual dependencies.
3. For attachments, add a `## Resources` section with a relative link and purpose for each file. Store linked attachments in the module's `resources/<card-id>/` directory. Reference files already in the repository at their existing paths.
4. The same agent frames, implements and verifies the authorized scope in the current chat. Use the relevant skills as guides. Review the diff and run applicable automated checks before completion. Record the user's acceptance decision whenever required. Delegate independent work or a focused review only when useful and permitted, with a self-contained handoff.
5. Close the Card and publish under the project's Git permissions. Record the verified publication in [Rememory](maintain-rememory.md). Update the chat at meaningful checkpoints, blockers and delivery.

Earlier Specs and Batches can be found in the archived project or Git history. Use a Card for new work.
