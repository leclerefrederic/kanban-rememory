# Working instructions

In a normal primary project session, act as [KR Orchestrator](agents/roles/orchestrator.md) and follow its startup procedure. If the session was explicitly started in another role or is a subagent assigned a role, retain that role and read its role instructions instead. This is a workflow default. Follow the host launch mechanism for enforced role checks.

Read the [shared working instructions](agents/guidelines/working-rules.md) before adopting the kit or working on cards.

## Rules for the Kanban Rememory repository

This repository uses its own cards and journal to track changes to the kit. The journal uses Europe/Paris time, and work in progress is limited to one card in Development. Before moving a card to Completion, review the diff and run applicable tests in Development. Select the oldest eligible backlog card by ID unless an agreed priority is documented on the card. Review blockers and flow at closure or before resuming interrupted work. Adapt this section for the target repository.

Publish each verified change to `origin/main` after closing its card. The repository owner has granted standing authorization for these pushes.
