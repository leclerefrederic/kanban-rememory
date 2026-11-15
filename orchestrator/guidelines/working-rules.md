# Shared working rules

Follow the [operational lean rules](lean-specifications.md) and the project’s root instructions. Reuse the user’s authorization where it covers the next action. Record scope, execution authority, verification and user decisions on the Card.

1. Read `project/settings.json`, the owning module’s Kanban and the latest relevant entry in `project/rememory/`. Reuse the existing Card and confirm ownership, dependencies and capacity before starting or resuming it.
2. The [Orchestrator](../roles/orchestrator.md) owns the Card from intake through verified delivery. Follow [Card delivery](../actions/deliver-card.md) and use the [router](../index.md) to load the next action. Independent helpers can contribute within their assignment and host permissions. The Orchestrator keeps ownership and verifies the combined result.
3. Review the candidate before asking for approval. Record required user acceptance and merge approval against the verified revision. Follow the project’s Git and deployment permissions.
4. Record verified publication in the [project journal](../actions/maintain-rememory.md). Review blocked work and delivery flow at closure or resumption.

For installations explicitly using separate roles or an older Batch workflow, load the [legacy rules](legacy-roles.md).
