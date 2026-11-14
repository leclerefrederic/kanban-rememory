---
type: card
id: "CARD-00000122"
batch: "Batch-008"
specifications: ["SPEC-012"]
---

# CARD-00000122 — Install the role-limit hook and the two Claude Code agents

- Owner: Development Agent
- Dependencies:

## Expected outcome

A project can enable the optional role-limit check for Claude Code with one command, and disable it with another. The kit ships two Claude Code agent definitions, `specification-agent` and `development-agent`, that only route to the role files, so the User starts a session as a role with `claude --agent <name>`. `agents/tools/install-claude-role-hook.py` copies them to `.claude/agents/` and adds the hook to `.claude/settings.json` without touching other settings or hooks; it previews unless `--apply` is given, is idempotent, and `--remove` takes back only what it added. The check was run in a scratch repository with the real Claude Code CLI to settle whether the session identity reaches the hook. Shared core: nothing changes for projects that do not install it.

## Acceptance criteria

- [x] The installer previews by default, installs the two agents and the hook with `--apply`, can run twice with no change, keeps other settings and hooks, and `--remove` deletes only its own entries.
- [x] A real Claude Code run as the Specification Agent in a scratch repository is refused on a `project/kanban/` read, and a run as the Development Agent can read it; both results are recorded.
- [x] Tests cover the installer; board validation and adoption tests pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T21:19:03+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T21:22:00+01:00 — Stage moved from `development` to `completion`.
