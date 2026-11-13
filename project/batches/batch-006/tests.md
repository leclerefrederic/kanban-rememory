---
type: tests
id: "TESTS-006"
batch: "Batch-006"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

- Tested commit:

| ID | Specification | Scenario | Expected result | Verdict |
| --- | --- | --- | --- | --- |
| UAT-01 | SPEC-008 | Compare both forms and the icon picker in Light and Dark. | Match the approved mockup and keep the fixed window size. | Pending |
| UAT-02 | SPEC-008 | Open New Watcher and exercise repository input and engine detection. | The form opens directly, resolves the repository root, and handles available and missing engines. | Pending |
| UAT-03 | SPEC-007 | Attempt editing while disabled, activated, running, and deactivating. | Only fully deactivated managed watchers can be edited. Save rechecks eligibility and preserves the service label. | Pending |
| UAT-04 | SPEC-006 | Exercise the menu bar panel and close the main window or quit KRR. | The panel shares watcher state, opens Settings and the main window, and quitting leaves loaded watchers registered. | Pending |

Present startup instructions before each case, then actions, expected results, and the OK / KO prompt.
