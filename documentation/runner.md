# Use the macOS companion

Kanban Rememory Runner, or KRR, is an optional native macOS app for managing repository watchers using the Codex or Claude Code command-line engines. The Markdown framework works independently of the app.

## What a watcher does today

A watcher associates a repository, an engine and a cadence. Current watchers request a read-only board summary. They do not yet start development, dispatch corrections or close Batches automatically. Automated Batch dispatch remains work to implement.

Ask Development Agent to prepare the app and provide its exact location and startup instructions. The app needs a supported installed engine and a repository configured for Kanban Rememory. Its current repository check also requires the Specification and Batch directories.

## Create a watcher

The plus button opens the New Watcher form. Choose a name, select or paste the repository location, select a detected engine, choose how often it should run and choose an icon. The app checks the repository configuration. If no supported engine is detected, creation is unavailable.

A new watcher starts disabled. Activation schedules it. Run Now is available when its service is enabled, loaded and idle. The watcher's technical identifier stays fixed when its display name changes.

## Edit or remove a watcher

Deactivate a KRR-managed watcher before editing or deleting it. If a run is active, wait for it to finish and complete deactivation. The app can also show recognized existing engine watchers; only those it owns can be edited or deleted.

The menu-bar icon opens the application window. Project scope, acceptance decisions and delivery evidence remain in the framework's records.

Return to [the guide index](index.md).
