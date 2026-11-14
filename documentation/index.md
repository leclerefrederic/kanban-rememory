# User guides

These guides explain how Kanban Rememory supports your project, what the records mean, and which decisions belong to you. Agents write and maintain those records. You can read them without learning the commands or document formats used to operate the framework.

Start with [Understand the framework](understand-the-framework.md) for the roles and connected records, and [Lean specifications](lean-specifications.md) for the shared principles.

## Choose what you want to do

| You want to… | Guide |
| --- | --- |
| Set up Kanban Rememory in a repository | [Start a project](start-a-project.md) |
| Give the agent work and agree on its priority | [Assign a task](assign-a-task.md) |
| Approve scope and follow a delivery | [Deliver a Batch](deliver-a-batch.md) |
| Try the candidate and decide on acceptance | [Test and accept a Batch](test-and-accept-a-batch.md) |
| Recover an interrupted session or handoff | [Resume work](resume-work.md) |
| Describe a problem and track its resolution | [Report a defect](report-a-defect.md) |
| Manage repository watchers on macOS | [Use Kanban Rememory Runner](use-kanban-rememory-runner.md) |

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
