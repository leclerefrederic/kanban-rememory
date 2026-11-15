# MM-12 correction — Developer verification

The correction candidate is `b93b732d69ceb72ef96209d9c806e6058140cfbe`, verified at `origin/codex/batch-012`. Published main remains `d1c711b96637fc0845c41568c158a8ba78df7f87`. The previous candidate `1d70a04e39b39492bfac502045095cede7cc5317`, its verdicts and [failure reproduction](mm-12-stale-acceptance.md) remain available.

On the revised tools, a successful combined check does not authorize publication if the committed product differs from the candidate accepted by the User. The closure tool, pre-push check and optional module artifact guard enforce this comparison. Valid closing changes limited to control records or evidence preserve the decision. A stale decision releases global integration ownership and keeps the module's delivery slot. The next attempt uses current main and the decision for the updated candidate.

## Run the affected scenarios

Use the exact revision in `/private/tmp/kr-batch012-development` or a clean candidate checkout. The commands create isolated fixtures and local Git origins.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-module-delivery.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-module-publication.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-kanban-board.py
```

- **MM-12.** A passes technical checks on a changed combined product with only its earlier decision. Preparation and replay of a saved stale closure record fail before remote ref writes. A remains occupied while B acquires integration and publishes. A resumes against B's main, tests and records a new synthetic decision, then its records-only closing commit publishes. The older recovery evidence survives.
- **MM-11 and MM-13.** The suite verifies integration ownership, rejects a moved main without fresh verification, and resumes accepted and rejected publications through a real fixture pre-push hook. It preserves the unchanged-candidate closing path, the exact archive or tag, and exclusion of rejected product changes. Module ownership and capacity tests also pass.
- **Publication.** A standalone pre-push fixture refuses changes to product content, deletion and executable mode with an old decision, and permits a tracking-only commit or a new decision on the updated product. The direct module artifact guard refuses changed product with an otherwise identical frozen artifact.

Results: 7 module delivery, 6 publication/guard, 42 board tests passed. Board validation, skill synchronization, approved input snapshot and scoped diff checks passed. This is technical evidence for the independent Tester replay, not a new verdict or a User decision.
