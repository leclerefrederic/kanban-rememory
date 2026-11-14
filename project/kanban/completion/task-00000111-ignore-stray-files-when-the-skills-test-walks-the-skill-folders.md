---
type: card
id: "TASK-00000111"
batch: null
specifications: []
---

# TASK-00000111 — Ignore stray files when the skills test walks the skill folders

- Owner: Development Agent
- Dependencies:

## Expected outcome

`test_sync_skills_copies_checks_and_keeps_other_skills` passes when Finder leaves a `.DS_Store` file in `agents/skills/`. It failed on 2026-11-14 because the test walked every entry of that folder, while `agents/tools/sync-skills.py` already keeps only folders holding a `SKILL.md`. The test now follows the same rule. The tool is unchanged.

## Acceptance criteria

- [x] The test walks only folders that hold a `SKILL.md`.
- [x] The 20 adoption tests pass with the stray `.DS_Store` still present.
- [x] Board validation passes.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:24:32+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:25:00+01:00 — Stage moved from `development` to `completion`.
