# Kanban & Rememory

A Git-based workflow for tracking tasks, recording evidence, and handing work over between people or agents.

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Instructions for resuming, executing, and handing over work |
| [Kanban guide](kanban/README.md) | Workflow policies, columns, IDs, and transitions |
| [Software development profile](kanban/software-development.md) | Example delivery stages, engineering checks, and feedback loops |
| [Task template](kanban/task-template.md) | Outcome, scope, dependencies, and acceptance criteria |
| [Rememory guide](Rememory/README.md) | Record of decisions, verification, and next steps |
| [Daily log template](Rememory/daily-template.md) | Structure for a daily log entry |

## Adopt the kit

Copy `AGENTS.md`, the Kanban guide, template and empty columns, and the Rememory guide and template into the target repository. Merge the instructions into any existing `AGENTS.md`. Define the workflow, limits on work in progress, and selection rules in the Kanban guide. In the project instructions, specify the task prefix, journal time zone, and Git permissions. If several owners share the repository, specify where each keeps their journal.

Kanban shows the official task status. Rememory records decisions, what was verified, and where to resume. Git preserves the history of both.

This repository uses the kit to track its own changes. Its task cards and dated log record that work.
