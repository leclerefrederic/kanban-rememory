---
type: batch
id: "Batch-013"
specifications: [{"id":"SPEC-021","revision":"2","path":"project/specs/approved/spec-021-r2.md"}]
status: closed
---

# Use one Kanban for the project

## Objective

Deliver SPEC-021 revision 2. Simple and multi-module installations use the same project board and global journal. Module scope governs the Cards, filtered views, delivery ownership and optional module records.

## Execution constraints

- Mission order: common board layout and installation, scoped Card operations and permissions, delivery capacity and integration, journal routing and publication milestones, regression checks and candidate delivery. Delegate independent tasks under one owning Developer.
- Develop on `codex/batch-013` in a dedicated worktree. Check SB-01 through SB-10 using disposable fixtures and local test remotes. Record actual native enforcement separately from advisory scope.
- Keep CARD-150 and the live repository's migration separate. Deliver the exact candidate for independent acceptance before integration into main.
