---
type: card
id: "TASK-00000080"
batch: null
specifications: []
---

# TASK-00000080 — Explain the agent-run workflow and Card ownership

- Owner: Development Agent
- Dependencies: None.
- Priority: User clarification of the README's audience and operating model.

## Expected outcome

Explain Kanban Rememory as an agent-run workspace: the User provides requests and decisions; AI agents organize, execute, verify, and record authorized work. Only Development Agent writes and maintains Cards. Explain the guiding principles, connected components, inputs, internal workflow, outputs, and approval boundaries, including how the framework supports the User throughout a project.

Scope: README and the documentation defining Card responsibilities. Preserve current capabilities, the optional Batch module, explicit authorization and acceptance, and the distinction between agent procedures and the future automated dispatcher.

## Acceptance criteria

- [x] Explain the guiding principles, connected components, and delivery loop: what enters the system, how agents handle it, what the User receives, and where User decisions are required.
- [x] Make AI-only Card creation and maintenance explicit in the README, shared instructions, roles, and Card guides; keep the User responsible for requests and decisions.
- [x] Describe current execution and Runner capabilities accurately without implying an implemented autonomous scheduler.
- [x] Review consistency, local links, and the diff; preserve approved historical records and unrelated local files.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `e73b24a`. The [README](../../../README.md) now explains the agent-run operating model, guiding principles, component relationships, delivery and correction loop, and support for the User from request to closure. Includes a Mermaid flow diagram and preserves the current scheduler/Runner limitations.
- Aligned the shared instructions, User and Development Agent roles, Card and board guides, and setup introduction: only Development Agent creates and maintains Cards. External-edit checks remain; Specification Agent's assigned responsibilities remain unchanged.
- `python3 tools/manage-kanban-board.py validate` and `git diff --check` passed. Reviewed the documentation diff against the existing roles, manifesto, and Batch procedure. This is a documentation-only revision; no executable behavior changed and no application test is claimed.
- Flow review: no other active Card or open Batch, no dependencies or blocker. Approved historical records and unrelated local files were preserved. Next action: publish the closed Card and documentation under standing authorization.

## History

- 2026-11-14 — User clarified that only AI writes Cards, then requested an explanation of the framework as an autonomous box. The clarification is incorporated into this same Card. All Batches are closed and no other Card is active.
- 2026-11-14 — User further requested guiding principles, how the pieces connect, and how the system runs and supports project building. Incorporated into the same README revision.

- 2026-11-14T01:21:29+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:24:21+01:00 — Stage moved from `development` to `completion`.
