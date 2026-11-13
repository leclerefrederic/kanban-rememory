---
type: tests
id: "TESTS-003"
batch: "Batch-003"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

| ID | Specification | Action | Expected result | Verdict |
| --- | --- | --- | --- | --- |
| UAT-01 | SPEC-002 | Select configured, nested, plain Git, and invalid board directories. | Only the configured root passes. | Pending |
| UAT-02 | SPEC-002 | Create a watcher for each engine, including a label collision. | New watchers are disabled and existing jobs are preserved. | Pending |
| UAT-03 | SPEC-002 | Exercise management and run controls on isolated jobs. | Active runs and unrelated jobs are preserved. | Pending |
| UAT-04 | SPEC-002 | Open the app from Finder and inspect the Dock. | The custom icon appears in both. | Pending |
