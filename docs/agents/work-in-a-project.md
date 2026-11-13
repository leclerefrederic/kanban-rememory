# Working instructions

## First access

Check for `project/kanban/workflow.json` before resuming or creating cards. If it is missing, follow the [guided adoption interview](configure-a-project.md). Offer express setup with a short, standard, or long software template or custom setup with a guided interview. Present the resulting stage folders and policies and wait for approval before wiring the board. Resume normal work once the approved configuration and folders pass validation.

## Resume work

1. Read the [Kanban guide](../kanban/board-guide.md), review the cards in progress, then check the relevant backlog.
2. Identify the card and its owner. Read the latest relevant Rememory entry and specifications, and check the Git state.
3. Verify dependencies and resume at the next authorized action. Report discrepancies between the card, journal, and evidence.

## Execute work

- Search every column for a matching card before proposing one. Define the expected outcome, scope, owner, dependencies, and verifiable criteria.
- Add the card to the backlog after approval. Once execution is authorized, move it to the first active stage before changing deliverables. Approval of a card or specification does not by itself authorize implementation or publication.
- Update the [owner's journal](../../project/rememory/README.md) at each significant milestone. At closure, verify the criteria and record the evidence, revision, and next step. Distinguish testing, merging, publication, deployment, and user validation.
- Follow the repository's Git permissions. Keep changes local until publication is authorized. Report any required records that could not be written.

## Default conventions

Use the `TASK` prefix. For a single owner, keep the journal in the root `project/rememory/` directory. Use the project date and specify its time zone at adoption.

## Batch workflow roles

For a project using Batches, read the role that applies before editing project files. Specification Agent folder instructions should point to the Specification Agent role file.

- [User](roles/user.md)
- [Specification Agent](roles/specification-agent.md)
- [Development Agent](roles/development-agent.md)

When adopting the Batch module, read the shared procedure under “Record debt and resume acceptance” in `docs/batches/start-and-close-batches.md` before preparing or executing a Batch. Both agents use the same test and debt records when handing work back for correction.
