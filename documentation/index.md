# Guides for project owners

These guides explain how Kanban Rememory supports your project, what the records mean, and which decisions belong to you. Agents write and maintain those records. You can read them without learning the commands or document formats used to operate the framework.

## A useful reading order

1. [Understand the framework](understand-the-framework.md): the roles, the pieces, and how they connect.
2. [Lean specifications](lean-specifications.md): the principles behind scope and implementation decisions.
3. [Start a project](start-a-project.md): what to agree with your agent before work begins.
4. [Deliver a change](deliver-a-change.md): how a request becomes a delivery, including interruptions and rejection.
5. [Acceptance and debt](acceptance-and-debt.md): how tests work, what failures mean, and what remains after a delivery.
6. [Use the macOS companion](runner.md): what Runner does today and how watchers fit into the picture.

The principles are shared by people and agents. These guides explain their meaning for you; the separate agent instructions define how to execute them. A guide does not grant an agent permission to change scope, accept a delivery, or publish code.

## A complete example

Follow one fictional delivery: preserve customer names in a booking CSV export. These five filled records show the agreed scope, implementation work, a failed test, its correction and accepted closure. They are reading examples, not live project records or claims that this demo application exists. Agents write all of them; the User supplies decisions and test verdicts.

| Read | What it demonstrates |
| --- | --- |
| [Specification](examples/project-specification.md) | The outcome, lean scope and two observable acceptance criteria. |
| [Batch description](examples/batch-description.md) | The selected approved revision and agreed delivery point. |
| [Card](examples/kanban-card.md) | An independently tracked implementation task pointing to the Specification and Batch. |
| [Tests](examples/batch-tests.md) | Startup instructions, actions, verdicts and results retained for each tested revision. |
| [Report](examples/batch-report.md) | Approval, debt, correction, the User's decision and publication evidence. |

The example Card points to the Batch; the Batch records contain no Card references. Tests and Report belong to the Batch. The Specification describes the intended outcome; the final test results and report show whether the delivery achieved it.
