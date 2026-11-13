---
type: tests
id: "TESTS-005"
batch: "Batch-005"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

- Tested commit: `d192a4ddab27d8c830fb2e8ca15fa4a388808cae`
- Technical evidence: Signed macOS bundle and isolated UUID collision retry check.

| ID | Scenario | Expected result | Verdict |
| --- | --- | --- | --- |
| UAT-01 | Inspect the compact watcher list with isolated fixtures. | Actions and states match Ready, Disabled, Running, and Deactivating. | No individual verdict recorded |
| UAT-02 | Change Appearance and relaunch. | System, Light, and Dark apply and the selection persists. | No individual verdict recorded |
| UAT-03 | Create, rename and change the icon of a watcher. | Name and icon persist while the launchd label stays fixed. | No individual verdict recorded |
| UAT-04 | Create two watchers for the same repository and simulate a label collision. | Generated labels are distinct, a collision is retried, and existing labels are preserved. | No individual verdict recorded |

- Visual check — KO (User). The empty-state text wraps into fragments and the creation sheet uses a cramped scrolling form. [Creation sheet](evidence/creation-ko.png) · [Empty state](evidence/empty-state-ko.png).

The User accepted the delivery with the creation form visual gap. Candidate revision: `50f0d923036e7d597e4d2cb2e6475b38cfababfb`. Earlier results and screenshots refer to the earlier build.
