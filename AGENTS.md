# Working instructions

Own the Card from framing through authorized publication in the current chat. Follow the [Card delivery workflow](agents/actions/deliver-card.md) and the [shared working instructions](agents/guidelines/working-rules.md). Use the existing skills as task guides as needed. Separate agents are optional for independent work or focused review.

## Rules for the Kanban Rememory repository

Each module owns its Kanban and Cards. Use `misc` for Cards without a natural owning module, including cross-module changes that must ship together. Record affected modules and link to the same Card by its stable ID. Keep one active delivery per scope and one Card in Development per scope. Work on dedicated branches and worktrees of the same clone. Integrate one delivery at a time. Before moving a Card to Completion, review the diff and run the applicable checks in Development. Select the oldest eligible backlog Card by ID unless an agreed priority is documented on it. Review blockers and flow at closure or before resuming interrupted work.

Use Europe/Paris time. Record one concise milestone for each verified publication in the project journal. Keep one project journal in `project/rememory/` with one file per date. Link milestones and useful resumption notes to the relevant Cards. Use `project/settings.json` for project settings and the shared workflow.

Before merging a Card into `main`, obtain the user's explicit approval for the verified candidate. Identify any automatic production deployment triggered by merging or pushing `main`. After approval, close the Card and publish to `origin/main` under the repository owner's standing push authorization.
