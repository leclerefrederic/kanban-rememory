---
type: card
id: "CARD-00000096"
batch: null
specifications: []
---

# CARD-00000096 — Enforce role limits with hooks for each LLM

- Owner: Development Agent
- Dependencies: CARD-00000095

## Expected outcome

Implement what the approved role-limits Specification (SPEC-012, Batch-008) requires, and nothing else: a role-limit check built from the role file headers in `agents/roles/*.md` and the optional Claude Code hook that calls it. Codex stays advisory in SPEC-012; a Codex branch needs a later Specification revision. The automatic check before `git push` already exists ([CARD-00000101](../completion/card-00000101-run-the-batch-checks-automatically-before-pushing-to-main.md)) and must not be duplicated. Shared core works for ChatGPT/Codex and Claude; any LLM-specific part is an optional branch that never changes a shared rule ([CARD-00000092](../completion/card-00000092-document-shared-core-and-llm-skill-branches.md)).

## Acceptance criteria

- [x] A write or a read forbidden for the active role is refused with an explicit message; an allowed write or read passes.
- [x] The behavior is tested without relying on the model's cooperation, for the shared check and the Claude hook, in `agents/tools/test-kanban-board.py`.
- [x] The kit works without either branch installed, and installing a branch is one documented command.
- [x] The hook files are part of the kit's package lists and `agents/templates/project-layout.md`.
- [x] `documentation/use-with-chatgpt-and-claude.md` no longer marks role hooks as planned and states what was delivered; the install procedure, the agent index and the roles are consistent with it.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14 — Refreshed under CARD-00000104 after CARD-00000092 to 103; see the Rememory entry of that day for what changed.
- 2026-11-14 — Rewritten from SPEC-012: Claude Code hook only, Codex advisory. Delivered on `claude/batch-008` (tested commit `843b4b3d0da50a0ce67f99024a1487b13eaffd57`) as CARD-00000115 and related Cards; close this Card after Batch-008 is accepted and merged.
- 2026-11-14 — Batch-008 was accepted and closed, tag `batch-008`. Delivered for Claude Code only; the Codex branch and the protection of the agent settings are tracked on [CARD-00000128](../backlog/card-00000128-protect-the-agent-settings-from-edits-and-cover-codex-with-role-limits.md). `agents/templates/project-layout.md` lists the `agents/tools/` directory, not each file.

- 2026-11-14T23:14:04+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T23:14:04+01:00 — Stage moved from `development` to `completion`.
