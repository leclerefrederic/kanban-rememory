---
type: report
id: "Batch-012-Report"
batch: "Batch-012"
---

# Batch report

## Handoff

- On 2026-11-15, in the original Codex chat, the User said “J'ai changé pour Sol elevé. Ok, je valide SPEC-021 r1. Lance le développement.” This approves the exact revision and authorizes development.
- Approved scope: [SPEC-021 revision 1](../../specs/approved/spec-021-r1.md). The spec is preserved byte for byte; its draft-era approval note is superseded by this decision.
- Working branch: `codex/batch-012`.
- Owner: KR Developer (Batch-012 Developer handoff in this Codex chat).
- Approval commit: `2e3578fd3fb8f9ce933b821cf31976166c187415` at `refs/heads/batch-approval/batch-012`.
- Base main commit: `d1c711b96637fc0845c41568c158a8ba78df7f87`.
- Designated worktree: `/private/tmp/kr-batch012-development`.
- Earlier development checkpoint: `b8209f8d7c4de652df308451a8f830f931200728`. This is an implementation milestone. Resume verification and remaining scope from the designated worktree and the dated Rememory entry.

- Candidate verified on `origin/codex/batch-012`: `1d70a04e39b39492bfac502045095cede7cc5317`. Technical evidence and startup commands are in [tests.md](tests.md).

- Correction candidate verified on `origin/codex/batch-012`: `b93b732d69ceb72ef96209d9c806e6058140cfbe`. [MM-12 and related integration verification](evidence/mm-12-correction-b93b732.md) passed technically and in [independent Tester replay](evidence/acceptance-b93b732.md). The original KO is preserved against its revision.

## Delivery summary and gaps

- Acceptance on `1d70a04e39b39492bfac502045095cede7cc5317` completed: 14 of 15 cases passed (MM-01 User verdict, 13 KR Tester verdicts), and MM-12 failed with blocking debt. See [scenario verdicts](tests.md) and [acceptance evidence](evidence/acceptance-1d70a04.md). The 92 automated tests passed but did not cover a successful combined check followed by publication with a stale acceptance decision.
- On `b93b732d69ceb72ef96209d9c806e6058140cfbe`, KR Tester confirmed MM-12 and replayed MM-07, MM-08, MM-11 and MM-13 successfully. All 55 affected checks passed.

## Open debt and outstanding tests

- **Batch-012-DEBT-01 (S1, blocks acceptance), MM-12.** Candidate `1d70a04e39b39492bfac502045095cede7cc5317` allowed preparation and publication of a combined integration containing a new shared source file, despite a recorded acceptance only for the earlier candidate. Technical checks and the pre-push hook passed on the fixture. See the [reproduction and observed refs](evidence/mm-12-stale-acceptance.md). The published reference in this reproduction belongs to a disposable local remote.
- Correction verified on `b93b732d69ceb72ef96209d9c806e6058140cfbe`; see the [Tester replay](evidence/acceptance-b93b732.md). No blocking failure remains in the affected cases.

## Correction request

- On 2026-11-15, the User approved the targeted MM-12 correction and authorized execution and replay of affected integration tests. Batch-012-DEBT-01 applies to delivered candidate `1d70a04e39b39492bfac502045095cede7cc5317`; see [MM-12 reproduction](evidence/mm-12-stale-acceptance.md).
- Enforce the existing SPEC-021 r1 requirement for affected acceptance checks and a decision on the updated candidate before publishing changed product content. Preserve prior evidence, release shared integration ownership during the wait, and recheck current main on resumption. Replay MM-12 and affected integration and recovery cases, including the unchanged-candidate path and records-only closure.
## User decision

- On 2026-11-15 the User accepted `b93b732d69ceb72ef96209d9c806e6058140cfbe` and explicitly requested Batch-012 closure, publication to `origin/main`, and the completion Telegram to Remy. No outstanding debt was deferred.

## Closure evidence

- Authorized accepted/tested candidate: `b93b732d69ceb72ef96209d9c806e6058140cfbe`. The five affected independent scenarios passed on this revision; the ten unaffected verdicts remain tied to their earlier evidence. No blocking debt remains.
- Closing paths: approved SPEC-021 r1, the description/test/report and evidence of this Batch, the completed Kanban record and the dated Rememory journal. The candidate already contains the product and automated tests.
- Working ref: `refs/heads/codex/batch-012` at the candidate. Recovery ref: `refs/heads/batch-recovery/batch-012` at the commit bearing trailer `Batch-Closure: Batch-012`. Retire both only after verifying their tips and published main.
- Retained archive: `refs/tags/batch-012` at the exact candidate. Retain the local `refs/heads/batch-approval/batch-012` at the approved snapshot.
- The project's pre-push hook is enabled. No artifact guard is configured for this Batch. The manifest and module activation are excluded from the live repository.
