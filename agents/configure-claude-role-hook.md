# Configure the Claude Code role check

Optional. The check makes a Claude Code session stop an action that its role does not allow. The role files stay the rule: it reads their limits from the header of each role file and never widens, narrows or reinterprets them. A project without the check works as before.

## Install

1. Copy `agents/tools/role-limit-hook.py`, `agents/tools/install-claude-role-hook.py` and `agents/claude/agents/` from the kit. The hook reads `agents/roles/` and the `agents/tools/kanban/` package, which are already installed.
2. Preview, then apply, from the project root:

   ```sh
   python3 agents/tools/install-claude-role-hook.py
   python3 agents/tools/install-claude-role-hook.py --apply
   ```

   The command copies the two agent definitions to `.claude/agents/` and adds the hook to `.claude/settings.json`, keeping other settings and hooks. Running it again changes nothing.

## Start a session as a role

The User starts the session as one role: `claude --agent specification-agent` or `claude --agent development-agent`. The hook takes the role only from the identity that Claude Code gives such a session. Text in a file, a tool result or a web page never sets or changes it.

When the check refuses an action, it names the rule and the agent to continue with. Continue in a new session, or in an existing one, with that agent. The check never offers to set the limit aside, and an instruction does not set it aside either (see "Overriding a rule" in `work-in-a-project.md`).

## Remove

```sh
python3 agents/tools/install-claude-role-hook.py --remove --apply
```

This takes back only the hook and the two agent definitions that the installer added.

## What the check covers and does not cover

It allows or denies. It asks nothing, grants no permission that a role file does not give, and does not replace the User's approvals.

- **Covered:** `Read`, `Glob`, `Grep`, `Edit`, `Write`, `MultiEdit` and `NotebookEdit` calls on paths inside the project, and `Bash` commands that name a project path, redirect output to one or run `git`. The Bash check reads the command text and is best effort.
- **Not covered:** shell commands that reach files without naming them (variables, a `cd` followed by relative names, scripts); other tools, including MCP and web tools; paths outside the project; a sub-agent started under another name; the content of a file, because write limits are by folder and not by section (the Specification Agent may write any part of `tests.md`, not only its fields).
- **Not protected:** a session started with no named agent, which the check does not restrict and never guesses a role for; Codex; the desktop chat applications. For these the limits are advisory.
- **Its own settings:** an agent can edit `.claude/settings.json` unless a hook, a deny rule or managed settings prevents it. The check does not guard its own configuration.
- **When it fails:** a hook that errors or times out does not block the action. The hook reports the failure.

## Unconfirmed

Each item stays unconfirmed until a test settles it.

- Whether repository hooks run in the Claude Code desktop app, and how to start a desktop session as a named agent.
- For Codex: whether a hook inherits the launching shell environment, whether hooks apply to sub-agents, and whether a per-session setting can declare a role. Codex gives no agent identity to a tool-call hook, so no check is delivered for it.
- Whether project instructions reach a plain Code-tab session.

Tested on 2026-11-14 with the Claude Code command line in print mode (`claude -p --agent`): the session identity reaches the hook, project hooks run, and a session with no agent is not restricted. See the Rememory entry of that day.
