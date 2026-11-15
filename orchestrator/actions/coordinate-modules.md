# Coordinate a module delivery

The [Card delivery](deliver-card.md) sequence lists the commands. This file covers ownership, check isolation and recovery. Coordinate only in worktrees of a single clone.

## Ownership

`claim` records the module, owner, branch, worktree and base. `add-card` joins further Cards of the module to the claimed phase; `publish-card`, `milestone --published` and `finish` then require all of them in `completion` with verified criteria. Each module holds one delivery; one integration runs at a time across the project. `status` shows the current claim. An interrupted session resumes with the same owner and worktree after confirming the previous session has stopped. Never clear a lock only because it is old.

`integration begin` records the local `main` tip. Do not overwrite intervening remote work. If `main` advances, release integration, rebuild the combined revision on the new `main` and verify it again. Approval covers one exact candidate.

## Verify the combined revision

Create an integration worktree at the expected `main` tip and assemble the combined revision there; never move `main` to a tentative result. Run all required checks as one command against that clean checkout:

```sh
python3 orchestrator/tools/manage-module-delivery.py --scope MODULE run-check DELIVERY --owner OWNER --integration-checkout PATH -- CHECK_COMMAND
```

Each run gets its own temporary directory. Use `KR_RUNTIME_DIR` for test databases and `KR_ARTIFACT_DIR` for builds. Give network fixtures dynamic loopback ports and independent data; run checks that need a fixed shared resource in sequence. A failed or interrupted run, or a changed checkout, invalidates earlier verification. `publish-card` accepts only the revision verified last.

## Recover

- **Publication interrupted:** rerun `publish-card` with the same closing commit. It recognizes a closing commit already on remote `main` and refuses a different one.
- **Journal missing:** `milestone ... --published` is keyed by delivery and revision and can be rerun after the push.
- **Capacity still held:** `finish` refuses until integration is released and the closing revision is on published `main`.

After `finish`, delete the delivery branch and worktrees only when they point to verified, published commits.
