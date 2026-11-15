---
type: card
id: "CARD-00000140"
batch: null
specifications: []
---

# CARD-00000140 — Parallelize independent work within an approved assignment

- Owner: KR Developer
- Dependencies: current KR orchestration and role instructions.
- Approval and priority: the User explicitly approved starting this Card ahead of other backlog work on 2026-11-15.

## Expected outcome

KR Orchestrator reduces the time the user waits for a Card or Batch by overlapping useful work that has independent inputs. The user approves the scope once and receives one coordinated result. The project's existing work-in-progress limit and publication rules still apply.

## Scope

- At handoff, KR Orchestrator identifies which work can start immediately, which work depends on a specific output, and who owns the result. Start useful independent work concurrently when the host supports the authorized delegation and the expected savings justify the coordination. Keep small or tightly coupled changes on a single path.
- One KR Developer owns the implementation, Card execution records, integration and Git publication. Helpers may inventory references, review an agreed snapshot or prepare and run checks within their assigned role and permissions. Give each helper a clear input, target revision or fixture, expected output, and write boundary. Use isolated scratch environments for checks that write files or could interfere with each other.
- Start checks that need the finished change only when their inputs are ready. Independent checks against the same candidate may run concurrently. Review the results together, report failures, and rerun any check invalidated by a change to the candidate. Only then proceed through the existing delivery and approval rules.
- If a workstream is blocked, continue independent authorized work. Surface the decision or missing prerequisite when it affects delivery. If the host cannot delegate or parallel execution would add more time than it saves, use the existing single-agent workflow.
- Keep this within one approved assignment and its existing work-in-progress policy. No parallel pickup of separate Cards, new permanent role, or permission change.

## Acceptance criteria

- [x] In a scratch Card that renames a skill, give KR Developer the implementation and start a reference inventory or test preparation with independent inputs. Evidence shows meaningful overlap before the candidate is ready. The Card has one owner and is picked up once.
- [x] Use a candidate with independent Codex and Claude Code checks. Run both against the same revision with isolated writable fixtures. Confirm that delivery waits for both required results. Change the candidate and confirm that any invalidated result is rerun.
- [x] Block one dependent step while independent work is available. Verify that the independent work continues, and that the owner reports the blocker and includes all outstanding checks in the delivery decision.
- [x] Exercise a trivial Card and a host without available delegation. Verify that the single-agent path completes under the same approval, verification and publication rules.
- [x] For the parallel scenario, record the start and finish of the overlapping work and compare elapsed time with the same steps run sequentially under comparable conditions. Report the observed savings or the overhead. Do not use a fixed time threshold across hosts.

## Resources

- [SPEC-016 revision 1](../../specs/approved/spec-016-r1.md) defines the orchestration and approval workflow.
- [Orchestration procedure](../../../agents/orchestrate-work.md) defines the current handoff.

## Execution and evidence

- State: Verified.
- Actual finish: 2026-11-15.
- In a controlled scratch rename, one KR Developer took the Card once. An independent baseline reference inventory and board verification overlapped the rename by 0.371 s. For the same work on equivalent scratch copies, including dispatch and join, elapsed time was 1.991 s in series and 1.700 s concurrently. Fixture resets were excluded equally. This is one local observation, not a general speedup guarantee.
- Timing in Europe/Paris: serial 01:57:31.284–01:57:33.275. Concurrent owner 01:57:33.439–01:57:33.810, inventory 01:57:33.439–01:57:35.138, full concurrent interval 01:57:33.438–01:57:35.138.
- Two native read-only CLI probes ran concurrently in distinct writable clones for fixture candidate `d0e5cc5ef76c5e99364a630315c29feefa5cd0be`, then for changed candidate `75c70027bb1e9463e8906d2d23eec3ec4564686d` (15.06 s and 14.18 s overlap). The test harness held delivery until both results for each revision and rejected the earlier results after the checked skill changed. Native Codex and Claude confirmed the candidate gating, rerun and fallback instructions. The harness coordinated the CLI processes; it does not establish automatic host scheduling.
- A blocked prerequisite left independent Kanban validation runnable while delivery remained blocked. Two direct single-agent fixtures (trivial work and unavailable delegation) each went from approval through board checks and closure to publication on their own local-only Git remote.
- 34 board tests, 22 Telegram tests, board validation, skill synchronization and diff checks passed. Reviewed the scope and flow before closure. No blocker remains.

## History

- 2026-11-15 — Reclassified the draft SPEC-021 as this backlog Card at the User’s request. Development was subsequently authorized by the User.

- 2026-11-15T01:55:22+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T02:01:11+01:00 — Stage moved from `development` to `completion`.
