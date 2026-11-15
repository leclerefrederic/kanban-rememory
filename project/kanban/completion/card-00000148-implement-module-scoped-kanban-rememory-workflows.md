---
type: card
id: "CARD-00000148"
batch: "Batch-012"
specifications: ["SPEC-021"]
---

# CARD-00000148 — Implement module-scoped Kanban Rememory workflows

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

Support independent Kanban Rememory modules in a shared repository with backward compatibility.

## Scope and authorization

The User approved SPEC-021 r1 and authorized development on 2026-11-15. Execute the Batch-012 mission on the dedicated worktree. Preserve the live repository layout.

## Acceptance criteria

- [x] Manifest, setup, module selection and role-scoped operations work for A/B and legacy repositories.
- [x] Shared ownership, local/global journal, isolated worktrees, and serialized integration and recovery satisfy the approved scenarios.
- [x] Remy distinguishes same-ID events in separate modules.
- [x] Review candidate diff and record technical checks for MM-01 through MM-15.

## Execution and evidence

- State: complete
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker: none

## History

- 2026-11-15: Batch approval verified and dedicated worktree ready. Begin manifest validation and module context. See [Rememory](../../rememory/2026-11-15.md).

- 2026-11-15T14:10:41+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15: committed manifest/setup/Remy and module tracking/roles/coordination milestones, latest revision `b8209f8d7c4de652df308451a8f830f931200728`. Next: integrate and verify qualified guard/publication and recovery, round out edge cases, run the integrated technical scenarios and hand off the exact candidate. Existing board, role and Telegram tests passed with isolated fixtures, including an additional simultaneous ownership/integration/journal check. No acceptance verdicts recorded.
- 2026-11-15: the dedicated candidate `1d70a04e39b39492bfac502045095cede7cc5317` passed technical verification and was published on `origin/codex/batch-012`. Next: Tester acceptance against the exact candidate, then the User's delivery decision. See [technical evidence](../../batches/batch-012/evidence/technical-verification.md).
- 2026-11-15: resumed on the same branch under the User-approved targeted MM-12 correction. Preserve the original candidate and case results. See [correction request](../../batches/batch-012/report.md#correction-request).
- 2026-11-15: MM-12 correction candidate `b93b732d69ceb72ef96209d9c806e6058140cfbe` verified on the dedicated branch. 55 affected automated checks passed. Next: KR Tester replay of MM-12 and affected integration scenarios. [Correction evidence](../../batches/batch-012/evidence/mm-12-correction-b93b732.md).
- 2026-11-15: reviewed the exact accepted candidate `b93b732d69ceb72ef96209d9c806e6058140cfbe` and verified required evidence in Development before completion. Five affected cases passed on this revision and the ten unaffected cases retain their original passing results. The User accepted the exact candidate. WIP is clear at closure.

- 2026-11-15T15:02:56+01:00 — Stage moved from `development` to `completion`.
