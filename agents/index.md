# Agent instruction router

This is internal execution machinery. Human explanations live in `documentation/`. Start from the project's `AGENTS.md`, [shared rules](guidelines/working-rules.md) and the [Card delivery workflow](actions/deliver-card.md). Load the relevant task below. Procedures never grant authorization.

| Task | Load |
| --- | --- |
| Apply approval principles | [Operational lean rules](guidelines/lean-specifications.md) |
| Deliver a Card in the current chat | [Card delivery](actions/deliver-card.md) |
| Create or move Cards | [Kanban invariants](guidelines/kanban.md), [content](actions/write-card.md), [commands](actions/manage-board.md) |
| Coordinate a module delivery | [Module coordination](actions/coordinate-modules.md) |
| Record a milestone | [Rememory](actions/maintain-rememory.md) |
| Consult an existing Batch | [Batch invariants](guidelines/batches.md); [develop](actions/develop-batch.md) or [close](actions/close-batch.md) for that phase |
| Consult historical Batch acceptance | [Tester](roles/tester.md#run-and-guide-acceptance) |
| Resume an assignment | [Resume](actions/resume-work.md) |
| Send configured alerts | [Notify](actions/notify-user.md) |
| Adopt or upgrade | [Install](setup/install.md) |
| Inspect planned scheduling | [Scheduled procedure](actions/scheduled-batch-job.md), not an installed scheduler |

`guidelines/` owns invariant rules; `actions/` ordered execution; `setup/` installation/configuration; `roles/` authority; `hosts/` native adapters; `skills/` minimal discovery routes; `templates/` blank records; `tools/` executables.
