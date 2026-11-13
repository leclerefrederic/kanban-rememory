---
type: specification
id: "SPEC-006"
revision: "1"
---
# KRR in the macOS menu bar

## Expected outcome

Users can check and control their watchers from the macOS menu bar without opening the main window.

## Scope

- Show a recognizable KRR icon in the macOS menu bar while the app is running, including when the main window is closed.
- Clicking the icon opens the compact watcher list defined in [SPEC-004](../approved/spec-004-r1.md). Reuse the watcher names, icons, engine, status, and available actions. Show **Run Now** for eligible ready watchers and **Activate** for eligible disabled watchers.
- Provide **Settings** with the existing **Appearance** preference and **Open KRR** to open or focus the main window.
- Use the same watcher state and safety checks as the main window. Quitting KRR removes the menu bar icon. Loaded watchers continue running through launchd.

**Open KRR** opens or focuses the [fixed-size Watchers window](spec-008-r1.md). Creation and editing take place over that window. Use the [same edit eligibility rules](spec-007-r1.md) for any edit action exposed from the menu bar.

## Acceptance criteria

- Close the main window and verify the menu bar icon remains available. Open the panel and verify that its watcher state matches the main window.
- Using isolated watchers, verify that the panel exposes the appropriate actions and that those actions update both views.
- Verify that **Open KRR** focuses the main window and that **Settings** exposes System, Light, and Dark.
- Quit KRR and verify that the icon disappears and an isolated loaded watcher remains registered with launchd.
