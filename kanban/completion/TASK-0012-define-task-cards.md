# TASK-0012 — Define software workflow stages and task cards

- Owner: Kanban Rememory maintainers
- Dependencies: TASK-0011

## Expected outcome

Make it clear what a card represents, what belongs on it, and how to track it from intake to delivery.

## Scope

A card represents one executable task with an observable outcome. It can track a feature slice, a bug fix, a test, a migration, or operational work. A requirement or design can be linked as context.

Define the required card content: stable ID, action title, owner or responsible team, expected outcome, scope, dependencies, and checkable acceptance criteria. Describe which fields become required at start, when blocked, and at closure. Include actual dates, the blocker and next action when applicable, and links to the PR, revision, checks, delivery evidence, or Rememory entry.

Keep detailed specifications, discussion, investigation logs, and large artifacts in their source documents. Keep secrets and personal data out of cards.

## Acceptance criteria

- [x] The guide and template distinguish the stage folder from an optional state within that stage: waiting, in progress, or blocked.
- [x] The short, standard, and long templates use recognizable software stage names and show when a separate review, testing, or deployment stage adds value.
- [x] A worked example follows a task from intake through code review, rework, and closure. It shows both a merge-only finish and a finish that requires verified deployment.
- [x] The template and guide identify required and conditional fields and explain what belongs in linked material.
- [x] The board remains coherent with the configured stage folders, and repository validation passes.
