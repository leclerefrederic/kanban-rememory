# Start Kanban Rememory Runner on macOS

KRR manages repository watchers for the Codex and Claude Code command-line engines. Current watchers request a read-only board summary. They do not pick up, correct, close, or publish Batches. The [scheduled-job procedure](../run-scheduled-batch-job.md) describes the separate dispatch work still needed.

## Prerequisites

- macOS 13 or later.
- Apple command-line developer tools with `xcrun swiftc`, Git, `sips`, `iconutil`, and `codesign` available.
- Python 3.9 or later at `/usr/bin/python3`, which the current app uses for repository validation.
- At least one installed, authenticated `codex` or `claude` executable to create a watcher.
- A repository configured with Kanban Rememory. The current app also requires `project/specs/draft/`, `ready/`, `approved/`, and `project/batches/`, even for a summary watcher. See [framework setup](../install-in-a-project.md).

The app detects executables from its PATH and common locations: `~/.local/bin`, `~/.npm-global/bin`, `/opt/homebrew/bin`, `/usr/local/bin`, and `/usr/bin`. Shell aliases alone are not executable files the app can discover.

## Source and output layout

The companion application lives under `apps/krr/`. Sources are in `src/macos/` and generated output is in `build/macos/`, relative to that application directory. The `src/windows/` and `build/windows/` directories reserve space for future Windows work. Generated files stay ignored; platform placeholders remain tracked.

The framework's reusable commands live under `agents/tools/`. The build script copies the board validator from there into the app bundle.

## Build and open

From the Kanban Rememory source repository root:

```sh
bash apps/krr/src/macos/build-app.sh
open "apps/krr/build/macos/Kanban Rememory Runner.app"
```

The script compiles the Swift sources, bundles the icon and validator, signs locally, and verifies that signature. Its output is a local development build. Building again replaces that output; if a Batch is under acceptance, preserve its candidate and pass a separate output path instead:

```sh
bash apps/krr/src/macos/build-app.sh "apps/krr/build/macos/krr-correction.app"
open "apps/krr/build/macos/krr-correction.app"
```

Use the exact path and revision recorded in the Batch's tests when running acceptance. Follow the Batch artifact guard before replacing or cleaning any candidate. In this repository, the Batch guard record lists `build-app.sh` in `full_build_files`: a change to it requires a recorded successful full build before publication.

## Create and manage a watcher

1. Click **+** to open **New Watcher**.
2. Enter a **Watcher Name** and paste a repository path or use **Browse…**. Verify the repository; a selected subdirectory resolves to its Git root.
3. Select a detected **Engine**, set **Run every** in minutes, and choose an **Icon**. Creation stays unavailable when no supported CLI is detected.
4. Click **Create Watcher**. The watcher starts disabled; **Activate** schedules it. **Run Now** is available when the service is enabled, loaded, and idle.
5. Deactivate a KRR-managed watcher before editing or deleting it. If a run is still active, wait for it to finish and complete deactivation. The app also lists recognized existing engine watchers, but only those it owns can be edited or deleted.

The Watcher Name can change; the generated `krr.<uuid>` service label stays fixed. The menu-bar icon opens the app window.

## Start a Claude Code task in a Terminal window

Use **Claude Task** in the toolbar, choose the repository folder, describe the task you authorize and press **Start**. KRR opens Claude Code interactively in its own Terminal window and minimizes that window. The repository needs `agents/tools/krr-signal.py` and `agents/tools/configure-telegram.py`, and a detected `claude` executable. Claude Code asks for tool permissions in that window as usual.

KRR appends instructions that make Claude run `python3 agents/tools/krr-signal.py waiting --id ID` before it asks you something, and `krr-signal.py resumed` once it continues. Only these explicit signals count; a slow command or silence never does. On `waiting`, KRR restores and raises that window, and sends one Telegram `attention` alert through `configure-telegram.py run --send`. The window comes forward even when Telegram is disabled or fails. When Claude resumes, KRR minimizes the window again. Repeating a signal with the same ID changes nothing. Other Terminal windows are never touched.

The **Claude sessions** list shows Working, Waiting for you or Ended. When the window closes or Claude exits, the session is marked ended and cannot be answered. Sessions are not restored when KRR quits.

The first use asks for macOS Automation permission to control Terminal; allow it under System Settings, Privacy & Security, Automation. Not covered: Claude Code's own permission dialogs, recovery after a session ends, answering from Telegram.

Run the logic tests with `bash apps/krr/tests/macos/run-tests.sh` and `python3 agents/tools/test-krr-signal.py`.

## Repository checks

Before creation, KRR checks the Git root, root `AGENTS.md`, readable `project/kanban/workflow.json`, every configured stage directory, the Batch directories listed above, and the bundled board validator's result. These are structural checks; they do not establish that product tests passed or that a Batch is accepted.

If validation reports a missing directory or broken reference, correct the project setup and verify again. If no engine is detected, check for a real executable in the searched locations and reopen the form. Build or validation errors should be investigated before activating a watcher.
