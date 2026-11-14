---
type: card
id: "TASK-00000103"
batch: null
specifications: []
---

# TASK-00000103 — Install the kit skills in this repository

- Owner: Development Agent
- Dependencies:

## Expected outcome

The three kit skills are installed in this repository (the patient-zero project) for Claude Code and Codex by running the kit's own sync script, and a test keeps the copies identical to `agents/skills/`. Follows TASK-00000098.

## Acceptance criteria

- [x] `.claude/skills/` and `.agents/skills/` hold copies identical to `agents/skills/`, and no other file is changed by the sync.
- [x] A test fails when a copy in this repository differs from its source.
- [x] Claude Code lists the installed skills in a session started in this repository, or the gap is recorded. Gap recorded in the journal: not checked in a new session.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T11:49:16+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T11:49:51+01:00 — Stage moved from `development` to `completion`.
