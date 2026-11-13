---
type: specification
id: "SPEC-008"
revision: "1"
---
# KRR window and watcher forms

## Expected outcome

Users can create and edit watchers within the compact Watchers window. This revision of the interface builds on [SPEC-004](../approved/spec-004-r1.md). Use the mock below as the visual reference for both forms.

## Scope

- Match the mock’s two-column layout, field order and footer. Present **Watcher Name**, **Repository**, **Engine**, **Run every**, and **Icon** in that order. Apply the existing System, Light, and Dark appearance preference to the window, forms, and icon popover.
- Require a nonblank name, a validated repository, an available engine, and a positive cadence. Default **Run every** to five minutes. Use **Cancel** and **Create Watcher** in the footer and show that new watchers start disabled. Generate the immutable `krr.<uuid>` label at creation and keep it in technical details.
- **Edit Watcher** uses the same layout with the current values and a **Save** action. Apply the [deactivation requirement](spec-007-r1.md). Preserve the label on save. Cancel returns to the list without applying changes.

- The **+** button opens **New Watcher** immediately.
- **Repository** accepts a pasted path, a dropped folder, or a recent repository. **Browse…** opens the native folder picker on demand. Resolve a selected Git subdirectory to its worktree root, display that root, and show the result of Kanban Rememory validation beside the field.
- Detect usable Codex and Claude Code CLI executables automatically. If both are available, offer both. If only one is available, select it and show the other as unavailable. If neither is available, disable creation and offer **Locate Executable…**. Offer the same action for an individual engine installed in a custom location.
- Resolve and store an absolute executable path suitable for launchd. Keep the path in technical details. Accept a manually located executable only after verifying it is usable.
- Keep the name, icon, engine, and cadence in the same form. Enable **Create Watcher** when the repository is valid and all required fields are complete.

- Keep icon selection optional and default to Folder. Use one button showing the selected symbol, its name, and a chevron. Open an anchored popover with a 6-by-2 grid of 12 symbols. Mark the current selection with a teal background and a checkmark. Selecting a symbol updates the button and dismisses the popover without moving the form fields.

- Use a compact, fixed-size Watchers window. Keep its logical dimensions within the proportions of the approved mockup. Do not use the exported image pixel dimensions as macOS window points.
- Present **New Watcher** and **Edit Watcher** over the Watchers window, within its bounds. Keep the underlying window at the same size and return to the watcher list when the form closes.

## Acceptance criteria

- Compare the full window, both forms and the icon popover against the mock in Light and Dark. Verify that the fields and footer fit without clipping and that the Watchers window cannot be resized. Open both creation and editing and verify that the form covers the watcher list without opening a separate window or expanding the original one. Verify that closing either form restores the list at the same size.

- Click **+** and verify the form opens without opening the system folder picker. Use a pasted Git subdirectory, a dropped folder, and a recent repository. Verify the displayed root and validation feedback. Verify **Browse…** opens the picker on demand.
- Exercise both engines installed, only one installed, and neither installed. Verify the available choices, default selection, and creation state. Locate a custom executable and verify that the resolved absolute path is saved.

- Open the icon picker from its single button. Verify that the grid opens without moving the form, the current selection is marked, and choosing another symbol updates the preview and closes the popover.

## Resources

- [Approved New Watcher mockup](../resources/active/krr-new-watcher-icon-picker.png) shows the standalone form with the icon picker open.
