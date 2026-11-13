---
type: specification
id: "SPEC-002"
revision: "1"
---
# Kanban Rememory Runner v1

## Expected outcome

A native macOS app lets users discover and manage their existing Codex and Claude Code watchers from one window.

## Scope

- Build in Swift and SwiftUI for macOS 13 or later, with an English interface.
- Design a custom macOS app icon for Kanban Rememory Runner (KRR). Use a simple, recognizable mark that stays legible at small sizes. Keep the icon independent of the Codex and Claude Code brands and bundle it with the app.
- Name the app **Kanban Rememory Runner**. Call each managed configuration a **watcher** and use **Watchers**, **Edit Watcher**, **Delete Watcher**, and **Run Now** in the interface.
- For watchers managed by the app, use `kanban.rememory.<repo>` as the default LaunchAgent label, for example `kanban.rememory.kanban-rememory`. When a repository has multiple watchers, add a purpose suffix to distinguish them, for example `kanban.rememory.kanban-rememory.batch-closure`. Keep the label stable when switching between Codex and Claude Code. Preserve the labels of existing watchers.
- Discover user LaunchAgents that invoke Codex or Claude Code directly or through a recognized wrapper. Show the evidence used to identify the engine. Leave unrelated and ambiguous jobs outside the list.
- Discover verified watchers regardless of their label prefix. Determine edit and delete support from the configuration the app can safely manage.
- Show the engine, current service state, trigger, working directory when available, last run, and last result. Mark unavailable information as unknown.
- Allow editing and deletion of supported existing configurations. Explain when an identified watcher is read-only because its configuration cannot be changed safely. Preserve unrelated settings, confirm deletion, and keep user scripts and logs unless removal is explicitly selected for app-owned files.
- Offer Run Now for supported watchers when idle. Preserve the existing invocation and permissions and avoid restarting an active run.
- Keep the latest result separately and retain at most 20 significant events per watcher in app history. Idle checks update the latest result. Repeated identical errors share a row with a count and last occurrence. Bound technical logs owned by the app through rotation and preserve existing external logs and Batch records.
- Reuse existing Kanban Rememory Batch rules. Automated Batch pickup and closure are separate work, including TASK-00000039. Watcher creation is outside this Batch.

## Repository layout

Create this structure at the repository root:

```text
src/
  macos/
  windows/
build/
  macos/
  windows/
```

Place the Swift and SwiftUI project in `src/macos/` and write generated build artifacts to `build/macos/`. Reserve `src/windows/` and `build/windows/` for future Windows work. Keep empty directories with `.gitkeep` and ignore generated contents under `build/`.

## Acceptance criteria

- With Codex, Claude Code, an unrelated agent, and an ambiguous wrapper installed in a test environment, the list shows only the two verified watchers.
- Edit and reload a supported watcher for each engine, then delete it after confirmation. Verify the other services, user files, and settings remain intact. Simulate a failed reload and verify the original configuration remains recoverable.
- Run each watcher from the app and confirm that an active run cannot be interrupted or duplicated by Run Now.
- Verify idle runs update the latest result without adding history rows. Simulate more than 20 significant events and repeated identical failures. Verify retention and grouping after restarting the app.
- Build on macOS and run the above scenarios against isolated test LaunchAgents before using existing live jobs.
- Verify that the bundled KRR icon appears in Finder and the Dock and remains recognizable at small sizes.
- Verify that all four platform directories exist in a fresh clone and that macOS build artifacts are ignored by Git.
