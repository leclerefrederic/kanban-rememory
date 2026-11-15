# Configure the workflow

Use when adopting a new board or explicitly migrating policy. [Installation](install.md) owns the approval/copy sequence. Preserve an existing workflow unless the User approved its migration. Ask only unresolved questions, one at a time; suggest answers from the project's actual task flow.

## Choose the policy

Use the mode agreed in [installation](install.md#inspect-and-agree) for both express and custom setup. Recommend the shortest template that exposes actual queues/handoffs.

| Template | Use when | Ordered stages | Active |
| --- | --- | --- | --- |
| Short | One person makes and checks a change. | backlog → development → completion | development |
| Standard | Distinct review before delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have distinct queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

All include Cancellation for abandonment. New/custom boards require backlog first, development first active, completion as delivery and cancellation as a separate terminal stage. Existing configurations remain supported until explicitly migrated. Work starts entering development; blocked active work counts toward WIP. Suggest one active Card for solo work; confirm the team's limit and selection policy.

For custom choices, walk a real change from request to usable delivery: where it waits, who checks it, where failed checks return, start/finish evidence, who authorizes pickup, capacity and priority exceptions. Confirm timezone and journal ownership (single owner defaults to `project/rememory/project/`). Carry express answers forward rather than repeat the interview.

Define entry/exit criteria and allowed rework moves. Short verifies in Development; Standard/Long return review failures to Development without resetting start. Long enters Refinement with clear outcome/checks/prerequisites, Testing after review, Deployment after pre-release checks, and Completion only after required delivery evidence. A project may finish at merge, deployment or explicit acceptance; distinguish these facts.

Present stage order/folders, transitions, active stages/WIP, timezone, ownership and finish evidence in the concrete adoption/migration proposal. Obtain the User's approval through the installation/current project workflow before applying it.

## Apply and verify

The commands below set up a single-project board. For multi-module installation, use the agreed workflow JSON with [module setup](project-modules.md).

From the approved target repository, preview the exact selected configuration:

```sh
python3 orchestrator/tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris
```

Substitute agreed values. For custom setup use a separately prepared approved JSON file:

```sh
python3 orchestrator/tools/manage-kanban-board.py init --config approved-workflow.json
```

Fields: ordered `stages`, WIP-counted `active`, delivery `completed`, positive `wip_limit`, IANA `timezone`, and approved `transitions` mapping each source stage to destination lists. If the preview matches approval, rerun the same command with `--apply`; no second approval is required for an unchanged proposal. Otherwise stop and resolve the discrepancy first.

The tool creates folders, empty-folder `.gitkeep` files and `project/kanban/workflow.json`. For approved [Specification and Batch setup](batches.md), add `--with-batches` to both the preview and application commands. If existing configuration differs or Cards fall outside proposed stages, agree a migration before moving them. Preserve filenames/IDs and affected references.

Record transition/evidence rules in the project's guide/instructions, and ownership/Git permissions in `AGENTS.md`. Create the approved journal folder; do not copy the daily template into it. Run:

```sh
python3 orchestrator/tools/manage-kanban-board.py validate
python3 orchestrator/tools/manage-kanban-board.py show
```

Confirm stage order and capacity match the agreement; record approval, checks and remaining actions in Rememory. [Layout](project-layout.md) describes the result; [Kanban rules](../guidelines/kanban.md) govern subsequent work.
