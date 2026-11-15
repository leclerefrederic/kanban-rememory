# Agent instruction router

This is internal execution machinery. Human explanations live in `documentation/`. Start from the project's `AGENTS.md`, [shared rules](guidelines/working-rules.md) and assigned [role](roles/); then load only the required task below. Procedures never grant authorization.

| Task | Load |
| --- | --- |
| Apply approval principles | [Operational lean rules](guidelines/lean-specifications.md) |
| Coordinate the current chat | [Orchestrate](actions/orchestrate-work.md) |
| Create or move Cards | [Kanban invariants](guidelines/kanban.md), [content](actions/write-card.md), [commands](actions/manage-board.md) |
| Record a milestone | [Rememory](actions/maintain-rememory.md) |
| Prepare or execute a Batch | [Batch invariants](guidelines/batches.md); [develop](actions/develop-batch.md) or [close](actions/close-batch.md) for that phase |
| Run acceptance | [Tester](roles/tester.md#run-and-guide-acceptance) |
| Resume an assignment | [Resume](actions/resume-work.md) |
| Send configured alerts | [Notify](actions/notify-user.md) |
| Adopt or upgrade | [Install](setup/install.md) |
| Inspect planned scheduling | [Scheduled procedure](actions/scheduled-batch-job.md), not an installed scheduler |

`guidelines/` owns invariant rules; `actions/` ordered execution; `setup/` installation/configuration; `roles/` authority; `hosts/` native adapters; `skills/` minimal discovery routes; `templates/` blank records; `tools/` executables. Four root relays and legacy role/Batch paths exist only for historical/custom references. Do not load them through active routing.
