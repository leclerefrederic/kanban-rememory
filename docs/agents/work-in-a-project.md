# Working instructions

Read the shared [Lean Development Through Lean Specifications manifesto](../guides/lean-specifications.md) and apply its [agent rules](lean-specifications.md) when defining, reviewing, implementing or resuming work. Both agent roles must follow the same principles as the User. Use the approval test before proposing scope and keep suggestions separate from approved requirements.

## First access

Check for `project/kanban/workflow.json` before resuming or creating cards. If it is missing, follow the [guided adoption interview](configure-a-project.md). Offer express setup with a short, standard, or long software template or custom setup with a guided interview. Present the resulting stage folders and policies and wait for approval before wiring the board. Resume normal work once the approved configuration and folders pass validation.

## Resume work

1. Read the [Kanban guide](kanban/board-guide.md), review the cards in progress, then check the relevant backlog.
2. Identify the card and its owner. Read the latest relevant Rememory entry and specifications, and check the Git state.
3. Verify dependencies and resume at the next authorized action. Report discrepancies between the card, journal, and evidence.

## Execute work

Only the AI Development Agent creates, writes, moves, and closes Cards, including for standalone work. The User supplies requests, priorities, approvals, and verdicts through conversation; the agent records them. Never ask the User to write or maintain a Card.

- Search every column for a matching card before proposing one. Define the expected outcome, scope, owner, dependencies, and verifiable criteria.
- Add the card to the backlog after approval. Once execution is authorized, move it to the first active stage before changing deliverables. Approval of a card or specification does not by itself authorize implementation or publication.
- Update the owner's journal at each significant milestone following the [Rememory instructions](maintain-rememory.md). At closure, verify the criteria and record the evidence, revision, and next step. Distinguish testing, merging, publication, deployment, and user validation.
- Follow the repository's Git permissions. Keep changes local until publication is authorized. Report any required records that could not be written.

## Default conventions

Use the `TASK` prefix. For a single owner, keep the journal in the root `project/rememory/` directory. Use the project date and specify its time zone at adoption.

## Batch workflow roles

Cards and Rememory support standalone work. Its approved outcome, scope, and checks live on the Card; a Specification and Batch are optional. Follow the project's Git permissions for standalone delivery. Batch approval, branch, and closure rules apply only to Batch work.

For a project using Batches, read the role that applies before editing project files. Configure each agent's project instructions to read this file and its role; use the role links below. The same agent may perform the roles at different times while preserving their responsibilities. Specification Agent records scope and acceptance; Development Agent owns implementation, Cards, and Git. New standalone work waits until an active Batch is delivered and must preserve its acceptance candidate.

- [User](roles/user.md)
- [Specification Agent](roles/specification-agent.md)
- [Development Agent](roles/development-agent.md)

When adopting the Batch module, read the shared procedure under “Record debt and resume acceptance” in `docs/agents/batches/start-and-close-batches.md` before preparing or executing a Batch. Both agents use the same test and debt records when handing work back for correction.
