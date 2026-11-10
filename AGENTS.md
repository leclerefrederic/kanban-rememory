# Working instructions

## Resume work

1. Read the [Kanban guide](kanban/README.md), review the cards in progress, then check the relevant backlog.
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

This repository uses its own cards and journal to track changes to the kit. The journal uses Europe/Paris time, and work in progress is limited to one card across implementation, review, and ready to release. Select the oldest eligible backlog card by ID unless an agreed priority is documented on the card. Review blockers and flow at closure or before resuming interrupted work. Adapt this section for the target repository.
