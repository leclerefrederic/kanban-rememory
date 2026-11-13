---
type: card
id: "TASK-00000067"
batch: null
specifications: []
---
# TASK-00000067 — Manage shared Specification resources

- Owner: Development Agent

## Expected outcome

Keep the resources agents need for implementation available at the approved revision.

## Acceptance criteria

- [x] Document `project/specs/resources/active/` for resources still in use and `project/specs/resources/archived/` for retained historical resources. Each Specification links to its resources and explains their purpose. Reuse existing repository files by linking to them directly.
- [x] Include referenced resource versions in the Git approval snapshot. Keep the association between each approved Specification revision and the exact files it used after archiving. Preserve approved Specification contents and make historical links resolvable through the approval commit.
- [x] Move a resource to Archived only when no current Specification needs it. Preserve the file and verify traceability with a resource shared by two Specifications, then archived after both stop using it.

## History

- 2026-11-13T21:42:37+01:00 — Stage moved from `backlog` to `development`.

- Verified a shared resource and two approved Specifications in an isolated Git repository. The archived file matched the historical snapshot for both. Eleven board tests passed.

- 2026-11-13T21:43:22+01:00 — Stage moved from `development` to `code-review`.

- 2026-11-13T21:43:23+01:00 — Stage moved from `code-review` to `completion`.
