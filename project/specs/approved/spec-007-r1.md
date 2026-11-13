---
type: specification
id: "SPEC-007"
revision: "1"
---
# Require deactivation before editing a KRR watcher

## Expected outcome

Users can edit a KRR-managed watcher only after it is fully deactivated.

Use the [shared Edit Watcher form](spec-008-r1.md). The restriction applies regardless of where the edit action is exposed.

## Acceptance criteria

- An activated watcher cannot be edited, whether idle or running. This applies to every editable field, including the display name, repository, engine, cadence, and icon. Explain in the interface that the watcher must be deactivated before editing.
- Editing remains unavailable while deactivation is pending. Once deactivation completes, editing is available again for watchers managed by KRR.
- Recheck the watcher state when saving. If it became activated after the editor opened, reject the save and preserve the existing configuration.
