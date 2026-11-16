# Install Kanban Rememory {version}

Three steps. The kit never writes outside `kanban-rememory/` until you approve a plan.

1. Unzip `{zip}` in a folder **outside** your repository, for example your downloads folder. Do not unzip it inside the repository.
2. Open your agent (Claude Code, Codex or another) in the root of your repository, on `main`, with a clean checkout.
3. Give it this instruction, with the real path of the unzipped folder:

   ```text
   Install Kanban Rememory. The kit is /path/to/{folder}. Follow /path/to/{folder}/kanban-rememory/orchestrator/install.md.
   ```

The agent checks the prerequisites, shows its plan, asks for your approval, then asks its questions and installs. It commits and never pushes. The same instruction upgrades an existing installation.
