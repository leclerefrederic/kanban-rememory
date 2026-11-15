---
type: card
id: "CARD-00000138"
batch: null
specifications: []
---
# CARD-00000138 — Shorten KR agent and skill names

- Owner: KR Developer
- Dependencies: none identified; reconcile with any existing agent-renaming work before execution.
- Approval to execute: User explicitly approved scope and start on 2026-11-15. Targeted priority ahead of the other backlog entries.

## Expected outcome

Make KR agents and their skills easy to identify and invoke with short, consistent names. The User clarified that renaming agents also means renaming skills, whose current names are too long.

## Scope

Use short names for the four role skills: `kr-orchestrator`, `kr-writer`, `kr-developer`, and `kr-tester`, aligned with the corresponding KR agent names. Update the relevant skill declarations, installed names, role references, installation/synchronization mappings, and current instructions so the renamed entries remain discoverable and usable. Preserve role responsibilities and permissions. Historical delivery records remain historical.

This is future work in the main Kanban Rememory repository, independent of the disposable batch-status.txt acceptance fixture and its Batch-001.

## Acceptance criteria

- [x] The four role skills are exposed under `kr-orchestrator`, `kr-writer`, `kr-developer`, and `kr-tester`.
- [x] Agent names and current instructions consistently identify the corresponding Orchestrator, Writer, Developer, and Tester roles.
- [x] Installation/synchronization and role handoffs resolve the renamed skills; verify with applicable checks and a discovery/handoff smoke check.
- [x] Role permissions and responsibilities remain unchanged, verified by diff review and applicable role checks.

## Execution and evidence

- State: Verified.
- Actual finish: 2026-11-15.
- 33 board and 22 Telegram checks passed, including role checks and retirement of unchanged legacy skills while preserving a customized copy. Board validation, skill synchronization and diff checks passed.
- Codex CLI 0.169.0 and Claude Code 2.1.323 both discovered all four short skills and successfully delegated a read-only KR Developer role probe in an isolated repository. The retained Claude Code `development-agent` ID loaded `kr-developer`.
- Compared all twelve canonical and installed skill copies with their earlier contents. Only the names changed. Role limits, hook logic and technical launch IDs remain unchanged.
- Flow reviewed before closure. No blocker remains. Remy review was not picked up.

## History

- 2026-11-15T01:39:30+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T01:43:05+01:00 — Stage moved from `development` to `completion`.
