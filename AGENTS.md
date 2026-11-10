# Working instructions

## First access

Check for `kanban/workflow.json` before resuming or creating cards. If it is missing, follow the [guided adoption interview](agents/adoption.md). Offer express setup with a short, standard, or long software template or custom setup with a guided interview. Present the resulting stage folders and policies and wait for approval before wiring the board. Resume normal work once the approved configuration and folders pass validation.

## Resume work

1. Read the [Kanban guide](docs/kanban.md), review the cards in progress, then check the relevant backlog.
2. Identify the card and its owner. Read the latest relevant Rememory entry and specifications, and check the Git state.
3. Verify dependencies and resume at the next authorized action. Report discrepancies between the card, journal, and evidence.

## Execute work

- Search every column for a matching card before proposing one. Define the expected outcome, scope, owner, dependencies, and verifiable criteria.
- Add the card to the backlog after approval. Once execution is authorized, move it to the first active stage before changing deliverables. Approval of a card or specification does not by itself authorize implementation or publication.
- Update the [owner's journal](Rememory/README.md) at each significant milestone. At closure, verify the criteria and record the evidence, revision, and next step. Distinguish testing, merging, publication, deployment, and user validation.
- Follow the repository's Git permissions. Keep changes local until publication is authorized. Report any required records that could not be written.

## Default conventions

Use the `TASK` prefix. For a single owner, keep the journal in the root `Rememory/` directory. Use the project date and specify its time zone at adoption.

## Rules for the Kanban Rememory repository

This repository uses its own cards and journal to track changes to the kit. The journal uses Europe/Paris time, and work in progress is limited to one card across Development, Code Review, and Deployment. Select the oldest eligible backlog card by ID unless an agreed priority is documented on the card. Review blockers and flow at closure or before resuming interrupted work. Adapt this section for the target repository.

Publish each verified change to `origin/main` after closing its card. The repository owner has granted standing authorization for these pushes.
