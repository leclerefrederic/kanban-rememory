---
type: card
id: "TASK-00000073"
batch: null
specifications: []
---

# TASK-00000073 — Require startup instructions for every acceptance test

- Owner: Development Agent
- Dependencies: None.

## Expected outcome

Make acceptance sessions self-contained at every case, preserve instructions when a verdict menu opens, and resume unfinished tests before requesting the delivery decision. The User authorized this correction through the documentation audit.

## Acceptance criteria

- [x] Begin every acceptance test and every individual case with explicit startup instructions, even when the setup repeats. State the exact build, how to launch it, any session to close or connection to establish, and any fixtures or data to prepare.
- [x] Present startup instructions first, then the actions and expected result, then the OK / KO menu. Keep the complete instructions visible alongside the test.
- [x] Apply the rule to the shared acceptance procedure and test template. Verify it on two consecutive cases with the same startup steps.
- [x] After recording each verdict and any required KO evidence, immediately present the next test or case with its startup instructions and OK / KO menu. Do not ask for a separate confirmation to continue. Repeat until every case has a verdict or a documented blocker, or until the User explicitly pauses the session.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Updated the guided acceptance procedure, tests template, and delivered-Batch resume guide. Pending scenarios are resumed before the final delivery decision.
- Walked through two consecutive export cases using the same fixture: both presentations repeat the exact build, launch, connection and fixture setup inside the verdict question. After the first OK, the second case follows immediately; a KO pauses only for explanation and screenshot evidence. This was a document walkthrough, not a live application acceptance session.
- Board validation, all 11 adoption tests, and `git diff --check` passed. Diff reviewed in Development; no executable behavior changed.
- No blockers remain. Publication target: origin/main.

## History

- 2026-11-14 — Resume this existing backlog Card first under the User's authorization to resolve the documentation audit. All Batches are closed.

- 2026-11-14T00:58:38+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T00:59:30+01:00 — Stage moved from `development` to `completion`.
