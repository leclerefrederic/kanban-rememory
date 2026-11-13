---
type: tests
id: "TESTS-002"
batch: "Batch-002"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

| ID | Specification | Action | Expected result | Verdict |
| --- | --- | --- | --- | --- |
| UAT-01 | SPEC-002 | Open the app with isolated Codex, Claude Code, unrelated, and ambiguous fixture jobs. | Only the verified watchers appear. | Pending |
| UAT-02 | SPEC-002 | Edit, run, and delete both supported watchers. | Other jobs and user files remain intact, and Run Now cannot interrupt an active run. | Pending |
| UAT-03 | SPEC-002 | Check idle results, event retention, and repeated failures, then restart. | Latest result is current and history is bounded and deduplicated. | Pending |
| UAT-04 | SPEC-002 | Build and open the app and inspect Finder and Dock. | The app opens with its bundled icon and build output is ignored. | Pending |
