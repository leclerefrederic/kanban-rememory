---
type: card
id: "TASK-00000076"
batch: null
specifications: []
---

# TASK-00000076 — Adopt lean development through lean specifications

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User request to integrate the approved manifesto before other backlog work.

## Expected outcome

Make the approved six-principle Lean Development Through Lean Specifications manifesto part of the reusable framework and the instructions followed by both agents.

Scope: one canonical English manifesto, links from the working instructions, roles, Batch workflow and project overview, and inclusion in the adoption package. Preserve the lean Specification template and existing approved Batch baselines.

## Acceptance criteria

- [x] Record the approved six principles and approval test, including the three agreed clarifications about ambiguity, corrections, and debt records.
- [x] Connect the manifesto to specification preparation, User approval, and development through the shared instructions and actor roles.
- [x] Include the manifesto in the installation instructions, directory template, and existing adoption test fixtures.
- [x] Review the diff and verify the board, documentation links, installation tests, and whitespace before closure.

## Execution and evidence

- State: Verified.
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Canonical reference: [Lean Development Through Lean Specifications](../../../documentation/lean-specifications.md).
- Reviewed the manifesto against the approved text and clarifications. Shared instructions, all three role files, the Batch workflow, installation guide, layout, and README link to the same reference. No new template fields or product behavior were added.
- `python3 tools/manage-kanban-board.py validate` — passed, including local Markdown links and anchors.
- `python3 tools/test-kanban-board.py` — all 11 tests passed, including adoption in isolated repositories with the manifesto installed.
- `git diff --check` — passed. Diff reviewed in Development before closure.
- Flow review: all Batches are closed, no blockers on this Card, and the older local backlog request remains separate. Publication target: origin/main under standing authorization.
- [Journal](../../rememory/2026-11-14.md).

## History

- 2026-11-14 — User approved the manifesto with three clarifications and authorized its integration into the framework. This standalone documentation task has priority over the older backlog card; all Batches are closed and Development is empty.

- 2026-11-14T00:42:49+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T00:44:26+01:00 — Stage moved from `development` to `completion`.
