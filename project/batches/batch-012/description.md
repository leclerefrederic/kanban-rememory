---
type: batch
id: "Batch-012"
specifications: [{"id":"SPEC-021","revision":"1","path":"project/specs/approved/spec-021-r1.md"}]
status: closed
---

# Independent modules in one shared repository

## Objective

Deliver SPEC-021 revision 1 in full, with separate module tracking and shared sources in one repository. Preserve single-project operation.

## Execution constraints

- Mission order: manifest, setup and module context; scoped tool and role operations; worktree coordination, journals and integration/recovery; module-qualified notifications; end-to-end regression and delivery. Parallelize independent tasks under one owning Developer.
- Develop on `codex/batch-012` in a dedicated worktree. Run all MM-01 through MM-15 checks or record gaps against the exact candidate. Use isolated fixtures and local test remotes. Keep the live repository in single-project mode.
- Deliver the candidate for separate Tester acceptance. The standard Batch acceptance and closure rules apply before main publication.
