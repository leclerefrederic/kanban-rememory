---
type: card
id: "TASK-00000059"
batch: "Batch-003"
specifications: ["SPEC-002"]
---
# TASK-00000059 — Create and manage watchers safely

- Owner: Development Agent
- Dependencies: Batch-002 closed. Batch-003 has explicit User priority.

## Expected outcome

Implement and verify SPEC-002 revision 2.

## Acceptance criteria

- [ ] Verify repository preflight, watcher creation and management, and the icon.

## History

- 2026-11-13 — Authorized and moved to Development.
- 2026-11-13 — Connected New Watcher to repository selection and bundled validation. The signed app builds. Swift smoke checks passed for this repository, a nested path, a plain Git repository, and a board missing a stage. Installation and activation remain pending.
- 2026-11-13 — Retrospective record: during UAT, the Development Agent removed redundant local build artifacts and retained the signature-verified acceptance binary. Commit `c590f14` changed the build script and documented the single-bundle policy before the work was recorded on this card. Shell syntax passed. A full build of the revised script remains pending. Run it outside the current acceptance session before offering a replacement bundle for testing.
