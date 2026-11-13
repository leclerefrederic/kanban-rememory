# Getting started

Start in an existing Git repository or run `git init` in a new project. Use Python 3.9 or later and Git.

1. Copy these files from the kit into the target repository, preserving their paths.

   | Directory | Files |
   | --- | --- |
   | `docs/agents/` | `adoption.md`, `working-instructions.md`, `actor-user.md`, `actor-specification-agent.md`, `actor-development-agent.md` |
   | `docs/` | `kanban.md`, `software-development.md`, `card-guide.md` |
   | `docs/templates/` | `card.md`, `project-layout.md` |
   | `tools/` | `manage-kanban-board.py` and the `kanban/` package |
   | `project/rememory/` | `README.md`, `daily-template.md` |

   In the target repository's root `AGENTS.md`, create or merge this entry:

   ```markdown
   Read the [shared working instructions](docs/agents/working-instructions.md) before adopting the kit or working on cards.
   ```

   Define the target project's ownership, journal conventions, and Git permissions in its own `AGENTS.md`. The kit repository's root instructions, board configuration, cards, and dated journal belong to this repository.

2. Follow the [guided adoption interview](agents/adoption.md) to select a template or agree on a custom workflow. From the target repository root, preview the result. This example uses the standard template.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris
   ```

3. After approval, apply the same configuration and verify the board.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris --apply
   python3 tools/manage-kanban-board.py validate
   python3 tools/manage-kanban-board.py show
   ```

   Check that the displayed stages and capacity match the approved workflow. Record the project's agreed transition and delivery rules and the adoption result as described in the [adoption guide](agents/adoption.md).

For the optional Batch module, also copy `docs/batch-workflow.md`, `docs/batch-operations.md`, `docs/batch-handoff.md`, `specification.md`, `description.md`, `tests.md`, and `report.md` under `docs/templates/`.

See the [project directory template](templates/project-layout.md) for the installed layout.
