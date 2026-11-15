---
type: batch
id: "Batch-011"
specifications: [{"id":"SPEC-017","revision":"1","path":"project/specs/approved/spec-017-r1.md"},{"id":"SPEC-018","revision":"1","path":"project/specs/approved/spec-018-r1.md"},{"id":"SPEC-019","revision":"1","path":"project/specs/approved/spec-019-r1.md"}]
status: closed
---

# Start as KR Orchestrator and clarify the four role handoffs

## Objective

Deliver default Orchestrator activation, the KR Orchestrator, KR Writer and KR Developer display names, Writer access to backlog Cards, and the new KR Tester role. Align dependent instructions, skills, launch paths, tests and optional hooks. Preserve existing technical identifiers where needed for compatibility. KR Developer retains Git operations.

## Execution constraints

- Run technical checks on the dedicated Batch branch. Before integrating the candidate onto main for UAT, KR Developer must create a backup tag at the exact current main commit, verify the tag on the authorized remote and record the candidate and backup refs. Stop before integration if the backup cannot be verified or main has changed since it was captured.
- The approved pre-UAT integration applies to this Batch only. Record the integrated candidate and leave the Batch awaiting the User verdict. If the candidate needs to be withdrawn, use the recorded backup and integration commits to prepare a revert without rewriting published history.
- Run exactly two acceptance journeys per host, one real Card workflow and one real Batch workflow. Open the normal project so the default role is discovered from the integrated main. Use isolated repositories or branches for disposable work with no fixture changes sent to the real origin/main.
