---
type: card
id: "TASK-00000100"
batch: null
specifications: []
---

# TASK-00000100 — Record build-check files when creating a Batch guard record

- Owner: Development Agent
- Dependencies:

## Expected outcome

The Batch start procedure tells the agent to write `full_build_files` into a new guard record when the project has build files needing a full build before publication (in this repository, the patient-zero project, the KRR build script `apps/krr/src/macos/build-app.sh`). Follows [TASK-00000094](../completion/task-00000094-make-the-batch-guard-follow-the-configured-workflow.md), which made the list configurable and empty by default.

## Acceptance criteria

- [x] The guard record example in `agents/batches/start-and-close-batches.md` shows the optional `full_build_files` field and when to set it.
- [x] The User confirms the build-file name(s) to list for this repository.
- [x] The delivery example and adoption tests still pass; no rule's meaning changes.

## Execution and evidence

- State: completed
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker:

## History

- 2026-11-14T10:47:33+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T10:48:06+01:00 — Stage moved from `development` to `completion`.
