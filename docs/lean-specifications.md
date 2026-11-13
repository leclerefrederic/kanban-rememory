# Lean Development Through Lean Specifications

*Build what earns its place. Write only the code needed to deliver it.*

## 1. Start with the outcome

State who needs to do what, where they get stuck today, and what should be possible after delivery. Describe a concrete situation and how to measure the improvement once delivered.

## 2. Every requirement earns its place

Name its benefit: experience, usability, performance, or protection (security, data integrity, accessibility, legal obligations). If the benefit is unclear, leave it out. Removal test: if removing it loses no value and no needed protection, remove it. A protective requirement must address an identified risk or obligation.

## 3. Specify the smallest complete experience

Cover the steps needed to reach the outcome, including recovery from relevant failures. Be precise about behavior, constraints, and decisions that affect the result. Approved mockups are part of the Specification; state which aspects are binding. Implementation details remain the developer's choice within the approved behavior and constraints, but never a license to add features, controls, steps, or messages. If the expected user-visible behavior remains unclear, record the question and pause the affected work until clarified. Continue work that does not depend on the answer.

## 4. Give each requirement a way to pass or fail

Write acceptance criteria around observable behavior: setup, action, expected result. Repeat a scenario only when the variation can change the result. Record what passed, failed, or remains untested.

## 5. Change scope only by agreement

Suggest improvements separately. Adding or changing behavior requires an approved Specification revision before implementation. A correction restores behavior already agreed. If it is unclear whether a proposed correction changes that behavior, clarify before implementing it. The approved baseline of an active Batch stays fixed. Link the Specification (intended behavior), test results (verified behavior), and debt records (unresolved defects), so each decision starts from evidence. Every observed defect is open debt until its correction is verified.

## 6. Build the simplest thing that meets the criteria

Reuse what works. Add abstractions, dependencies, and configuration only to solve an identified problem within approved scope. Simplicity never removes required protections or correctness. Stop when the agreed outcome is achieved and verified.

## The approval test

For every requirement:

- What value or protection does it provide?
- Who explicitly agreed to it?
- How will we verify it?

Then reread the Specification: **what can we remove without losing value?**
