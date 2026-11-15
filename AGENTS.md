# Working instructions

In a normal primary project session, act as [KR Orchestrator](agents/roles/orchestrator.md) and follow its startup procedure. If the session was explicitly started in another role or is a subagent assigned a role, retain that role and read its role instructions instead. This is a workflow default. Follow the host launch mechanism for enforced role checks.

Read the [shared working instructions](agents/guidelines/working-rules.md) before adopting the kit or working on cards.

## Rules for the Kanban Rememory repository

This repository tracks Cards on one project Kanban. Each Card names its owning module or project scope. Keep one active delivery per scope and one Card in Development per scope. Work on dedicated branches and worktrees of the same clone. Integrate one delivery at a time. Before moving a Card to Completion, review the diff and run the applicable checks in Development. Select the oldest eligible backlog Card by ID unless an agreed priority is documented on it. Review blockers and flow at closure or before resuming interrupted work.

Use Europe/Paris time. Record one concise milestone for each verified publication in the project journal. Keep durable module rationale and resumption notes in the module journal when useful. Link to the original Card, Spec, Batch or evidence. The records from before the multi-module cutover are stored locally under ignored `Archives/`. Project Rememory links to their version in Git history.

Publish each verified change to `origin/main` after closing its card. The repository owner has granted standing authorization for these pushes.
