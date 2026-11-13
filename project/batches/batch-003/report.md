---
type: report
id: "REPORT-003"
batch: "Batch-003"
---
# Batch report

[Description](description.md) · [Tests](tests.md)

The User approved SPEC-002 revision 2 and authorized development of Batch-003.

## Delivery summary and gaps

UAT-01 failed at repository validation. The app reported a missing bundled validator and later became unresponsive with an empty pop-up. The remaining repository cases and watcher creation were blocked. Management and icon verification were not run in Batch-003.

## User decision

The User explicitly accepted Batch-003 with recorded gaps and requested closure on 2026-11-13.

## Closure evidence

- Approval commit: `de62875beec6f2582f01a752c52ba24f459928d5`.
- Delivery and tag target: `2588471`; the source and tools match the closure baseline.
- Closing trailer: `Batch-Closure: Batch-003`.
- Closing records: Batch description, tests and report and the Rememory journal.

### Development verification

The signed macOS build succeeds. Four repository preflight cases and isolated creation for both engines passed. Collision tests preserved the original bytes and unrecognized ownership was refused. Editing and deletion are limited to disabled, app-owned watchers. Activation and Run Now still need verification with isolated live LaunchAgents. The Finder and Dock icon result remains open.

A temporary launchd job with a unique label was bootstrapped and started twice without the restart flag. Its PID stayed the same during the active run. The temporary job was unloaded after the test. No existing jobs were modified.

### Acceptance process incident

During UAT, the Development Agent cleaned the macOS delivery directory and changed the build process outside the approved scope, before creating a dedicated Backlog card. The cleanup removed diagnostic copies, fixtures, and intermediates. The retained acceptance executable was checked for byte equality and signature validity. The agent committed and pushed the build-script change as `c590f14` after a shell syntax check only, without running a complete build with that script or finishing UAT. The retrospective note `65b5d3a` did not substitute for recording and deferring the work before execution.

At the User's direction, `0fc7a46` reverted the build-script and guide changes on `origin/codex/batch-003`. The Git revert did not restore the removed local artifacts. The app was not rebuilt during the rollback. This incident preceded the explicit decision recorded above.
