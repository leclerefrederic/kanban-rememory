---
type: card
id: "TASK-00000086"
batch: null
specifications: []
---

# TASK-00000086 — Group companion app sources and builds under apps

- Owner: Development Agent
- Dependencies: None.
- Priority: Explicit User request to group application code and builds under apps.

## Expected outcome

Group the KRR companion under `apps/krr/`, with `src/` and `build/` subdirectories retaining their macOS and Windows platform layout. Keep the reusable framework tools at the repository root.

Scope: directory relocation, build-script resource paths, ignore rules and current documentation. Preserve existing local generated files and historical approved Specification contents. Verify a full app build in an isolated temporary output, without changing product behavior or replacing an acceptance artifact.

## Acceptance criteria

- [x] Move existing sources and generated-output directories into `apps/krr/`, preserving their contents and tracked platform placeholders.
- [x] Resolve framework validator resources correctly from the relocated build script; default output belongs under the app's build directory.
- [x] Update ignore rules and current documentation; keep generated outputs untracked and historical approved scope unchanged.
- [x] Verify shell syntax, a complete isolated macOS build with bundled validator/icon and signature, repository validation and the diff before publication.

## Execution and evidence

- State: verified
- Actual start: 2026-11-14
- Actual finish: 2026-11-14
- Blocker: None.

- Starting revision: `5fc6eaa`. Moved the source and build trees into `apps/krr/`, preserving all 199 existing files during relocation. Tracked source/assets/placeholders remain byte-for-byte identical except for the build script's repository-root lookup and validator copy paths. The default app output resolves inside the relocated build directory.
- Updated ignore rules, the README and [Runner build procedure](../../../agents/runner/build-and-run.md). Verified source and platform placeholders remain trackable while generated outputs remain ignored. Historical approved Specification contents remain unchanged.
- `bash -n apps/krr/src/macos/build-app.sh` passed. Ran a complete build into an isolated temporary output. The initial confined attempt could not launch SwiftUI macros; the authorized retry outside confinement passed. Verified the executable, ICNS asset, byte-identical bundled validator modules, bundled validator execution against this repository, and strict code signature. The app was not launched. Removed the temporary verification bundle afterward.
- Board validation and whitespace checks passed. Reviewed the build-script change, documentation and ignore rules; checked existing generated files were preserved under the new path. No product behavior changed.
- Flow review: no active Batch or competing Card, no blocker. Unrelated local files remain untouched. Next action: publish the closed Card and verified layout under standing authorization.

## History

- 2026-11-14 — User requested an apps directory containing source code and builds. The prior documentation Card is published. No Batch or other Card is active.

- 2026-11-14T01:49:40+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-14T01:52:11+01:00 — Stage moved from `development` to `completion`.
