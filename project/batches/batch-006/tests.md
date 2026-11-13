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
| UAT-01 | SPEC-008 | Compare both forms and the icon picker in Light and Dark. | Match the approved mockup and keep the fixed window size. | OK (User, four cases) |
| UAT-02 | SPEC-008 | Open New Watcher and exercise repository input and engine detection. | The form opens directly, resolves the repository root, and handles available and missing engines. | Pending |
| UAT-03 | SPEC-007 | Attempt editing while disabled, activated, running, and deactivating. | Only fully deactivated managed watchers can be edited. Save rechecks eligibility and preserves the service label. | Pending |
| UAT-04 | SPEC-006 | Exercise the menu bar panel and close the main window or quit KRR. | The panel shares watcher state, opens Settings and the main window, and quitting leaves loaded watchers registered. | Pending |

Present startup instructions before each case, then actions, expected results, and the OK / KO prompt.

## UAT-01 case results

- Case 1, New Watcher in Dark — OK (User). The User reported small controls and text, uneven spacing, and roughly one third of the window unused. No screenshot file could be copied.

- Case 2, New Watcher and icon picker in Light — OK (User).

- Case 3, Edit Watcher in Light with cancellation — OK (User).

- Case 4, Edit Watcher in Dark — OK (User). The User requested no further repetition of identical functional cases across color schemes.

## UAT-02 case results

- Case 1, Git root resolution — OK (User). Replace the success message with unobtrusive feedback that does not shift the form fields. Keep actionable validation errors visible.

- Case 2, repository drag and drop — OK (User) on the tested build. The User then withdrew this interaction due to the risk of moving a folder accidentally in Finder. The replacement candidate must reject drops and retain pasted paths, Browse, and Recent.

- Case 2 retest, no-drop candidate — OK (User) for pasted repository validation and Browse availability. No drag operation was attempted. The form no longer registers a folder drop handler.

- Case 3, recent repository — KO (User). The Recent control was absent in New Watcher. The build only exposes it when a saved recent repository value exists. Whether that value was saved in this session is unconfirmed.
  - Scope clarification: the User did not request Recent. Withdraw this case from acceptance. Remove the Recent control and its persistence from the next candidate. Keep pasted paths and Browse.

- Case 4, repository selection via Browse — OK (User, 2026-11-14, no-drop candidate).

- Case 5, engine detection — User reported no visible effect when clicking Codex or Claude Code. Selection highlight and engine availability still to be confirmed. The User requested removal of the New watchers start disabled footer text.

- Case 5 follow-up — OK for switching the highlighted engine. Missing-engine scenarios remain unverified.

- UAT-03 setup: the initial instructions were blocked because Locate Executable is hidden for detected engines. For the isolated retest, launch KRR with the stub directory first in PATH and verify the executable in Details before activation.

- Engine availability clarification: creation requires an automatically detected CLI for the selected engine. Unavailable engines cannot be selected. When no supported CLI is detected, disable Create Watcher and explain why. Remove the manual executable picker from New Watcher.

## Remaining acceptance scope

The User reported that the remaining checks were not testable in the current setup and that the behavior worked previously. Do not request these checks again in this session. Edit eligibility and menu bar access have no confirmed verdict on the current candidate. Keep these verification gaps separate from the scenarios already passed. CLI absence remains a technical check for the corrected candidate.

## Final delivery

The User accepted closure with the menu bar reduced to a single action that opens KRR. The status item uses the KRR text label. Final signed build revision: `c1da3532ba732150255fa9b54158740ba4cd83e2`. The final bundle compiled and passed signature verification. Prior UI verdicts apply to earlier builds. Live verification of the final menu bar click and edit guard remains outstanding.
