---
type: tests
id: "TESTS-003"
batch: "Batch-003"
---
# Acceptance tests

[Description](description.md) · [Report](report.md)

| ID | Specification | Action | Expected result | Verdict |
| --- | --- | --- | --- | --- |
| UAT-01 | SPEC-002 | Select configured, nested, plain Git, and invalid board directories. | Only the configured root passes. | KO — case 1 failed; cases 2–4 blocked |
| UAT-02 | SPEC-002 | Create a watcher for each engine, including a label collision. | New watchers are disabled and existing jobs are preserved. | Blocked by UAT-01 |
| UAT-03 | SPEC-002 | Exercise management and run controls on isolated jobs. | Active runs and unrelated jobs are preserved. | Not run — recipe ended after UAT-01 blocked progress |
| UAT-04 | SPEC-002 | Open the app from Finder and inspect the Dock. | The custom icon appears in both. | Not run in Batch-003 — icon fix remains open |

## UAT-01 case results

- Case 1 of 4, configured repository root — KO (User, 2026-11-13). The app displayed “Watcher operation failed” with “The bundled board validator is missing. Rebuild the app.”
  - The User launched the app from Finder. A read-only check found the running KRR instance at the expected acceptance bundle path. The validator file exists and an independent Foundation lookup resolves it. The in-app failure remains unexplained.
  - Case 1 follow-up: the User reported that relaunching from Finder displayed an empty pop-up and the app became unresponsive. No screenshot was supplied.

The User ended acceptance testing on 2026-11-13. The acceptance executable was built from the implementation preceding evidence-only commit `2588471`. The source and tools at the closure baseline match that commit. No replacement build was tested.
