# Lean Development Through Lean Specifications — Agent rules

Apply these rules in both Specification Agent and Development Agent roles, including during resumed work and corrections. They operationalize the six principles in the [shared manifesto](../guides/lean-specifications.md), which applies to the User and agents alike. The shared manifesto remains the authority; this document adds no independent scope or permissions.

Read the approved scope, existing decisions and applicable project instructions before acting. Reuse recorded authorization where it already covers the work. Keep proposals, authorized implementation, technical verification and User acceptance distinct.

## 1. Start with the outcome

Identify who needs to do what, the current difficulty, the intended improvement and how it will be checked. Use information already available in the request and project records. Ask only for missing decisions that affect the result.

Specification Agent records the outcome in the Specification. For standalone work, Development Agent records it on the Card. Do not substitute an implementation idea or a list of features for the expected outcome.

## 2. Every requirement earns its place

Name the value of each requirement: experience, usability, performance or necessary protection. For protective requirements, identify the risk or obligation they address. Leave unsupported additions out of the proposed scope.

Apply the removal test before proposing approval: could this be removed without losing value or necessary protection? If yes, remove it from the proposal. Once scope is approved, suggest any removal or addition separately and obtain agreement before changing behavior. This principle never authorizes silently dropping an agreed requirement.

## 3. Specify the smallest complete experience

Cover the steps needed to reach the outcome and recovery from relevant failures. State the behavior, constraints and binding mockup details that affect the result. Choose implementation details within those boundaries.

Do not invent features, controls, configuration, steps or messages because the Specification is silent. When user-visible behavior remains ambiguous, record the question, ask, and pause the affected work. Continue independent authorized work within the WIP limit. Do not treat silence or elapsed time as approval.

## 4. Give each requirement a way to pass or fail

Specification Agent defines observable scenarios with setup, action and expected result. Repeat a scenario only when the variation can change its outcome. Development Agent supplies the exact candidate revision, environment, startup instructions and technical evidence.

Record passed, failed, blocked and unexecuted cases accurately against their tested revision. Preserve earlier attempts. During User acceptance, follow the [guided test procedure](roles/specification-agent.md#preparing-and-guiding-acceptance-tests): startup instructions in each case, an OK / KO choice, and an explanation and screenshot request after KO. The agent maintains the records.

Do not turn a missing test into a pass or present technical checks as the User's acceptance decision.

## 5. Change scope only by agreement

Record approval before implementing added or changed behavior: on the Card for standalone work, or in an approved Specification revision for Batch work. Keep improvement suggestions separate. Existing approval still applies to the work it covers; do not repeatedly request it.

Keep an active Batch's approved baseline fixed. A correction restores the agreed behavior. If its classification is unclear, clarify before implementation. When a change is needed, propose the new revision and delivery plan without rewriting the active baseline.

Connect the intended behavior, test results and unresolved defects through the existing records. Every observed defect opens debt, including defects noticed during an OK test. Preserve required tests still due. The agent records the User's explicit delivery decision; it does not make that decision on the User's behalf.

## 6. Build the simplest thing that meets the criteria

Reuse what works. Introduce abstractions, dependencies and configuration only for an identified problem inside the approved scope. Preserve correctness and required protections.

Implement and verify the agreed outcome, then stop. Record unrelated improvements for consideration instead of absorbing them into the current task. Keep records concise enough to support execution and handoff.

## Apply the approval test

Before proposing scope, answer for every requirement:

- What value or protection does it provide?
- Who explicitly agreed to it? If approval is still pending, say so.
- How will we verify it?

Then review the Specification or standalone Card scope for anything removable without losing value. Present the proposal to the User when approval is needed. Before execution or resumption, verify that the authorization and approved scope cover the intended action.

These checks use the existing Specification, Card, tests and report sections. They do not require another approval document or new metadata fields.
