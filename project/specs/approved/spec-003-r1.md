---
type: specification
id: "SPEC-003"
revision: "1"
---
# KRR acceptance fixes

## Expected outcome

KRR opens from Finder, validates repositories and supports safe watcher management. Its custom icon is visible in Finder and the Dock.

## Scope

The [Batch-003 acceptance report](../../batches/batch-003/report.md) records the missing validator error and the empty pop-up that made KRR unresponsive. Watcher management and icon verification remain open.

## Acceptance criteria

- Open the signed app from Finder. A configured repository opens the New Watcher form. A nested directory, a plain Git repository and an invalid board each produce an actionable error. Dismiss each error and verify that KRR remains responsive.
- Verify creation, activation and safe management using isolated jobs for Codex and Claude Code. Confirm existing jobs and active runs are preserved.
- Verify the custom icon in Finder and the Dock.

## Required acceptance scenarios

Carry forward all four scenarios from the [Batch-003 acceptance tests](../../batches/batch-003/tests.md#uat-01-case-results). Record each verdict against the new signed build.

1. UAT-01 — Replay the configured-root KO from Finder, then run the three previously blocked cases: nested path, plain Git repository, and invalid board. Verify the form and dismissible diagnostics.
2. UAT-02 — Create a disabled watcher for each engine, verify persistence, and confirm that a label collision preserves the existing job.
3. UAT-03 — Verify activation, Run Now, editing, and deletion on isolated fixtures. Confirm that existing jobs and active runs are preserved.
4. UAT-04 — Verify the custom icon in Finder and the Dock at small sizes.
