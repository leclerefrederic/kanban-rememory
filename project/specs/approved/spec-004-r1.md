---
type: specification
id: "SPEC-004"
revision: "1"
---
# KRR watcher interface redesign

## Expected outcome

Users can identify a watcher, understand its state, and act on it from a compact native macOS window.

## Scope

- Show the watcher name, chosen icon, engine, and state on each row. Show **Run Now** for Ready and **Activate** for Disabled. Show progress for Running and explain the wait for Deactivating. Group secondary actions in the row menu. Put the technical label, paths, and history in details.
- Provide **System**, **Light**, and **Dark** in Settings under **Appearance**. Apply the choice throughout the app and persist it across relaunches.
- Offer a built-in icon picker in **New Watcher** and **Edit Watcher**, with a default icon and choices for folders, code, documents, servers, terminals, and tools.
- Require **Watcher Name** at creation and let users rename it in **Edit Watcher**. Store the display name and icon locally against the service label.
- Generate a launchd label in the form `krr.<uuid>` using a random UUID v4 at creation. Check for collisions in local configurations and launchd. Generate a new UUID if the label is taken, and reserve the configuration without overwriting an existing file, including during concurrent creation. Keep the label fixed for the lifetime of the watcher. Preserve existing watcher labels. Remove the Purpose and suffix controls from creation and editing.
- Use **Create Watcher** and explain that new watchers start disabled. Resolve generated label collisions automatically. Show an actionable error if creation cannot complete. Preserve existing ownership and active-run safeguards.

## Acceptance criteria

- Verify the compact list and available actions for Ready, Disabled, Running, and Deactivating watchers.
- Switch between System, Light, and Dark and verify appearance, contrast, and persistence after relaunch.
- Create a named watcher with a selected icon. Rename it and change its icon. Verify persistence after relaunch and confirm the same launchd service label is used throughout.
- Simulate a UUID collision and verify that creation retries with a fresh label and preserves the existing watcher. Verify that two watchers for the same repository have distinct labels and that existing watchers retain their original labels.

## Resources

- [Watcher list and creation mockup](../resources/active/krr-watchers-and-creation.png) illustrates the compact list and creation layout. Use **Watcher Name** in place of **Purpose**. Generated label collisions are retried automatically.
- [Light and Dark appearance mockup](../resources/active/krr-light-and-dark-appearance.png) illustrates the appearance control and consistent action placement across themes.
