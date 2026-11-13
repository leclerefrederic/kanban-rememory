# Kanban & Rememory

A Git-based workflow for tracking tasks, recording evidence, and handing work over between people or agents.

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Entry point for agents and rules specific to this repository |
| [Kanban guide](docs/kanban.md) | Workflow policies, columns, IDs, and transitions |
| [Software development profile](docs/software-development.md) | Example delivery stages, engineering checks, and feedback loops |
| [Task card guide](docs/card-guide.md) | Required card content and the distinction between stage and state |
| [Board commands](tools/manage-kanban-board.py) | Workflow setup, card creation, stage view, guarded moves, and validation |
| [Optional Batch workflow](docs/batch-workflow.md) | Specification and Batch templates and stable ID mapping |
| [Card template](docs/templates/card.md) | Outcome, scope, dependencies, and acceptance criteria |
| [Rememory guide](project/rememory/README.md) | Record of decisions, verification, and next steps |
| [Daily log template](project/rememory/daily-template.md) | Structure for a daily log entry |

## Repository layout

Use the [project directory template](docs/templates/project-layout.md) for the base kit and the optional Batch module.

## Adopt the kit

Start in an existing Git repository or run `git init` in a new project. Use Python 3.9 or later and Git.

1. Copy these files from the kit into the target repository, preserving their paths.

   | Directory | Files |
   | --- | --- |
   | `docs/agents/` | `adoption.md`, `working-instructions.md`, `actor-user.md`, `actor-specification-agent.md`, `actor-development-agent.md` |
   | `docs/` | `kanban.md`, `software-development.md`, `card-guide.md`
   | `docs/templates/` | `card.md`, `Project-layout.md` |
   | `tools/` | `manage-kanban-board.py` and the `kanban/` package |
   | `project/rememory/` | `README.md`, `daily-template.md` |

   In the target repository's root `AGENTS.md`, create or merge this entry:

   ```markdown
   Read the [shared working instructions](docs/agents/working-instructions.md) before adopting the kit or working on cards.
   ```

   Define the target project's ownership, journal conventions, and Git permissions in its own `AGENTS.md`. The kit repository's root instructions, board configuration, cards, and dated journal belong to this repository.

2. Follow the [guided adoption interview](docs/agents/adoption.md) to select a template or agree on a custom workflow. From the target repository root, preview the result. This example uses the standard template.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris
   ```

3. After approval, apply the same configuration and verify the board.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris --apply
   python3 tools/manage-kanban-board.py validate
   python3 tools/manage-kanban-board.py show
   ```

   Check that the displayed stages and capacity match the approved workflow. Record the project's agreed transition and delivery rules and the adoption result as described in the [adoption guide](docs/agents/adoption.md).

For the optional Batch module, also copy `docs/batch-workflow.md`, `docs/batch-operations.md`, `docs/batch-handoff.md`, `specification.md`, `description.md`, `tests.md`, and `report.md` under `docs/templates/`.

Kanban shows the official task status. Rememory records decisions, what was verified, and where to resume. Git preserves the history of both.

This repository uses the kit to track its own changes. Its task cards and dated log record that work.
