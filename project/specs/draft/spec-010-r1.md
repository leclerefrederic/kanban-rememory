---
type: specification
id: "SPEC-010"
revision: "1"
---

# Recover from an unavailable watcher engine

## Expected outcome

KRR remains usable when an existing watcher's CLI disappears or loses authentication. The affected watcher remains visible and explains what the user can do to recover it.

## Scope

- When the configured executable is missing or cannot be executed, show an actionable engine-unavailable state for that watcher. Prevent activation and manual runs while the executable is unavailable. Keep deactivation and management available under the existing ownership and edit rules.
- When a run provides reliable evidence that interactive authentication is required, show a sign-in-required state and tell the user to sign in with the affected CLI. Preserve a generic failure for ambiguous errors.
- Restore manual run eligibility when the executable returns. After signing in, the user can retry and a successful run clears the authentication error.

## Acceptance criteria

- Remove the executable used by an isolated watcher. Verify KRR remains responsive, shows the affected watcher and its recovery instructions, and prevents activation or manual runs as applicable.
- Restore the executable. Verify an eligible watcher can run again.
- Simulate a recognized authentication failure and a generic failure. Verify the messages distinguish them, then verify that a successful retry clears the authentication error.
- Verify an unaffected watcher remains usable throughout.
