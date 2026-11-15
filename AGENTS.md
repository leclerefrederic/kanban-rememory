# Working instructions

Act as the Orchestrator and follow the [Card delivery workflow](orchestrator/actions/deliver-card.md). Separate agents are optional for independent work or focused review.

## Rules for the Kanban Rememory repository

- Each module owns its Kanban and Cards. Use `misc` for Cards without a natural owner, including cross-module changes that ship together.
- Keep one active delivery and one Card in Development per module. Integrate one delivery at a time. Work on a dedicated branch and worktree of this clone.
- Select the oldest eligible backlog Card by ID unless the Card records an agreed priority.
- Use Europe/Paris time. Settings and workflow: `project/settings.json`. Journal: `project/rememory/`, one file per date.
- Pushing `main` runs the GitHub Telegram setup tests when their files change; it triggers no production deployment. Recheck `.github/workflows/` before asking for merge approval.
- After the user's explicit approval of the verified candidate, close the Card and publish to `origin/main` under the repository owner's standing push authorization.
