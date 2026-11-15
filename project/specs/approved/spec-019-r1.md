---
type: specification
id: "SPEC-019"
revision: "1"
---
# Give KR Tester ownership of user acceptance testing

## Expected outcome

After a Batch has been delivered, KR Orchestrator hands its exact candidate to KR Tester. KR Tester prepares and runs the acceptance scenarios it can execute, guides the user through scenarios that require human action or judgment, and returns the evidence in the original chat. KR Writer can focus on defining the expected behavior and its acceptance criteria.

## Scope

- Define KR Tester as a distinct role in `agents/roles/tester.md`. Document how Codex and Claude Code sessions invoke it and how KR Orchestrator hands off and receives the result.
- KR Writer defines the acceptance criteria as part of writing the Specification. KR Developer runs the technical checks, supplies the exact delivered revision and reproducible startup instructions, and implements authorized fixes. KR Tester takes over guided acceptance and maintenance of its test results and evidence. Align the affected role and workflow instructions so each responsibility has one owner.
- At handoff, identify the approved scope, delivered revision, test environment, required scenarios and existing results. KR Tester checks that the evidence and scenario refer to the same revision. It reports a missing candidate or prerequisite and continues independent scenarios where possible.
- KR Tester executes eligible acceptance checks in a test environment and records observations against the exact candidate. For checks requiring the user, it provides one actionable scenario at a time, with startup steps, expected result and an OK or KO question. It records the user's answer and advances to the next applicable case. Distinguish agent-executed evidence, user verdicts, blocked cases and cases not run.
- KR Tester records discrepancies and routes them to the Orchestrator with reproduction steps and affected cases. It can use scratch fixtures and maintain acceptance records within its role. It does not change product code, approve scope, authorize publication, or close a Batch. The Orchestrator surfaces the evidence and records or routes the user's explicit delivery decision under the applicable Batch rules.
- This role applies to Batch acceptance and to standalone work only when the project calls for separate user acceptance. Ordinary technical checks on a standalone Card remain with KR Developer. If the optional role hook is updated, make its actual coverage explicit and preserve existing role limits.

## Acceptance criteria

Cover these checks within the two real workflows per host and the required technical checks. Do not add separate user acceptance scenarios for individual assertions.

1. From a delivered candidate, the Orchestrator invokes KR Tester with the exact revision and required scenarios. KR Tester reports a revision mismatch without assigning that evidence to the candidate.
2. KR Tester runs one eligible scenario and guides one human scenario. It records each with its evidence, source and revision. When the user gives OK or KO, it advances without a separate request to continue.
3. On a KO or missing prerequisite, KR Tester records the failing or blocked case and continues an independent eligible case. The Orchestrator receives enough evidence to route correction to KR Developer.
4. When the required scenarios are resolved, KR Tester returns the results and any gaps. The user is asked for the delivery decision. No Batch is accepted, merged or published based solely on a Tester report.
5. Verify that KR Writer still defines acceptance criteria and that KR Developer still owns technical checks and fixes. Test the documented handoff in both supported hosts.

## Resources

- [SPEC-016 revision 1](../approved/spec-016-r1.md) defines the Orchestrator workflow.
- [SPEC-018 revision 1](spec-018-r1.md) defines the proposed KR Writer and KR Developer roles. KR Writer owns the criteria, and KR Tester owns guided acceptance.
- [Batch workflow](../../../agents/batches/batch-workflow.md) defines the acceptance and closure gates.
