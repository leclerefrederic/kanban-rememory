---
type: card
id: "TASK-00000083"
batch: null
specifications: []
---

# TASK-00000083 — Apply the shared lean manifesto through explicit agent rules

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User request following the documentation separation.

## Expected outcome

Provide the agents with an operational version of the shared Lean Development Through Lean Specifications manifesto. Make each common principle actionable for Specification Agent and Development Agent without creating a different policy or moving agent procedures into human guides.

Scope: agent manifesto, entry-point and role links, adoption package and related installation verification. Preserve the approved shared manifesto and existing authorization, scope and acceptance rules.

## Acceptance criteria

- [x] Translate all six shared principles and the approval test into explicit agent actions with the common manifesto as the authority.
- [x] Require both agent roles to read and apply the operational version from the shared entry point.
- [x] Include the agent version in fresh adoption and maintain separate reader and agent navigation.
- [x] Verify links, installation tests and consistency with the unchanged common principles before closure.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `ff1370d`. Added the [agent manifesto](../../../docs/agents/lean-specifications.md), applying the six shared principles and approval test to existing Specification/Card, implementation, acceptance and debt records.
- Linked the operational version from shared working instructions, both AI roles, the agent index, installation procedure and directory template. The shared reader manifesto remains unchanged and authoritative; the agent version adds no independent scope, permissions or record format.
- Reviewed the document against all six common principles and existing role boundaries. Verified matching principle headings and byte-for-byte preservation of the shared manifesto. `python3 tools/test-kanban-board.py`: all 15 tests passed with the operational version in fresh installations. Board validation and whitespace checks passed.
- Flow review: no active Batch or other Card, no blocker. Unrelated local files remain untouched. Next action: publish the closed Card and verified changes under standing authorization.

## History

- 2026-11-14 — User clarified that the manifesto is binding on both people and agents and requested an agent version. TASK-00000082 is published; no other Card or Batch is active.

- 2026-11-14T01:36:39+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:38:02+01:00 — Stage moved from `development` to `completion`.
