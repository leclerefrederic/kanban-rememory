# Batch-013 — Independent acceptance

Candidate: `8552657d53415b10ee8272e15d85e82c007dc3e3`, attested by KR Developer on `origin/codex/batch-013`. KR Tester used the designated checkout and disposable fixtures with local-only origins. The results in [tests.md](../tests.md) are KR Tester observations. The User's delivery decision is separate.

## Targeted replay

Run from the designated candidate checkout. The existing test harnesses create disposable repositories.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-kanban-board.py \
  KanbanBoardTests.test_standard \
  KanbanBoardTests.test_scoped_creation_reserves_global_ids_and_preserves_history
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-module-delivery.py \
  ModuleDeliveryTests.test_activation_refuses_active_work_and_preserves_history \
  ModuleDeliveryTests.test_project_slot_is_independent_and_routes_work_notes \
  ModuleDeliveryTests.test_slot_holds_through_wait_rejection_and_resume \
  ModuleDeliveryTests.test_changed_combined_product_requires_new_acceptance_before_closure \
  ModuleDeliveryTests.test_interrupt_and_resume_accepted_and_rejected_publication
```

All seven selected tests passed. The installation walkthrough used the candidate's procedures for the initial simple-or-modular choice and the two CLI previews. The replay verified the common board path, historical lookup and preservation, concurrent ID allocation, scope capacity, exact-candidate guarding and resumption after interrupted publication. The Card publication fixture accepted the exact closing revision once, refused a premature milestone and a later unrelated revision, and left its module journal empty.

For SB-05 and SB-06, a separate run used the module delivery harness with two claimed Batches, and two operational Cards pinned to module A's in-progress Batch. A wrong owner was refused. The Batch owner moved the first Card, then was refused by Card WIP when moving the second. The Batch claim remained active. A resumption milestone referring to the Batch tests appeared only in A's journal. The fixture was removed.

## Reviewed evidence

- The [candidate technical record](pre-acceptance-verification.md) and local checkpoint cover the remaining board, role, notification and Git checks against the same revision.
- For SB-04, KR Tester compared SHA-256 digests of the candidate hook, board command and project resolver with the native fixture summary. All three matched. The Claude named-role probes recorded three allowed writes and three denied writes with file-byte checks. The four Codex probes and the unnamed Claude Orchestrator probe establish advisory scope. The explicit synthetic startup only demonstrates that configuration and does not establish native skill discovery, Desktop enforcement or settings protection.
- For SB-09, the fixture transcript identifies the blocked A Card, B's active Batch despite zero active B Cards, and each scope's latest exact published revision. It follows A's claim and one local note to the same resumption action. No replay against a live repository was necessary.
- SB-10 used a simulated Telegram transport. The checked cases differentiate project and module references and suppress repeats. The targeted real Git workflow used disposable origins for candidate and recovery checks.

No independent scenario requires a manual User action for this acceptance assessment. Overall delivery acceptance has no verdict in this record.
