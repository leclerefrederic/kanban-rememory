---
type: tests
id: "Batch-007-Tests"
batch: "Batch-007"
---

# Acceptance tests

User reported all acceptance tests OK on candidate `8d6528a`.

| ID | Verdict | Tested revision |
| --- | --- | --- |
| TEST-01 | OK | `8d6528a` |
| TEST-02 | OK | `8d6528a` |
| TEST-03 | OK | `8d6528a` |

- Tested candidate revision: `8d6528aa468f1f640f0e6bf4cdf0f82507654259`.
- Signed app: `/Users/fleclere/Documents/GitHub/kanban-rememory/apps/krr/build/macos/KRR Batch-007 Top Right.app`.
- Technical evidence: macOS compilation and strict signature verification passed. Prepare the isolated watcher fixture before TEST-03.

| ID | Startup | Action | Expected result |
| --- | --- | --- | --- |
| TEST-01 | Quit KRR. Open the signed candidate from Finder. | Inspect the app in Finder and in the Dock at a small icon size. | Both show the approved application icon. |
| TEST-02 | Quit KRR and open the signed candidate. Close its main window. | Inspect the status item in light and dark menu bar appearances, then click it repeatedly. Repeat on another display if available. | The symbol remains legible. A single Watchers window opens or comes forward at the top right of the clicked display. |
| TEST-03 | Open the signed candidate with an isolated KRR-owned watcher fixture. | Try editing the watcher while active. Deactivate it and try again. | Editing is unavailable while active and opens after deactivation completes. |

TEST-02 and TEST-03 carry forward the live checks outstanding in [Batch-006](../batch-006/tests.md#remaining-acceptance-scope). Also carry forward CLI absence as a technical check: with neither supported CLI detected, watcher creation stays unavailable.

## Prior attempt

- TEST-02 — KO on `a8359a9`. Repeated clicks opened multiple Watchers windows. [Screenshot](evidence/test-02-duplicate-windows.png).
