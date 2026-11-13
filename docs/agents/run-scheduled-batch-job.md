# Run the scheduled Development Agent job

Use the configured repository and its designated Batch worktree. Follow the shared working instructions and Development Agent role. Apply the coordination and publication rules in the [Batch operations guide](../batches/start-and-close-batches.md).

1. Acquire the exclusive repository lock. If it is held, end this run without changing the repository. Keep the lock through selection and closure. A separate clone requires shared coordination.
2. Check for a published recovery ref or an interrupted local closure before selecting work. Verify the candidate closing commit, the tested revision, the User decision, and expected refs. Resume that closure using the recovery procedure. If the evidence conflicts, report the blocker and end the run.
3. Otherwise, look for a Batch with a recorded decision. Verify that the explicit User decision in the report agrees with the Description status and identifies the full tested commit in the tests record. Verify approval, remote reachability, and applicable acceptance checks. If any evidence is missing or inconsistent, leave the Batch in place, report the blocker, and end the run.
4. Close the decided Batch using the accepted merge or rejected archive procedure. Write closure evidence and verify remote publication before reporting success. Release the lock and end the run.
5. If an open Batch is awaiting a decision, end the run. When no closure or active Batch needs attention, use the approved pickup procedure for eligible ready work.

Configure the scheduler to invoke this procedure with the Development Agent. Test both decisions and an interrupted closure in an isolated repository before enabling the job against a live remote.
