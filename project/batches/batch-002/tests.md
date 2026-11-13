---
type: tests
id: "TESTS-002"
batch: "Batch-002"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

| ID | Specification | Action | Expected result | Verdict |
| --- | --- | --- | --- | --- |
| UAT-01 | SPEC-002 | Open the app with isolated Codex, Claude Code, unrelated, and ambiguous fixture jobs. | Only the verified watchers appear. | OK (User, 2026-11-13, isolated plist fixtures) |
| UAT-02 | SPEC-002 | Edit, run, and delete both supported watchers. | Other jobs and user files remain intact, and Run Now cannot interrupt an active run. | Blocked: edit and delete are disabled for discovered watchers; live execution is unverified. |
| UAT-03 | SPEC-002 | Check idle results, event retention, and repeated failures, then restart. | Latest result is current and history is bounded and deduplicated. | OK (User, isolated storage test); app restart verification pending |
| UAT-04 | SPEC-002 | Build and open the app and inspect Finder and Dock. | The app opens with its bundled icon and build output is ignored. | KO (User, three attempts; icon absent in Finder and Dock). Fix deferred to Batch-003. |

Delivery verification revision: `455afcb98a4df24c0f8b6658ed65bb61869d7aed`. The committed source was rebuilt and signature-verified. User verdicts refer to local UAT builds.
