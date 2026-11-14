# Run the scheduled Development Agent job

This is an agent procedure, not an executable scheduler or an installed recurring job. Closure and recovery have been exercised in isolated Git repositories. End-to-end scheduled dispatch, including correction and interrupted development, still needs implementation and verification. KRR currently invokes a read-only board summary and does not execute this procedure.

Use the configured repository and its designated Batch worktree. Follow the shared working instructions and Development Agent role. Apply the coordination and publication rules in the [Batch operations guide](../batches/start-and-close-batches.md).

1. Acquire the exclusive repository lock. If it is held, end this run without changing the repository. Keep the lock through selection and closure, and release an acquired lock on every exit, including errors and no-work results. A separate clone requires shared coordination.
2. Check for a published recovery ref or an interrupted local closure before selecting work. Verify the candidate closing commit, the tested revision, the User decision, and expected refs. Resume that closure using the recovery procedure. If the evidence conflicts, report the blocker and end the run.
3. Otherwise, look for a Batch with a recorded decision. Verify that the explicit User decision in the report agrees with the Description status and identifies the full tested commit in the tests record. Verify approval, remote reachability, and applicable acceptance checks. If any evidence is missing or inconsistent, leave the Batch in place, report the blocker, and end the run.
4. Close the decided Batch using the accepted merge or rejected archive procedure. Write closure evidence and verify remote publication before reporting success. Release the lock and end the run.
5. If an open Batch is awaiting acceptance or a decision, end the run. A recorded correction request or interrupted development requires the authorized Development Agent handoff in the Batch report; this closure procedure does not implement that dispatcher. When no closure or active Batch needs attention, use the approved pickup procedure for eligible ready work.

Before enabling any future recurring job, test its actual agent invocation, both decisions, interrupted closure, correction, and interrupted development in an isolated repository. Do not treat the presence of this document as evidence that the scheduler is active.
