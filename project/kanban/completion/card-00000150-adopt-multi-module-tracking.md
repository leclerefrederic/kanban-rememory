---
type: card
id: "CARD-00000150"
batch: null
specifications: []
---

# CARD-00000150 — Adopt multi-module tracking in Kanban Rememory

- Owner: KR Developer
- Dependencies: [CARD-00000149](../completion/card-00000149-choose-project-mode-during-installation.md), completed.
- Prerequisite before migration: deliver one project-wide Kanban with scoped Cards and journal routing. [SPEC-021 r1](../../specs/approved/spec-021-r1.md) documents the earlier board-per-module design.

## Expected outcome

Adopt multi-module tracking in this repository. One project Kanban tracks Cards across the eight modules. Each module has its own Specs, Batches and journal. Sources, agent instructions, documentation, Git main and project memory are shared.

## Scope and authorization

On 2026-11-15 the User explicitly authorized execution of this Card and migration to the eight modules below. Preserve the former board as an archive. Notify the User via the configured Telegram bot after verified publication.

| Module | Work assigned to it | Workspace |
| --- | --- | --- |
| Configuration Module | Installation, project manifest, project modes and workspace configuration | `project/modules/configuration/` |
| Kanban Module | Cards, priorities, transitions, dependencies and Card WIP | `project/modules/kanban/` |
| Specification Module | Specification authoring, revisions, approval state and retirement | `project/modules/specifications/` |
| Delivery Module | Batch selection, exact candidate, integration, publication and closure | `project/modules/deliveries/` |
| Acceptance Testing Module | Guided acceptance, case verdicts and evidence against the tested candidate | `project/modules/acceptance/` |
| Agent Module | Roles, permissions, delegation and host adapters | `project/modules/agents/` |
| Memory Module | Journals, milestones, checkpoints and work resumption | `project/modules/memory/` |
| Notification Module | Notification configuration, messages, transport and deduplication | `project/modules/notifications/` |

Record one primary scope on each Card: the owning module or the project. A Batch about notifications lives in `notifications/batches/`; a change to how KR publishes Batches belongs to Delivery. A change to global journal behavior belongs to Memory. Name one owner and check other affected modules. Remy is this project's configured bot. Telegram uses the privately configured bot and recipient.

### Record ownership

| Record | Information it owns |
| --- | --- |
| Project Card | Operational task, scope, owner, stage, blocker and completion checks. Links to related delivery and evidence. |
| Module Spec or Batch | Expected behavior and its revision in the Spec. Delivery state, tested candidate, verdicts and closure in the Batch records. |
| Project Rememory | Decisions affecting the solution and one short milestone per verified publication, including single-module work. Include scope, outcome, commit and a link to the Card or Batch. |
| Module Rememory | Durable technical rationale and resumption notes specific to the module. Link to any existing checks and evidence. Add an entry when it helps a future session. |

Use the Card's scope to route work notes. Project-scoped notes belong in project Rememory. Keep the detail in one place and link to it from other records. A small change documented fully in its Card only needs the global publication milestone.

### Proposed cutover

1. Use the delivered shared-board configuration. Propose root `project.json` for `kanban-rememory`, the eight workspaces above, shared `agents/` and `documentation/`, and global `project/rememory/`. Keep the project's stages and Europe/Paris time. Apply per-module capacity to the shared board, require a branch and worktree for each delivery, and serialize integrations. Keep the existing publication policy. Operate from one shared clone after cutover.
2. Treat the existing tracking history as an archive. Preserve frozen files at their original paths and link to them in the global journal. Preserve local drafts in place and outside the publication. Assign future work on SPEC-005 to Delivery and SPEC-013 to Notification by separate decision.
3. In an isolated clone on `codex/card-00000150`, review the scoped diff and rehearse opt-in while this Card is in Development. Verify the shared board, eight workspaces, scope selection and journal routing. Exercise independent deliveries in two modules, competing claims within one module, serialized integration and module identity in notifications with a simulated transport. Reuse the existing Telegram configuration.
4. After checks, complete this migration Card on the legacy board in the isolated publication checkout. Activate from that clone's principal checkout after confirming no active Card/Batch, verify the actual combined revision, then publish the activation and closure together only if the observed remote main is still the agreed baseline. Reconcile the user's primary checkout while preserving unrelated work. Record the closing revision, global transition entry and verified publication before sending the completion alert.
5. If verification fails before publication, keep the existing main. If a rollback is required after publication, first stop and reconcile new module work, then use a reviewed revert without rewriting history or discarding module records.

## Acceptance criteria

- [x] Preview lists one project Kanban, the eight workspaces and the global journal. Approved activation creates the scoped tracking layout and preserves shared source locations.
- [x] The exact release has no active legacy Card/Batch at activation. Historical records retain paths, IDs and bytes; local drafts remain outside the migration commit; global Rememory links to the old board and Batch records.
- [x] The project board validates and can show work by module. Fresh sessions resolve the intended scope. Verify per-module capacity, serialized integration and scoped Telegram messages in disposable fixtures.
- [x] Verify a module-scoped and a project-scoped Card. Local context is routed by scope. Each verified publication adds one global milestone and links to its details. A small Card with sufficient context creates no duplicate module entry.
- [x] Review tests and diff in Development, close the legacy migration Card before activation, verify the combined revision and publish only the approved cutover. Verify remote main and the primary checkout without overwriting unrelated local changes.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

- Verified base: `20ba4bb62c847c4608f09897e43313a1f989e6d6`. Verified manifest SHA-256: `74d9a5eab643d26094ff2a7f1cafd08c0d7cf745524c9c477e6959b1396dc00f`. The publication milestone in [project Rememory](../../rememory/2026-11-15.md) records the published revision.
- Reviewed the planned configuration and repository policy in Development. A disposable clone successfully previewed and activated the exact manifest, found 64 record directories across eight workspaces, and created one disposable Card per module and one in project scope. The shared board showed each once. The project workflow and archived Card paths and bytes were preserved.
- Seven focused checks passed in disposable repositories: activation and frozen history, shared-board commands, concurrent ownership, per-scope capacity, journal routing, publication and recovery, and simulated Telegram routing. Verification used fresh CLI processes and local Git remotes.
- Review of the approved cutover found no active Card or Batch after this closure. Keep historic decisions and file paths available through [the archive lookup](../../../agents/actions/manage-board.md#inspect-and-validate). The pre-push guard protects the published manifest; any later reversal requires a separately reviewed migration after reconciling module work.

## History

- 2026-11-15T16:42:39+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T16:44:52+01:00 — Stage moved from `development` to `completion`.
