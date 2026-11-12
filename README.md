# Kanban & Rememory

A Git-based workflow for tracking tasks, recording evidence, and handing work over between people or agents.

| File | Purpose |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Entry point for agents and rules specific to this repository |
| [Kanban guide](docs/kanban.md) | Workflow policies, columns, IDs, and transitions |
| [Software development profile](docs/software-development.md) | Example delivery stages, engineering checks, and feedback loops |
| [Task card guide](docs/card-guide.md) | Required card content and the distinction between stage and state |
| [Board commands](tools/board.py) | Workflow setup, card creation, stage view, guarded moves, and validation |
| [Optional Lot workflow](docs/lot-workflow.md) | Fiche and Lot templates and stable ID mapping |
| [Card template](docs/lot-templates/Card.md) | Outcome, scope, dependencies, and acceptance criteria |
| [Rememory guide](Rememory/README.md) | Record of decisions, verification, and next steps |
| [Daily log template](Rememory/daily-template.md) | Structure for a daily log entry |

## Repository layout

Use the [project directory template](docs/lot-templates/Project-layout.md) for the base kit and the optional Lot module.

## Adopt the kit

Start in an existing Git repository or run `git init` in a new project. Use Python 3.9 or later and Git.

1. Copy these files from the kit into the target repository, preserving their paths.

   | Directory | Files |
   | --- | --- |
   | `agents/` | `adoption.md`, `working-instructions.md`, `actor-user.md`, `actor-specification-agent.md`, `actor-development-agent.md` |
   | `docs/` | `kanban.md`, `software-development.md`, `card-guide.md`
   | `docs/lot-templates/` | `Card.md`, `Project-layout.md` |
   | `tools/` | `board.py` |
   | `Rememory/` | `README.md`, `daily-template.md` |

   In the target repository's root `AGENTS.md`, create or merge this entry:

   ```markdown
   Read the [shared working instructions](agents/working-instructions.md) before adopting the kit or working on cards.
   ```

   Define the target project's ownership, journal conventions, and Git permissions in its own `AGENTS.md`. The kit repository's root instructions, board configuration, cards, and dated journal belong to this repository.

2. Follow the [guided adoption interview](agents/adoption.md) to select a template or agree on a custom workflow. From the target repository root, preview the result. This example uses the standard template.

   ```sh
   python3 tools/board.py init --template standard --wip-limit 1 --timezone Europe/Paris
   ```

3. After approval, apply the same configuration and verify the board.

   ```sh
   python3 tools/board.py init --template standard --wip-limit 1 --timezone Europe/Paris --apply
   python3 tools/board.py validate
   python3 tools/board.py show
   ```

   Check that the displayed stages and capacity match the approved workflow. Record the project's agreed transition and delivery rules and the adoption result as described in the [adoption guide](agents/adoption.md).

For the optional Lot module, also copy `docs/lot-workflow.md`, `docs/lot-operations.md`, `docs/lot-handoff.md`, `Fiche.md`, `Description.md`, `Tests.md`, and `Report.md` under `docs/lot-templates/`, and `tools/replay-lot-uat.py`.

Kanban shows the official task status. Rememory records decisions, what was verified, and where to resume. Git preserves the history of both.

This repository uses the kit to track its own changes. Its task cards and dated log record that work.
