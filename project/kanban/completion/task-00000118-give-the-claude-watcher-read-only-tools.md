---
type: card
id: "TASK-00000118"
batch: null
specifications: []
---

# TASK-00000118 — Give the Claude watcher read-only tools

- Owner: Development Agent
- Dependencies:

## Expected outcome

The Claude watcher of KRR can read the Kanban files it is asked to summarize. A second ChatGPT review of 2026-11-14 reported, and reading `apps/krr/src/macos/managed-watchers.swift` and the CLI help confirmed, that the watcher started `claude -p --permission-mode plan --tools ""`, and `--tools ""` disables every tool, so it could not read the board. The invocation now allows only `Read`, `Glob` and `Grep`: no shell and no writing, which keeps the watcher read-only. The Codex branch already reads through its read-only sandbox. A source check guards the argument list. Shared core: the watcher request is the same for ChatGPT/Codex and Claude; only the engine arguments differ.

## Acceptance criteria

- [x] The Claude invocation passes `--tools Read,Glob,Grep` and no longer disables every tool.
- [x] A test fails if the Claude invocation disables all tools again or allows a tool that can write.
- [x] The app compiles with `-warnings-as-errors` through its build script, written to a scratch folder.
- [x] The new argument list was run once with the Claude CLI on this repository and the result is recorded in the journal.
- [x] Board validation and adoption tests pass; skill copies match the kit.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T20:51:50+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T20:53:19+01:00 — Stage moved from `development` to `completion`.
