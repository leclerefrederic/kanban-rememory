# Agent operating instructions

This directory contains execution instructions for AI agents. Human-facing explanations live in `docs/guides/`; document templates live in `docs/templates/`.

Keep these audiences separate when maintaining documentation: reader guides explain what happens and why; agent procedures specify how to execute it. Both apply the shared lean principles and approved project rules.

Start with [shared working instructions](work-in-a-project.md) and the applicable role. These procedures implement the project's recorded rules and permissions; they do not grant authorization themselves.

| Operation | Reference |
| --- | --- |
| Apply the shared lean principles | [Agent rules](lean-specifications.md) |
| Install in another repository | [Installation procedure](install-in-a-project.md) |
| Agree on workflow configuration | [Adoption interview](configure-a-project.md) |
| Apply role responsibilities | [Specification Agent](roles/specification-agent.md), [Development Agent](roles/development-agent.md), [User responsibilities](roles/user.md) |
| Operate the board | [Board procedures](kanban/board-guide.md), [Card content](kanban/write-task-cards.md), [software workflow profile](kanban/software-development-workflow.md) |
| Record milestones and handoffs | [Maintain Rememory](maintain-rememory.md) |
| Prepare and validate delivery records | [Batch rules](batches/batch-workflow.md), [worked records](batches/delivery-example.md) |
| Pick up, correct or close a Batch | [Batch operations](batches/start-and-close-batches.md) |
| Resume acceptance or verify closure | [Resume a Batch](batches/resume-a-batch.md) |
| Follow the planned scheduled-job procedure | [Scheduled job](run-scheduled-batch-job.md) |
| Configure optional notifications | [Telegram](configure-telegram.md) |
| Build and run the optional app | [Runner procedure](runner/build-and-run.md) |

Copy only the required package into an adopting repository as described by the installation procedure.
