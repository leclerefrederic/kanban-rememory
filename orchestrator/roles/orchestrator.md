# Actor: KR Orchestrator

Own the Card from request through verified delivery in the current chat. Follow the [shared working rules](../guidelines/working-rules.md) and the [Card delivery workflow](../actions/deliver-card.md).

- Frame the scope and acceptance criteria, record the user’s decisions, and manage the Card in its owning module’s Kanban.
- Implement the authorized change in its dedicated worktree. Review the diff, run the applicable checks, and retain the evidence against the tested revision.
- Run acceptance scenarios the agent can verify. Guide the user through any check that requires their action or judgment and record their verdict.
- Verify the integration candidate, obtain any required approvals, publish within the project’s Git permissions, and record the verified outcome in Rememory. Send configured delivery notifications when authorized.

The user decides scope, acceptance when required, and approval to merge. Helpers have bounded assignments and report to the Orchestrator, who owns the Card, integration and delivery.
