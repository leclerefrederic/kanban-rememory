# Batch-013 technical delivery verification

Candidate `8552657d53415b10ee8272e15d85e82c007dc3e3` verified on `origin/codex/batch-013`. The worktree is `/private/tmp/kr-batch013-development`. Published main was `baa1b3d8cd6b7eae089fd1471cdcec9339058bad` at the same remote check.

The [local checkpoint](development-checkpoint.md) pins all 103 passing tool tests to the same code. The worktree remained clean. Approval snapshot verification, board validation, skills and diff checks passed again. The following checks closed the technical gaps listed in that checkpoint.

## SB-04 — native scope verification

Eight isolated CLI probes exercised all four roles in a synthetic A/B installation with one shared board and `KR_MODULE=a`. They used exact candidate tool bytes and synthetic records. The harness is in `/private/tmp/kr-sb04-native.6vih50/`, with commands, tool events, digests and a scrubbed `summary.txt` for review. Recreate the synthetic state before replaying `python3 run.py claude` and `python3 run.py codex`.

- Claude Code 2.1.323. The named Writer and Developer each edited their permitted A Card's body and were denied a B Card edit. The named Tester edited its A acceptance record and was denied an A Card edit. All six allowed/denied results were confirmed against file bytes. Unnamed Orchestrator scope remains advisory.
- Codex CLI 0.169.0. All four invocations identified the declared role and scope, read project/A context and ran `python3 -B agents/tools/manage-kanban-board.py show --scope a` in read-only sessions. Codex role scope remains advisory.
- The harness used the explicit synthetic startup and hook configuration. It does not establish new native skill discovery, Desktop enforcement or settings protection. Local board and hook tests retain the wrong-scope, ambiguous-command and cross-scope Batch-link checks.

## SB-09 — status and resumption

Reproduce from `PYTHONDONTWRITEBYTECODE=1 python3 /private/tmp/kr-batch013-sb09.z3no6u/reproduce.py`. It constructs an isolated A/B installation and local bare Git origin. The transcript is in the same fixture directory. The harness seeds publication summaries and verifies their revisions against the fixture origin.

- The shared board showed A's blocked work. The B view showed no active Card; B's in-progress Batch and recorded ownership established its occupied delivery slot.
- The global journal resolved the latest verified publication separately for A and B. A's older milestone stayed historical.
- The A filter, scoped status and one linked A note recovered the owner, branch, worktree and next action: wait for the contract fixture, then rerun export validation. B's local journal was unnecessary.

These technical observations are evidence for acceptance on the pinned revision. The independent Tester records scenario outcomes. User acceptance and integration remain separate.
