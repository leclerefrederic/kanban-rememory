# Batch-013 development checkpoint

Local product revision `8552657d53415b10ee8272e15d85e82c007dc3e3` in the dedicated worktree. The live repository has its existing single-project layout.

Reviewed the scoped diff in Development. Ran the five tool suites in disposable repositories, including local bare Git origins and a simulated Telegram sender:

| Suite | Passed |
| --- | ---: |
| `test-kanban-board.py` | 44 |
| `test-module-delivery.py` | 9 |
| `test-module-publication.py` | 6 |
| `test-role-migration.py` | 21 |
| `test-telegram-setup.py` | 23 |

Board validation, the approved snapshot, Python 3.9 syntax, skill synchronization and whitespace checks also passed.

- SB-01/02: fixture setup keeps a single project workflow and module journals, rejects unfinished work on older layouts and reads preserved historical Cards.
- SB-03/05: concurrent creation uses unique project IDs. Scope filters, scoped leasing, explicit project capacity and Batch claims were exercised.
- SB-04: local role hook payload tests cover declared scopes, allowed/denied actions and protected Card headers. Native Codex/Claude sessions on this revision still need independent verification.
- SB-06/07/08: local and project work notes route by scope. Scoped publication writes only after verified close, retries on the exact revision remain idempotent, and concurrent events survive. The Card scenario retries after a later unrelated publish and refuses the wrong revision.
- SB-09: the procedures derive status from the common board, active Batches and latest scope milestone. The full guided status and resumption check is for acceptance.
- SB-10: simulated alerts distinguish scoped and project events. Real local Git fixtures cover changed combined product, acceptance checks and publication replay. No Telegram request was sent during testing.

These are Developer checks. The Tester records verdicts for the delivered candidate.
