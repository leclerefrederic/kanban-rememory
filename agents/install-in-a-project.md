# Install the framework in a project

Agent procedure: perform the installation after agreeing on the workflow and required authorizations with the User. Maintain Cards yourself. Give the User the reader guides for explanations of the framework.

Start in an existing Git repository or run `git init` in a new project. Use Python 3.9 or later and Git.

1. Copy these files from the kit into the target repository, preserving their paths.

   | Directory | Files |
   | --- | --- |
   | `documentation/` | All reader guides and `examples/`, including the shared `lean-specifications.md` manifesto |
   | `agents/` | `configure-a-project.md`, `work-in-a-project.md`, `lean-specifications.md`, `maintain-rememory.md` |
   | `agents/roles/` | All three role files |
   | `agents/kanban/` | All three operating references |
   | `agents/templates/` | `kanban-card.md`, `project-layout.md` |
   | `agents/tools/` | `manage-kanban-board.py` and the `kanban/` package |
   | `project/rememory/` | `daily-template.md` |

   In the target repository's root `AGENTS.md`, create or merge this entry:

   ```markdown
   Read the [shared working instructions](agents/work-in-a-project.md) before adopting the kit or working on cards.
   ```

   Define the target project's ownership, journal conventions, and Git permissions in its own `AGENTS.md`. The kit repository's root instructions, board configuration, cards, and dated journal belong to this repository.

   Both agents read the [shared manifesto](../documentation/lean-specifications.md) and follow its [agent rules](lean-specifications.md), referenced by the shared instructions and both roles. Use the approval test when defining and reviewing scope.

2. Follow the [guided adoption interview](configure-a-project.md) to select a template or agree on a custom workflow. From the target repository root, preview the result. This example uses the standard template.

   ```sh
   python3 agents/tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris
   ```

3. After approval, apply the same configuration and verify the board.

   ```sh
   python3 agents/tools/manage-kanban-board.py init --template standard --wip-limit 1 --timezone Europe/Paris --apply
   python3 agents/tools/manage-kanban-board.py validate
   python3 agents/tools/manage-kanban-board.py show
   ```

   Check that the displayed stages and capacity match the approved workflow. Record the project's agreed transition and delivery rules and the adoption result as described in the [adoption guide](configure-a-project.md).

## Optional Batch module

Copy all operating references under `agents/batches/`, `agents/run-scheduled-batch-job.md`, the four Specification and Batch templates under `agents/templates/`, and `agents/tools/guard-batch-work.py`. Create the Specification state and resource directories shown in the project directory template. The reader guides explain this optional module without enabling it.

Configure the project instructions used by each agent to read the shared instructions and its role. For Specification Agent, use:

```text
Read agents/work-in-a-project.md and agents/roles/specification-agent.md
before preparing Specifications, Batches, or acceptance tests.
```

For Development Agent, use:

```text
Read agents/work-in-a-project.md and agents/roles/development-agent.md
before implementing work, handling corrections, or performing Git operations.
```

Give both agents access to the same project records and verify that a fresh session identifies its role, current Batch state, and next authorized action. The [worked example](batches/delivery-example.md) shows the records; the [state table](batches/batch-workflow.md#batch-states-and-transitions) defines the handoffs. Copying the [scheduled-job procedure](run-scheduled-batch-job.md) does not install or enable a scheduler.

See the [project directory template](templates/project-layout.md) for the installed layout.

For optional delivery notifications, copy `agents/configure-telegram.md` and `agents/tools/notify-telegram.py`, then follow [Configure Telegram](configure-telegram.md).

For the optional macOS app, follow [KRR getting started](runner/build-and-run.md). Its current repository check also requires the Batch directory layout.
