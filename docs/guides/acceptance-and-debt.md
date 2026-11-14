# Acceptance and debt

Acceptance checks whether the delivered result meets the approved behavior. The agent runs technical checks before delivery and then supports your review of the actual candidate. Your verdict is recorded as evidence, with the revision you tested.

## What happens for each test

Every case begins with instructions: which build to open, how to start it, any connection or session to prepare, and the test data needed. The agent then explains the actions, expected result and stopping point.

Those instructions remain available with the OK / KO choice. After your verdict is recorded, the agent presents the next case without asking for separate permission to continue. You can pause the session at any time.

For KO, the agent asks what happened, collects the exact message or observed behavior, and requests a screenshot. The screenshot is attached to the Batch and linked to the failed case. If it is unavailable, the agent records that fact. You supply the observation; the agent maintains the files.

## A verdict and a defect answer different questions

A test verdict says whether the behavior being checked passed. A defect records something wrong that was observed. A case can pass while revealing a separate visual defect; if the visual behavior was itself the expected result, its failure makes that case KO.

Every observed defect creates open debt. Its record includes severity, affected behavior, related tests and whether it blocks acceptance. Recording a defect does not resolve it.

| Severity | Meaning |
| --- | --- |
| S0 — Critical | The system is unusable. |
| S1 — Major | An essential workflow cannot be completed with an acceptable workaround. |
| S2 — Moderate | The work can be completed in degraded conditions. |
| S3 — Minor | A smaller defect affects presentation or comfort of use. |

Severity describes impact. The test record separately identifies which cases are blocked. The agent continues independent cases where possible; blocked or unexecuted cases remain explicitly outstanding.

## When correction is required

A blocking defect prevents acceptance. The request for correction identifies what was expected, what happened, the affected tests and the candidate involved. Development Agent corrects the agreed behavior in the same open Batch after authorization.

The previous candidate and its results remain available. The new candidate has its own revision and evidence. Acceptance resumes with the failing and affected scenarios, then the tests that the defect had blocked. Fixing the blocker does not automatically pass those tests: they must actually run.

If the proposed correction changes the agreed behavior, the agents bring that decision back to you. They cannot quietly expand the active Batch's scope.

## What can remain after acceptance

A delivery can be accepted with explicitly deferred nonblocking debt once all required scenarios pass and no blocking debt remains. The report identifies what was deferred and your decision. “Accepted” does not erase those defects.

If you reject the delivery, its report preserves both defects and tests still owed. Before proposing a successor, the agent reviews the relevant earlier records and carries forward those obligations.

A defect keeps its original reference across deliveries. A later report records the verified correction and the accepted delivery that includes it. The closed original report remains unchanged. A rejected successor does not resolve debt in the published baseline.

Return to [the delivery process](deliver-a-change.md) or the [guide index](index.md).
