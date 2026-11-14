# Start Kanban Rememory Runner on macOS

KRR manages repository watchers for the Codex and Claude Code command-line engines. Current watchers request a read-only board summary. They do not pick up, correct, close, or publish Batches. The [scheduled-job procedure](../agents/run-scheduled-batch-job.md) describes the separate dispatch work still needed.

## Prerequisites

- macOS 13 or later.
- Apple command-line developer tools with `xcrun swiftc`, Git, `sips`, `iconutil`, and `codesign` available.
- Python 3.9 or later at `/usr/bin/python3`, which the current app uses for repository validation.
- At least one installed, authenticated `codex` or `claude` executable to create a watcher.
- A repository configured with Kanban Rememory. The current app also requires `project/specs/draft/`, `ready/`, `approved/`, and `project/batches/`, even for a summary watcher. See [framework setup](../getting-started.md).

The app detects executables from its PATH and common locations: `~/.local/bin`, `~/.npm-global/bin`, `/opt/homebrew/bin`, `/usr/local/bin`, and `/usr/bin`. Shell aliases alone are not executable files the app can discover.

## Build and open

From the Kanban Rememory source repository root:

```sh
bash src/macos/build-app.sh
open "build/macos/Kanban Rememory Runner.app"
```

The script compiles the Swift sources, bundles the icon and validator, signs locally, and verifies that signature. Its output is a local development build. Building again replaces that output; if a Batch is under acceptance, preserve its candidate and pass a separate output path instead:

```sh
bash src/macos/build-app.sh "build/macos/krr-correction.app"
open "build/macos/krr-correction.app"
```

Use the exact path and revision recorded in the Batch's tests when running acceptance. Follow the Batch artifact guard before replacing or cleaning any candidate.

## Create and manage a watcher

1. Click **+** to open **New Watcher**.
2. Enter a **Watcher Name** and paste a repository path or use **Browse…**. Verify the repository; a selected subdirectory resolves to its Git root.
3. Select a detected **Engine**, set **Run every** in minutes, and choose an **Icon**. Creation stays unavailable when no supported CLI is detected.
4. Click **Create Watcher**. The watcher starts disabled; **Activate** schedules it. **Run Now** is available when the service is enabled, loaded, and idle.
5. Deactivate a KRR-managed watcher before editing or deleting it. If a run is still active, wait for it to finish and complete deactivation. The app also lists recognized existing engine watchers, but only those it owns can be edited or deleted.

The Watcher Name can change; the generated `krr.<uuid>` service label stays fixed. The menu-bar icon opens the app window.

## Repository checks

Before creation, KRR checks the Git root, root `AGENTS.md`, readable `project/kanban/workflow.json`, every configured stage directory, the Batch directories listed above, and the bundled board validator's result. These are structural checks; they do not establish that product tests passed or that a Batch is accepted.

If validation reports a missing directory or broken reference, correct the project setup and verify again. If no engine is detected, check for a real executable in the searched locations and reopen the form. Build or validation errors should be investigated before activating a watcher.
