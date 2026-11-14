---
type: card
id: "CARD-00000133"
batch: null
specifications: []
---

# CARD-00000133 — Migrate Kanban identifiers to CARD

- Owner: Development Agent
- Priority: targeted executive decision from the User on 2026-11-15 (Europe/Paris).

## Expected outcome

Cards use CARD identifiers and matching lowercase filenames. The migration updates existing links, Rememory journals, historical references, tools, templates and documentation. Preserve numbers, evidence and decisions.

## Acceptance criteria

- [x] Canonical CARD identifiers and filenames are consistent across the board, journal, references and documentation.
- [x] New cards use the CARD prefix and continue existing numbering, including projects upgrading from the previous prefix.
- [x] Repository review, link validation, skill synchronization and applicable tests pass.

## Execution and evidence

- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Reviewed all 132 existing cards against their original bytes after applying only the identifier and reference substitutions. Reviewed remaining legacy matches and retained compatibility and Git history lookups.
- Board validation, skills synchronization, whitespace checks, 32 board tests and 22 Telegram setup tests passed. The next Card preview resolves to CARD-00000134.
- Flow reviewed before closure. This was the only active Card and no blocker remains.

## History

- 2026-11-15T00:09:56+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T00:11:50+01:00 — Stage moved from `development` to `completion`.
