# TASK-00000001 — Add Kanban practices to the reusable kit

- Owner: requester
- Dependencies: none
- Approval to add and execute: requester, 2026-11-10

## Expected outcome

Enable a project to configure its workflow and track a card from selection to closure.

## Acceptance criteria

- [x] The guide explains how to configure the workflow and its transition policies.
- [x] The guide covers selection based on capacity and how to handle blockers.
- [x] The guide and templates support the four flow measures and workflow reviews.
- [x] Project-specific rules are separate from common practices.

## Execution and evidence

- Actual start and finish: 2026-11-10, Europe/Paris.
- Git base verified: `285e5c2`. Deliverables are in the local changes.
- Workflow checked: a started card fills the only WIP slot, still counts while blocked, and frees the slot at closure. A card started on the 10th and finished on the 14th is two days old on the 12th, has a four-day cycle time, and adds one to throughput when closed.
- Local checks: column structure, unique card ID, template fields, and `git diff --check`.
- [Milestone log](../../rememory/2026-11-10.md).
