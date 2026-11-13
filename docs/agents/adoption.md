# Guided adoption

If `project/kanban/workflow.json` is missing, ask “Would you like to use a ready-made software workflow or build one around your process?”

## Express setup

Present the three templates and recommend the shortest one that makes the user's actual handoffs and queues visible.

| Template | Choose it when | Folders in delivery order | Active stages | Completion evidence |
| --- | --- | --- | --- | --- |
| Short | One person can make and check a small change without a separate handoff. | `backlog` → `development` → `completion` | `development` | Acceptance checks pass and the agreed change is delivered. Record the verified revision or artifact. |
| Standard | A distinct review happens before delivery. | `backlog` → `development` → `code-review` → `completion` | `development`, `code-review` | Required review and checks pass, and the change is merged if merge is the agreed delivery point. |
| Long | Preparation, verification, and release each involve a distinct handoff or queue. | `backlog` → `refinement` → `development` → `code-review` → `testing` → `deployment` → `completion` | `development`, `code-review`, `testing`, `deployment` | Required checks pass, deployment is verified, and any required sign-off is recorded. |

All templates use `archive` for abandoned cards. Work starts when a card enters `development`. Pull the oldest eligible card when execution is authorized and capacity is available. Suggest one active card for solo work and confirm the team's limit. Count blocked cards in active stages.

In Short, record the checks on the card in `development`. In Standard and Long, return cards to `development` if review requests changes. In Long, move work to `refinement` once the outcome, checks, and prerequisites are clear. Move reviewed work to `testing` for separate checks. If a check requires rework, return the card to `development`. When pre-release checks pass, move the card to `deployment` until the required delivery evidence is available. Keep the original start date through rework.

Ask which template fits. If a stage needs adjusting, carry the confirmed answers into the custom interview and ask only about the unresolved choices. Confirm the journal owner and project time zone. Present the resulting workflow for approval before following the shared setup steps below.

## Custom setup

Ask one question at a time. Summarize what you understood before moving on. Offer a suggested answer based on the user's example whenever they are unsure.

1. **Walk through a real task.** Ask “Take a recent change. Where did it start, who picked it up, who checked it, and when could the recipient use it?” If there is no example yet, offer Backlog → Development → Code Review → Completion as a starting point.
2. **Identify queues and rework.** Ask “Where did the work wait, and where did it go when checks failed?” If changes regularly wait after review, propose a separate Deployment stage. If delivery happens at merge, propose moving directly to Completion.
3. **Define the start and finish.** Ask “Which move starts the clock, and what evidence lets us call the work delivered?” Offer concrete choices such as a merged PR, a deployment with a successful check, or acceptance by the requester. Confirm how abandoned work is recorded.
4. **Agree on selection and capacity.** Ask who authorizes a start and how to select the next eligible card. For solo work, suggest one active card as a starting limit. For a team, ask how many cards it can actively review and deliver at once. Count blocked cards and cards waiting inside the active workflow.
5. **Set the journal conventions.** Confirm the project time zone and who keeps the journal. Suggest the root `project/rememory/` folder for a single owner.

Present a compact proposal listing each stage, its folder name, the conditions to enter and leave it, allowed moves including rework, which stages count toward WIP, the overall limit, and the finish evidence. Ask the user to approve or amend it. Wait for approval before creating or moving stage folders or writing the workflow configuration.

## Apply the approved workflow

Use the [project directory template](../templates/project-layout.md) to check the resulting layout.

1. Preview the approved template with `python3 tools/kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris`. Substitute the agreed template, limit, and time zone. For a custom workflow, write the proposal to a separate JSON file and preview it with `python3 tools/kanban-board.py init --config approved-workflow.json`. Set `stages` to the ordered folder names, `active` to the stages counted toward WIP, `completed` to the completion stage, `wip_limit` to a positive integer, `timezone` to the agreed IANA time zone, and `transitions` to the approved mapping of source stages to lists of destinations.
2. Confirm the preview with the user and rerun the same command with `--apply`. The tool creates the stage folders, adds `.gitkeep` to empty folders, and writes `project/kanban/workflow.json`. If a different workflow exists or cards would fall outside the proposed stages, agree on a migration before moving any cards. Preserve filenames and IDs and update affected links.
3. Record the approved transition and evidence rules in the project's Kanban guide. Record ownership and Git permissions in the project's root `AGENTS.md`.
4. Run `python3 tools/kanban-board.py validate` and `python3 tools/kanban-board.py show`. Verify that each approved stage appears in order and that capacity matches the agreement. Record the approved workflow and verification in Rememory.
