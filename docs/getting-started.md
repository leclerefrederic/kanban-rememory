# Getting started

Start in an existing Git repository or run `git init` in a new project. Use Python 3.9 or later and Git.

1. Copy these files from the kit into the target repository, preserving their paths.

   | Directory | Files |
   | --- | --- |
   | `docs/agents/` | `configure-a-project.md`, `work-in-a-project.md` |
   | `docs/agents/roles/` | All three role files |
   | `docs/kanban/` | All three guides |
   | `docs/templates/` | `kanban-card.md`, `project-layout.md` |
   | `tools/` | `manage-kanban-board.py` and the `kanban/` package |
   | `project/rememory/` | `README.md`, `daily-template.md` |

   In the target repository's root `AGENTS.md`, create or merge this entry:

   ```markdown
   Read the [shared working instructions](docs/agents/work-in-a-project.md) before adopting the kit or working on cards.
   ```

   Define the target project's ownership, journal conventions, and Git permissions in its own `AGENTS.md`. The kit repository's root instructions, board configuration, cards, and dated journal belong to this repository.

2. Follow the [guided adoption interview](agents/configure-a-project.md) to select a template or agree on a custom workflow. From the target repository root, preview the result. This example uses the standard template.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris
   ```

3. After approval, apply the same configuration and verify the board.

   ```sh
   python3 tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris --apply
   python3 tools/manage-kanban-board.py validate
   python3 tools/manage-kanban-board.py show
   ```

   Check that the displayed stages and capacity match the approved workflow. Record the project's agreed transition and delivery rules and the adoption result as described in the [adoption guide](agents/configure-a-project.md).

For the optional Batch module, also copy `docs/batches/batch-workflow.md`, `docs/batches/start-and-close-batches.md`, `docs/batches/resume-a-batch.md`, `specification.md`, `batch-description.md`, `batch-tests.md`, and `batch-report.md` under `docs/templates/`.

See the [project directory template](templates/project-layout.md) for the installed layout.
