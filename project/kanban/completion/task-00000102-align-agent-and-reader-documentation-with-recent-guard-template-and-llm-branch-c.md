---
type: card
id: "TASK-00000102"
batch: null
specifications: []
---

# TASK-00000102 — Align agent and reader documentation with recent guard, template and LLM-branch changes

- Owner: Development Agent
- Dependencies:

## Expected outcome

Agent and reader documentation describe the same behavior after TASK-00000092, 93, 94, 100 and 101, with no contradictory or missing statement. No rule changes meaning; the Specification Agent's pending role Specification is out of scope.

## Acceptance criteria

- [x] Every agent document that mentions the guard, publication, the daily template or the build-check files (`resume-a-batch.md`, `delivery-example.md`, `runner/build-and-run.md`, `batch-report.md` template and the documentation example) is reviewed and consistent with the current guard, `full_build_files`, the optional push check and the template location.
- [x] The reader guide for delivering a Batch tells the User, in user terms, that publication of a closed Batch can be refused automatically and what that means; no command or format is added to reader guides.
- [x] `documentation/use-with-chatgpt-and-claude.md` reflects the verified findings: Claude has a Cowork/Code boundary, ChatGPT and Codex share one project space, and the kit protects transitions rather than sessions; unverified points stay marked.
- [x] A final search finds no stale reference to `project/rememory/daily-template.md` or to the former hard-coded `build-app.sh` rule outside historical records.
- [x] Adoption tests and board validation pass.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T11:25:41+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T11:26:41+01:00 — Stage moved from `development` to `completion`.
