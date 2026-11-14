---
type: card
id: "TASK-00000105"
batch: null
specifications: []
---

# TASK-00000105 — Limit each agent to its own perimeter with least privilege

- Owner: Development Agent
- Dependencies:

## Expected outcome

Each agent reads and writes only what its role needs (least privilege), and the instructions say so in one place without ambiguity. A test of the Specification Agent skill on 2026-11-14 showed it opened a Card under `project/kanban/` although its role lists that folder as forbidden, because the role does not say whether the ban covers reading, `agents/work-in-a-project.md` tells every agent to review the Cards, the skill lists that file under "Read first", and the TASK-00000095 handoff entry links the Card. The same test showed the agent stating "No Batch active" without reading the Batch records, while Batch-007 is not closed. This Card fixes the instructions only; mechanical enforcement stays with TASK-00000096 and the Specification of TASK-00000095. Shared core: the rule is the same for ChatGPT/Codex and Claude. The manifesto and the lean agent rules are not changed here, because TASK-00000099 plans their single source.

## Acceptance criteria

- [x] The shared working instructions state the least-privilege rule: read and write only what the role needs, and stop and ask when work needs more.
- [x] Each role file lists Read access, Write access and Forbidden, and says whether Forbidden covers reading.
- [x] The Specification Agent neither reads nor writes `project/kanban/`, code or Git; the Development Agent reads Specifications only from the approved set and does not write `project/specs/`.
- [x] The Card steps in `agents/work-in-a-project.md` apply to the Development Agent only, and the Specification Agent skill no longer routes to them.
- [x] The Specification Agent reads the Batch records and states the Batch state before acting; it never states a state it has not read.
- [x] The TASK-00000095 handoff entry can be used without opening the Card.
- [x] The reader documentation matches, and the skill copies still match `agents/skills/`.
- [x] Board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T19:46:21+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T19:47:33+01:00 — Stage moved from `development` to `completion`.
