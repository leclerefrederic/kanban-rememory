---
type: card
id: "CARD-00000144"
batch: null
specifications: []
---

# CARD-00000144 — Ignore local Graphify output

- Owner: KR Developer
- Dependencies:

## Expected outcome

Generated Graphify files stay local and no longer appear as untracked in Git.

## Scope and authorization

The User requested ignoring local Graphify files. Apply a repository-root rule for `graphify-out/` and preserve generated files.

## Acceptance criteria

- [x] A generated file under graphify-out/ is ignored by the repository.
- [x] Existing local Graphify files are preserved.


## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker: none
- Evidence: Reviewed scoped diff and ran `git diff --check`. `git check-ignore -v` identified the root rule on an existing generated file. The file remains on disk and no generated files are tracked. Board validation passes against the candidate in an isolated checkout. The two missing Runner links in the working tree predate this card.

## History

- 2026-11-15T13:02:33+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T13:02:57+01:00 — Stage moved from `development` to `completion`.
