---
type: card
id: "TASK-00000092"
batch: null
specifications: []
---

# TASK-00000092 — Document the shared core and LLM-specific skill branches

- Owner: Development Agent
- Dependencies:

## Expected outcome

Explain in `documentation/` how the kit keeps one shared core usable by ChatGPT/Codex and Claude, with optional skill branches per LLM that exploit each one's capabilities without breaking consistency.

## Acceptance criteria

- [x] A documentation page states what belongs to the shared core and what belongs to each LLM branch, and is linked from `documentation/index.md`.
- [x] The page records the verified discovery paths (`.claude/skills/`, `.agents/skills/`), the common `SKILL.md` format, and the hook differences relevant to role enforcement, with official sources.
- [x] The page states the rule that a branch may add capabilities but never change the meaning of a shared rule.
- [x] `python3 agents/tools/test-kanban-board.py` and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T10:30:38+01:00 — Created directly in `development` at the User's explicit request. The file reuses the obsolete duplicate of TASK-00000091 (closed in `completion`), renamed and re-identified.

- 2026-11-14T10:33:56+01:00 — Stage moved from `development` to `completion`.
