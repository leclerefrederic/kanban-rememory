# Install Kanban Rememory 0.1.0

## For the user

1. Put this file and `kanban-rememory-kit-0.1.0.zip` in the root of your repository, which is on `main` with a clean checkout.
2. Open your agent (Claude Code, Codex or another) there and tell it: `Follow START.md.`

The agent shows its plan and asks for your approval before it changes anything. It commits and never pushes. The same instruction upgrades an existing installation.

## For the agent

1. Unzip `kanban-rememory-kit-0.1.0.zip` into a new folder outside the repository, created with `mktemp -d`. KIT = `<that folder>/kanban-rememory-kit-0.1.0`.
2. Follow `KIT/kanban-rememory/orchestrator/install.md`. `START.md` and `kanban-rememory-kit-0.1.0.zip` are not part of the repository content: never stage them.
3. After its section 5, ASK: `Delete START.md and kanban-rememory-kit-0.1.0.zip? yes / no`. `yes`: delete both. `no`: leave both.
