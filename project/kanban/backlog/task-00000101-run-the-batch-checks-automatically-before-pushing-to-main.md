---
type: card
id: "TASK-00000101"
batch: null
specifications: []
---

# TASK-00000101 — Run the Batch checks automatically before pushing to main

- Owner: Development Agent
- Dependencies:

## Expected outcome

A Git `pre-push` hook shipped with the kit runs the existing Batch checks (`guard-batch-work.py publish`, and `verify-approval` when a Batch starts) so they no longer depend on the agent remembering to call them. It is LLM-independent: it protects the transitions (approval, acceptance, publication) for ChatGPT, Codex and Claude alike, including in the desktop apps. It does not cover work that bypasses Git. Follows the User's decision to protect transitions rather than sessions, in place of the push-guard item of [TASK-00000096](task-00000096-enforce-role-limits-with-hooks-for-each-llm.md).

## Acceptance criteria

- [ ] The User approves which pushes are checked and when a Batch counts as awaiting publication, so that the hook never blocks unrelated or standalone pushes.
- [ ] A push to `main` that would publish a Batch without a recorded acceptance of the exact revision is refused with an explicit message; a compliant push passes.
- [ ] The hook is versioned in the kit, installable with one documented command, and tested with a temporary repository.
- [ ] Installation is optional; the procedures still work without it.
- [ ] Adoption tests and board validation pass.

## Execution and evidence

- State:
- Actual start:
- Actual finish:
- Blocker:

## History
