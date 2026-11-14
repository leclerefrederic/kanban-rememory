---
type: report
id: "Batch-008-Report"
batch: "Batch-008"
---

# Batch report

## Handoff

- User approved the scope and authorized development on 2026-11-14: SPEC-011 revision 1 and SPEC-012 revision 1, in that priority order.
- Approved Specifications: [SPEC-011](../../specs/approved/spec-011-r1.md), [SPEC-012](../../specs/approved/spec-012-r1.md). Mission order: SPEC-011, then SPEC-012.
- Approval commit: `c8430e0ee0e596df29f7996e99a52614848b4b54` at `refs/heads/batch-approval/batch-008`.
- Base main commit: `51a013a5106e2c7dcabc845b4d11d2544e3d6939`.
- Working branch: `claude/batch-008`.
- Designated worktree: `/Users/fleclere/Documents/GitHub/kanban-rememory`.
- Guard record: not applicable. This Batch delivers no build artifact.

## Delivery summary and gaps

- Correction of Batch-008-DEBT-01 delivered on `claude/batch-008` as candidate `65b02a5f38559c201b6fc675bf2af402f67246aa`. The receipt key of `attention` and `completed` alerts now includes the task and the text of the request, so a different request that reuses a confirmed ID is notified; a resend stays a duplicate, and a Batch closure and completion of the same Batch remain one alert. Limit: rewording the text of a resend counts as a new request. No feature added. Debt stays open until the User verifies the correction. TEST-05, TEST-09, TEST-04 and TEST-08 are to replay on the new revision.

## Open debt and outstanding tests

No defect is open. Batch-008-DEBT-01 is resolved (below). All required scenarios have a verdict:

- TEST-01 to TEST-09 (SPEC-011) passed: the User gave OK on 2026-11-14 for `843b4b3` after testing with ChatGPT, with real Telegram sends. They were blocked earlier while the bot was not operational. The Development Agent's simulated run with a local stub, partly collected before it was interrupted, is supplementary technical evidence in tests.md.
- The User confirmed on 2026-11-14 that Telegram notifications work in full after a complete test in real conditions (a Development Agent session following a recipe, with real alerts at the choice and at completion). The tested revision of that live run was not stated by the User; the verdicts above stay recorded for `843b4b3`.
- Batch-008-DEBT-01, defect, blocking (classified by the User on 2026-11-14): the Telegram deduplication key uses chat, project, kind and an id chosen by the agent, not the task. In the stub run, a different request that reused an id already confirmed in the same project sent no alert (the agent said honestly in the chat that the User was not notified). Seen during the TEST-05 and TEST-09 technical evidence in tests.md; the User's ChatGPT tests did not report it. Resolved on the corrected candidate `65b02a5`: the User replayed TEST-04, TEST-05, TEST-08 and TEST-09 on 2026-11-14, all OK, including a different request reusing a confirmed ID in TEST-05.
- TEST-10 to TEST-17 (SPEC-012) passed: the User gave OK on 2026-11-14 for `843b4b3`, based on the Development Agent's automated technical evidence in tests.md. Codex was not run, which the Specification states as advisory.

## Correction request

- Tested revision: `843b4b3d0da50a0ce67f99024a1487b13eaffd57`. Blocking defect: Batch-008-DEBT-01. Related tests: TEST-05 and TEST-09 (SPEC-011), whose previous OK verdicts stay in `tests.md`.
- Expected behavior (SPEC-011, "Avoid duplicate alerts" and criterion 5): one confirmed alert per intervention request or completed task; a different request, task or event stays notifiable even if the agent reuses an identifier. Observed: the receipt key is built from chat, project, kind and an agent-chosen id, so a different request that reuses a confirmed id is skipped as a duplicate and no alert is sent. Evidence: the TEST-05 and TEST-09 entries of the technical evidence in [tests.md](tests.md).
- Authorization: on 2026-11-14 the User chose to correct first, within the approved scope of SPEC-011. The correction restores the agreed behavior and adds no feature. Development Agent delivers a new candidate; the User's earlier verdicts apply to `843b4b3` only, and TEST-05 and TEST-09 plus any case the change affects are guided again on the new revision.

## User decision

Accepted by the User on 2026-11-14 for the tested revision `65b02a5f38559c201b6fc675bf2af402f67246aa` recorded in [tests.md](tests.md). All 17 required scenarios passed on the revisions recorded there, and no debt remains open.

## Closure evidence

- Delivery tag: `batch-008` at `9fd71f78c20fb969cf1f37c65679c871111d3dc3`, the merge revision of `claude/batch-008`, which contains the accepted candidate `65b02a5f38559c201b6fc675bf2af402f67246aa`.
- Merge revision: `main` was merged into the Batch branch because the Telegram pages conflicted (`agents/configure-telegram.md`, `agents/install-in-a-project.md`). The tested code is unchanged from `65b02a5`. On 2026-11-14 the User accepted the combined pages in the chat ("Oui, clos") and asked for the closure; the acceptance recorded above is for `65b02a5`.
- Checks on the merged `main` before closing: 33 adoption tests, 22 Telegram setup tests, board validation, skill copy check and `verify-approval Batch-008` pass.
- Closing trailer: `Batch-Closure: Batch-008`. Batch-008-DEBT-01 resolved on `65b02a5`.
