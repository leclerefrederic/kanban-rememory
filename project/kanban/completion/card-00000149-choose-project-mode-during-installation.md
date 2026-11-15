---
type: card
id: "CARD-00000149"
batch: null
specifications: []
---

# CARD-00000149 — Choose project mode during installation

- Owner: KR Developer
- Dependencies: None.

## Expected outcome

During guided installation, the User chooses between a single project with one board and a solution with independently tracked modules. The agent prepares and applies the approved layout for that choice.

## Scope and authorization

- Ask explicitly at initial installation, in both express and custom flows, unless the User already gave an unambiguous choice. Use the answer when presenting the existing setup proposal.
- For a single project, use the existing `project/` setup without creating a root `project.json`. For multi-module, collect the module names, reuse the existing manifest and preview procedures, and apply the agreed layout after approval.
- Explain both choices in the human installation guide. On upgrades, preserve the installed mode unless the User explicitly requests migration.
- The User authorized development on 2026-11-15. Migration of this Kanban Rememory repository is a separate follow-up after this Card closes.

## Acceptance criteria

- [x] Walk through express and custom installation in disposable projects. The agent explains both modes and asks for the choice once, or reuses an explicit answer.
- [x] Choose single-project mode and approve the proposal. The existing board and journal are created, with no root manifest.
- [x] Choose multi-module mode with two modules. The preview shows the workspaces and shared journal without writing them. After approval, the root manifest, separate boards and journals, and shared journal match the proposal.
- [x] Reopen or upgrade an existing installation in each mode. The configured mode is preserved, and fresh sessions recover it.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:
- Verified product revision: `d0f4797f35a6b4647e71b04278e89b3eb449ecae`.
- Reviewed the scoped diff in Development. Reviewed the guided choice and upgrade branches, then exercised the four express/custom and single-project/multi-module combinations against the delivered commands in disposable Git repositories. Previews made no writes. Approved single-project setup had no manifest. Multi-module setup created A/B boards and journals and shared memory without moving sources. Fresh CLI processes reopened and validated each layout without changes. The prompt and upgrade routing were verified by procedure walkthrough; no fresh native chat was run.
- All 42 Kanban tests and board validation passed. [Rememory](../../rememory/2026-11-15.md).

## History

- 2026-11-15T15:09:10+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T15:11:33+01:00 — Stage moved from `development` to `completion`.
