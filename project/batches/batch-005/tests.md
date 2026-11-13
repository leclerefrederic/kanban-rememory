---
type: tests
id: "TESTS-005"
batch: "Batch-005"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

- Tested commit:
- Technical evidence:

| ID | Scenario | Expected result | Verdict |
| --- | --- | --- | --- |
| UAT-01 | Inspect the compact watcher list with isolated fixtures. | Actions and states match Ready, Disabled, Running, and Deactivating. | Pending |
| UAT-02 | Change Appearance and relaunch. | System, Light, and Dark apply and the selection persists. | Pending |
| UAT-03 | Create, rename and change the icon of a watcher. | Name and icon persist while the launchd label stays fixed. | Pending |
| UAT-04 | Create two watchers for the same repository and simulate a label collision. | Generated labels are distinct, a collision is retried, and existing labels are preserved. | Pending |
