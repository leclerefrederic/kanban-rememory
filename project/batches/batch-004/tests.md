---
type: tests
id: "TESTS-004"
batch: "Batch-004"
---

# Acceptance tests


- Tested commit: `410e53bf50a7c8037991f4d7217eed538919d706`
- Environment or prerequisites:
- Technical evidence:

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| UAT-01 | SPEC-003 | Launch from Finder and run the four repository preflight cases. | Valid root opens the form; invalid selections show dismissible diagnostics. | OK (4/4) | `410e53b` | See case results. |
| UAT-02 | SPEC-003 | Create isolated watchers for both engines and try a label collision. | Both start disabled; collision preserves the existing job. | OK (3/3) | `410e53b` | See case results. |
| UAT-03 | SPEC-003 | Verify management and Run Now on isolated jobs. | Existing jobs and active runs are preserved. | OK after correction | `410e53b` | See case results. |
| UAT-04 | SPEC-003 | Check the icon in Finder and Dock. | The custom icon is visible and legible. | OK (User) | `410e53b` | Confirmed in Finder and Dock. |

Retain earlier attempts. Link screenshots under `evidence/`. For blocked or unexecuted required tests, record the reason and original scenario reference when carried forward.

## UAT-01 case results

- Case 1 of 4, configured repository root — OK (User, 2026-11-13). On build `410e53bf50a7c8037991f4d7217eed538919d706`, the New Watcher form opened with the expected engine choices, interval and label, and the app remained responsive.
- Acceptance testing is paused at the User's request. Cases 2–4 remain pending.

- Acceptance resumed at the User’s request on the same verified build.

- Case 2 of 4, nested directory — OK (User, 2026-11-13). The User suggested automatically resolving a selected subdirectory to its Git root as a future improvement.

- Case 3 of 4, plain Git repository — OK (User, 2026-11-13). The User requested a summary of the repository checks after acceptance testing.

- Case 4 of 4, incomplete board — OK (User, 2026-11-13).

## UAT-02 case results

- Case 1, disabled Codex watcher — OK (User, build `410e53b`). The User requested renaming the button from Create Disabled Watcher to Create Watcher.

- Case 2, disabled Claude Code watcher — OK (User, build `410e53b`).

- Case 3, label collision — OK (User, build `410e53b`). The duplicate was refused. The alert exposed a filesystem error. The User requested disabling Create Watcher when the label already exists and showing an inline explanation. [Screenshot](evidence/uat-02-case-3-label-collision.png).

## UAT-03 case results

- Case 1, activate the isolated Claude Code watcher — KO (User, build `410e53b`). The Activate Watcher button was disabled. The Run Now case depends on activation and is blocked. Screenshot and displayed service state requested.

  - Screenshot received: service state is Not loaded. Activate Watcher appears enabled and Run Now appears disabled. Activation has not yet been confirmed. [Screenshot](evidence/uat-03-case-1-activation.png).

- Case 1 retest, same build — OK (User). Activation succeeded after identifying the Activate Watcher control. The User flagged confusing ergonomics around Activate Watcher and the disabled Run Now control. The initial observation and screenshot are retained.

- Case 2, Run Now on the isolated Claude Code watcher — OK (User, build `410e53b`).

- Case 3, edit the interval of the isolated disabled Codex watcher — OK (User, build `410e53b`). The User noted that Edit Watcher should edit all watcher settings; if only the interval is editable, the button should be named Change Frequency.

- Case 4, delete the isolated disabled edit fixture — OK (User, build `410e53b`). The User confirmed deletion.

- Activated watcher deletion — KO (User, build `410e53b`). The Codex fixture shows `not running` but remains loaded. KRR offers neither deactivation nor deletion for the installed watcher. This blocks in-app cleanup of activated fixtures. The earlier deletion OK applies to the disabled fixture only. [Screenshot](evidence/uat-03-activated-watcher-deletion.png).

- Same-session correction retest — OK (User, 2026-11-13). The User confirmed deletion of both previously activated UAT watchers. Signed bundle: KRR Batch-004 same-session.app. Executable SHA-256: `ba0e420d102a39951870089b07ac7aae1aa36573f46f62f9e6d367d9de5e5ccc`. The corrected source was subsequently recorded as `e45fa9cf626a945a126f29d84c21534a98d82750`.

- Active-run protection, isolated launchd check — OK (Development Agent). A temporary LaunchAgent kept the same PID after disable, completed normally, and was unloaded only after reaching not running. Exactly one run was observed. This verifies the launchd sequence directly.
