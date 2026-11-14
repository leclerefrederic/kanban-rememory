---
type: card
id: "CARD-00000134"
batch: "Batch-010"
specifications: ["SPEC-016"]
---

# CARD-00000134 — Orchestrate approved work from the same chat

- Owner: Development Agent
- Dependencies: approved SPEC-016 revision 1; native subagent support for live handoff.

## Expected outcome

Install a shared orchestration skill for approved Card and Batch handoffs in Codex and Claude Code.

## Acceptance criteria

- [x] Same-chat coordination covers proposals, exact approval, real delegation, recovery, evidence review, closure and authorized alerts.
- [x] Both host skill copies and supported launch paths are documented and verified as far as the environment permits.
- [x] Technical tests pass and the candidate exposes acceptance prerequisites and known limits.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Technical evidence: board validation, approval verification, skill sync, 32 board tests and 22 Telegram tests passed. Native Codex 0.169.0 and Claude Code 2.1.323 smoke sessions loaded the kit and dispatched one read-only child each on a disposable `spec016/smoke` branch. Both read the expected marker and returned its exact revision.
- Scope of evidence: native dispatch verified with a read-only fixture. Product acceptance cases still require the User's verdict.
- Flow and blockers: WIP reviewed at closure, with no other active Card. The Batch proceeds through candidate delivery and acceptance.

## History

- 2026-11-15T00:16:30+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T00:21:45+01:00 — Stage moved from `development` to `completion`.
