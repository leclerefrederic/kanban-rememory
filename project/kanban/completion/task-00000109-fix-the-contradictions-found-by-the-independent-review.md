---
type: card
id: "TASK-00000109"
batch: null
specifications: []
---

# TASK-00000109 — Fix the contradictions found by the independent review

- Owner: Development Agent
- Dependencies:

## Expected outcome

The contradictions found by an independent read-only review on 2026-11-14 are fixed where the file is not closed, so the instructions, the skills and the reader documentation agree with the role perimeters of TASK-00000105, 107 and 108. The review reported 18 findings; the ones fixed here were read in the files first. A closed Batch report keeps its stale sentences and the journal records them.

## Acceptance criteria

- [x] The Specification Agent skill no longer routes to a journal procedure or to Git checks its role cannot perform; the resume procedure marks its Git checks for the Development Agent.
- [x] The Batch procedures name the Development Agent for `validate` and `verify-approval`, and the Specification Agent for resource moves and restores.
- [x] Both roles list `AGENTS.md` in their read access, the Development Agent also `agents/`; the "ready files" wording no longer reads as `project/specs/ready/`.
- [x] The standalone skill reads the Development Agent role.
- [x] The reader documentation names the agent per step and says roles are separate sessions.
- [x] TASK-00000096 tests reads as well as writes; TASK-00000099 facts are corrected.
- [x] The stale sentences of the closed Batch-007 report are recorded in the journal, not edited.
- [x] Board validation and adoption tests pass; the installed skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:20:37+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:20:38+01:00 — Stage moved from `development` to `completion`.
