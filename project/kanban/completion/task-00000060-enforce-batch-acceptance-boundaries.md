---
type: card
id: "TASK-00000060"
batch: null
specifications: []
---
# TASK-00000060 — Enforce Batch scope and protect acceptance builds

- Owner: Development Agent
- Dependencies: Batch-003 must be delivered before this card enters Development.

## Expected outcome

Prevent unrelated work, changes to the artifact under acceptance, and premature publication during a Batch. See the [Batch-003 incident](../../batches/batch-003/report.md#acceptance-process-incident).

## Acceptance criteria

- [x] Require an authorized active Card before changing code, build scripts, or delivery artifacts. When a request falls outside the approved Batch scope, record it in a dedicated Backlog card and defer execution until after the active Batch is delivered.
- [x] Record the exact commit and artifact under acceptance. Protect that artifact from replacement, renaming, or cleanup during UAT. Verify that a replacement requires an explicit restart of the affected tests with the new revision recorded.
- [x] Add an enforceable publication check. Require applicable technical verification, including a full build for build-script changes. Require the recorded User decision for closure and publication to main. A syntax check alone must not qualify a changed build script.
- [x] Reproduce the incident in an isolated repository. Confirm that an out-of-scope cleanup, an attempt to change the artifact under test, and publication after syntax-only verification are blocked. Confirm that authorized and verified work can proceed.

## History

- 2026-11-13 — User requested a dedicated follow-up after the Batch-003 acceptance incident. Added to Backlog.

- 2026-11-13T21:02:19+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-13 — Isolated Git fixture verified scope, freeze, restart requirement, full-build requirement, acceptance, and artifact integrity checks. Guard is invoked by the documented workflow.

- 2026-11-13T21:03:23+01:00 — Stage moved from `development` to `code-review`.

- 2026-11-13T21:03:23+01:00 — Stage moved from `code-review` to `completion`.
