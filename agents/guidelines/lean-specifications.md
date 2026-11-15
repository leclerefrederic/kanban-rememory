# Apply the lean principles

The [shared manifesto](../../documentation/lean-specifications.md) is the authority for the six principles. This operational view adds no scope or permission. Load the manifesto when interpreting or changing a principle; routine work uses this view and the applicable role/action. Approved requirements and binding mockup details remain binding.

## 1. Start with the outcome

Identify who needs to do what, the present difficulty, improvement and observable check. Reuse the request and recorded decisions. Writer records the outcome in the Specification; Developer uses the Card for standalone work. Ask only for missing decisions that affect the result.
## 2. Every requirement earns its place

Name its experience, usability, performance or necessary protection value. For protection, identify the risk/obligation. Before approval, remove unsupported scope. After approval, propose additions/removals separately and obtain agreement; never silently drop requirements.
## 3. Specify the smallest complete experience

Cover the steps and relevant failure recovery needed for the outcome. State behavior, constraints and binding mockup details; choose implementation within them. Do not invent features because a Specification is silent. Record ambiguous user-visible behavior, ask, and pause only dependent work within WIP. Silence and elapsed time are not approval.
## 4. Give each requirement a way to pass or fail

Writer supplies setup/action/expected-result scenarios. Developer supplies the exact candidate, environment, startup and technical evidence. Tester owns [acceptance execution](../roles/tester.md#run-and-guide-acceptance). Preserve passed, failed, blocked and unexecuted results against their revisions; technical tests are not User acceptance.
## 5. Change scope only by agreement

Record approval before changed behavior: on the standalone Card or in a new approved Specification revision. Reuse existing authority for a correction restoring agreed behavior; clarify uncertain classification. Keep an active Batch baseline fixed. Link intended behavior, tests and debt; every observed defect opens debt, including during OK tests. Only the User decides delivery acceptance.
## 6. Build the simplest thing that meets the criteria

Reuse working components. Add abstractions/dependencies/configuration only for a problem inside approved scope. Preserve protections and correctness. Once the agreed outcome is verified, stop; record unrelated suggestions separately.

## Apply the approval test

For each requirement: what value/protection does it provide, who agreed (or is approval pending), and how can it pass/fail? Then ask what can be removed without losing value or protection. Use the existing Specification/Card and test/report sections, not new approval metadata. Verify scope and execution authorization again when resuming.
