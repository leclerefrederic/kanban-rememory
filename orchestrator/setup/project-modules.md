# Configure project modules

`project/settings.json` holds the project identity, module workspaces, execution policy, the embedded `workflow` and `last_card_id`. Use lowercase module IDs and include `misc`. Each module has its stage directories and `resources/` directly in its workspace. The journal is flat under `project/rememory/`.

## Choose the workflow

Ask only unresolved questions, one at a time, and suggest answers from the project's actual flow. Recommend the shortest template that shows the real queues.

| Template | Use when | Ordered stages | Active |
| --- | --- | --- | --- |
| Short | One agent makes and checks a change. | backlog → development → completion | development |
| Standard | A distinct review happens before delivery. | backlog → development → code-review → completion | development, code-review |
| Long | Preparation, verification and release have distinct queues. | backlog → refinement → development → code-review → testing → deployment → completion | development, code-review, testing, deployment |

Every workflow also has `cancellation` as a separate terminal stage. The setup tool requires backlog first (it is the intake stage), development as the first active stage, completion as the delivery stage and cancellation as a terminal stage. Review failures return to development without resetting the start date. Suggest a WIP limit of one Card per module for solo work. A project may finish at merge, deployment or explicit acceptance; record which.

Workflow fields: ordered `stages`, WIP-counted `active`, delivery `completed`, positive `wip_limit`, IANA `timezone`, and the required `transitions` mapping each source stage to its permitted destinations. Set `last_card_id` to zero for a new project, or to the last assigned number if earlier Cards were removed.

## Apply and verify

From the target's primary checkout, preview the approved settings, then apply the unchanged proposal:

```sh
python3 orchestrator/tools/configure-project-modules.py /path/to/proposed-settings.json
python3 orchestrator/tools/configure-project-modules.py /path/to/proposed-settings.json --apply
python3 orchestrator/tools/manage-kanban-board.py validate
python3 orchestrator/tools/manage-kanban-board.py show --scope misc
```

Stop on any difference from the approved proposal. Record the approval and check results in Rememory.
