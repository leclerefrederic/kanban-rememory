---
type: tests
id: "Batch-012-Tests"
batch: "Batch-012"
---

# Acceptance tests

- Tested commit: `b93b732d69ceb72ef96209d9c806e6058140cfbe`, the correction candidate on verified `origin/codex/batch-012`. The observed acceptance results below remain tied to the earlier `1d70a04e39b39492bfac502045095cede7cc5317`.
- Environment or prerequisites: Start from the exact candidate in the dedicated worktree. See the linked reproduction commands. Use isolated A/B fixtures and a local-only test remote. Replay the affected integration/closure cases using the correction evidence.
- Technical evidence: [MM-12 correction and 55 passing affected checks](evidence/mm-12-correction-b93b732.md). The [original 92 checks, native scope notes and scenario coverage](evidence/technical-verification.md) remain available.

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| MM-01 | SPEC-021 r1 | Operate an existing project without a manifest; separately configure two modules through approved setup. | Legacy behavior is preserved; setup shows the intended layout, creates separate tracking spaces and retains common sources. | OK | `1d70a04e39b39492bfac502045095cede7cc5317` | KR Tester observed expected behavior in a disposable fixture. User replied “MM-01 OK, passe à MM-02 et guide-moi.” See MM-01 below. |
| MM-02 | SPEC-021 r1 | Supply invalid JSON, duplicate IDs/keys, unknown schema, unsupported policy values, overlapping/escaping paths and symlink aliases. | Explicit actionable failure before affected writes; no fallback to another project/module. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Tester replay: all 26 invalid setup and board attempts were refused without writes or legacy fallback. See MM-02 below. |
| MM-03 | SPEC-021 r1 | Give A and B identical Card/Spec/Batch IDs; select each, then submit an ambiguous command. | Qualified references resolve correctly, including Spec revisions; the ambiguous write/pickup waits for clarification. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Board fixture resolved the same Card, Spec and Batch IDs per module, pinned distinct Spec revisions, refused ambiguous creation and excluded cross-module moves. |
| MM-04 | SPEC-021 r1 | Invoke all four roles on A in Codex and Claude; exercise forbidden role operations and an authorized shared-source change. | Existing role limits hold at new paths; B's records remain outside A's assignment. Host enforcement/advisory evidence is distinguished. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | All eight native invocations passed on the delivered hook and parser. Claude named-role denials and authorized shared write observed. Codex scope is advisory. |
| MM-05 | SPEC-021 r1 | Publish independent A and B deliveries, retry one journal write, then start a fresh session scoped to A. | Both local histories and concise linked global milestones survive once; startup loads relevant common/A context and follows needed dependencies. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Both synthetic deliveries published to local origin. Local and global journal links remained valid, replay was idempotent, and fresh module context was verified separately. |
| MM-06 | SPEC-021 r1 | Race two agents for A while another starts B; update tracking with conflicting branch-local state. | One owner per module; tracking is visible without unfinished product integration or lost writes. Stale copies cannot bypass ownership. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Three concurrent claims produced one A owner and one B owner. A stale branch's tracking update appeared in the primary checkout with no product merge. |
| MM-07 | SPEC-021 r1 | Block A, deliver it for acceptance, then wait for integration; attempt another A delivery at each stage. | A's slot remains occupied until verified closure; independent B work can continue. Rejection also retains A's slot until closure. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | A retained its claim during wait, delivery, validation and rejection while B remained active. Release required verified closure and retained remote evidence. |
| MM-08 | SPEC-021 r1 | Prepare a Batch during an A Card, then execute that Batch after closure alongside a B Card; delegate tasks and try a second A pickup. | Draft/ready reserves no slot. Active deliveries each have a branch/worktree; helpers obey owner/Card WIP; a second A delivery cannot start. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | A ready Batch coexisted with the A Card and could only start after Card closure while B continued. A helper lacked active-move ownership. Module WIP refused a second Batch Card. |
| MM-09 | SPEC-021 r1 | Interrupt an owner and resume in a fresh session; attempt a takeover while the original still runs. Try unsupported multi-clone execution. | Resume preserves identity/checkpoint; no live-owner takeover or unsupported concurrency guarantee. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Wrong-owner takeover refused while the owner's check was running. Same owner and checkpoint resumed in a fresh process. A separate clone's pickup was refused. |
| MM-10 | SPEC-021 r1 | Run checks concurrently using the same default resource names. | Required runtime isolation prevents one module's checks from altering the other's artifacts or results. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Concurrent runtime checks isolated same-named SQLite databases and artifacts. Developer's exact-candidate loopback evidence also passed. |
| MM-11 | SPEC-021 r1 | Request two integrations together and advance main before the second publishes. | One integration at a time; the second verifies against current main and preserves intervening changes. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | A second integration was refused while the first held ownership. Advanced main invalidated verification and the next owner began against the new base. Local publications preserved both modules. |
| MM-12 | SPEC-021 r1 | Make passing branches incompatible via a shared format; alter an accepted candidate at integration, then await a decision. | Incompatible publication stops; affected acceptance/decision refer to the new candidate. Global integration ownership is released, B can publish, and A rechecks main on resumption. | KO (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | The incompatible combined build was blocked. A compatible changed revision nevertheless published with only the old candidate's decision. See [MM-12 evidence](evidence/mm-12-stale-acceptance.md). |
| MM-13 | SPEC-021 r1 | Interrupt accepted publication and rejected archival, then resume each. | Existing recovery completes once for the qualified delivery; rejected product changes stay outside main, evidence survives and slots release only at closure. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Local recovery replay passed after both accepted and rejected interruptions, with the pre-push hook active. Retained refs were exact, rejected code stayed outside main and the slots released after verified closure. |
| MM-14 | SPEC-021 r1 | Produce equivalent Remy events for A and B with identical local IDs; replay one event. | Two distinct module-qualified alerts, one per event; confirmed replay is deduplicated and existing language/next-action rules hold. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | A/B alerts with identical local IDs generated two distinct French messages with module and next action. Replay was suppressed with a simulated transport. |
| MM-15 | SPEC-021 r1 | Propose activation with frozen records and active work; decline, then approve it. | Decline changes nothing. Activation waits for existing work to close; approved setup preserves frozen bytes/paths and IDs, and starts with reconciled ownership. | OK (Tester) | `1d70a04e39b39492bfac502045095cede7cc5317` | Preview made no changes, an active legacy Card blocked activation, and explicit activation after closure preserved frozen Card, Spec and Batch paths and bytes. |

## Startup and actions by case

Use isolated repositories with modules A and B, shared sources, and a local test remote. Use a separate legacy fixture without a manifest. For MM-04 use fresh role invocations in Codex and Claude Code. For MM-06 through MM-13 record participating worktrees, candidates and the points where simultaneous actions or interruptions occur. For MM-14 use a test destination or a fixture transport. Record exact launch steps, revision, observations and evidence before assigning verdicts.

### MM-01 — Legacy board and opt-in activation

- KR Tester used the exact candidate in the Developer's designated worktree and the disposable setup from `agents/tools/test-module-delivery.py`. The fixture ran with a local-only remote and was removed after the observations.
- Before activation, `manage-kanban-board.py new "Legacy fixture task" --owner Fixture --apply` created the legacy fixture's backlog Card under `project/kanban/backlog/` without a manifest or module selector.
- `configure-project-modules.py proposal.json --workflow workflow.json` listed modules A/B, their stages and the global and local memory paths. It printed `Preview only. Run again with --apply after approval.` and created neither `project.json` nor any module directory.
- Explicit `--apply` printed `Project modules are ready.` Each module received its own `kanban/workflow.json` and `rememory/`. The shared source and the legacy Card kept the same paths and exact bytes. The fixture also contained global `project/rememory/`.
- User verdict: OK for this candidate. The User authorized proceeding to MM-02.

### MM-02 — Invalid manifests and refusal before writes

- KR Tester used the disposable setup from `agents/tools/test-module-delivery.py` on the Developer's exact candidate. The fixture had a working legacy board with a backlog Card and a local-only remote.
- For each variant, run `configure-project-modules.py proposal.json --workflow workflow.json --apply` with no active manifest. Then place the same invalid bytes at `project.json` and attempt `manage-kanban-board.py new "Must be refused" --owner Fixture --apply`. Stop on the exit result and compare the checkout before and after each command.
- Thirteen variants covered malformed JSON, repeated schema key and module ID, schema version 2, unsupported values for all four execution policies, parent path escape, nested workspaces, overlap with global memory, a symlink alias of another workspace and a symlink pointing outside the repository. Both commands exited 1 for each variant with a message naming the invalid syntax, key, value or path.
- File hashes, directory paths and symlink targets were unchanged after all 26 refusals, excluding fixture Git metadata. Failed setup created no manifest. Failed board writes created no Card on the existing legacy board or in a module. Removing the invalid manifest let the legacy control create a Card again. The fixture was removed.
- Tester verdict: OK. The User delegated independent scenario verdicts to the Tester.

### MM-03–MM-15 — Independent Tester verdicts

The User delegated the independent case verdicts. The [Tester replay and additional observations](evidence/acceptance-1d70a04.md) supplement the Developer's technical evidence. MM-12 is KO and remains tied to the delivered revision. The Batch has no overall acceptance decision.

### Correction replay — b93b732

Exact tested revision: `b93b732d69ceb72ef96209d9c806e6058140cfbe`. All results below are KR Tester verdicts in disposable fixtures. The original verdicts remain associated with the initial candidate. See the [replay evidence](evidence/acceptance-b93b732.md).

| ID | Verdict | Observed result |
| --- | --- | --- |
| MM-07 | OK (Tester) | A retained its claim during waiting and rejection. B progressed independently. Slots released after verified closure. |
| MM-08 | OK (Tester) | A ready Batch coexisted with a standalone Card, then started after Card closure while B remained active. Board regressions preserved move ownership and Card WIP. |
| MM-11 | OK (Tester) | The first integration excluded a concurrent one. An advance of main invalidated earlier verification. The resumed A integration used the new main. |
| MM-12 | OK (Tester) | The original stale decision now blocks closure even after combined checks pass. Recovery also refused the stale decision. B published while A kept its module claim. A rechecked and closed with a new fixture decision on the combined revision. The incompatible case remained blocked. |
| MM-13 | OK (Tester) | Accepted and rejected interruption recovery was idempotent with the hook active. Retained refs matched the approved results. Rejected product stayed outside main. |

The corrected candidate also passed unchanged-product closure and artifact guard checks. No overall acceptance decision is recorded.
