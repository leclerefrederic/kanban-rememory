---
type: card
id: "CARD-00000139"
batch: null
specifications: []
---

# CARD-00000139 — Retire the redundant standalone skill

- Owner: KR Developer
- Approval and priority: the User explicitly authorized removing the standalone skill and executing this follow-up on 2026-11-15. Targeted priority ahead of other backlog entries.
- Dependency: CARD-00000138, the short names for the four role skills.

## Expected outcome

Users handle adoption and work outside a Batch through KR Orchestrator and KR Developer. The kit no longer installs a separate standalone skill. Sync retires unchanged shipped copies on upgrade and leaves customized copies for manual review.

## Acceptance criteria

- [x] The separate skill is absent from canonical, Codex and Claude Code directories and active skill lists.
- [x] The remaining routes cover adopting the kit, creating and closing a standalone Card, and finding the software workflow profile.
- [x] Sync detects and retires unchanged legacy copies for both hosts and preserves a customized copy. Board, skills and applicable tests pass.

## Execution and evidence

- State: Verified.
- Actual finish: 2026-11-15.
- Verified a fresh core-only adoption, including preview and initialization, and a standalone Card through Completion without a Batch.
- Verified migration using the exact pre-removal shipped standalone copy in both hosts. A stale canonical source was skipped, and a customized installed copy was preserved. Board validation, skill synchronization, diff checks, 34 board tests and 22 Telegram tests passed.
- Reviewed flow and diff before closure. No blockers remain.

## History

- Earlier proposed renaming was superseded by the User's approved removal before implementation started.

- 2026-11-15T01:48:32+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T01:51:12+01:00 — Stage moved from `development` to `completion`.
