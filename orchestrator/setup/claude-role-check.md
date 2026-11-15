# Configure the Claude Code role check

Optional. The check makes a Claude Code session stop an action that its role does not allow. The role files stay the rule: it reads their limits from the header of each role file and never widens, narrows or reinterprets them. A project without the check works as before.

## Install

1. Copy `orchestrator/tools/role-limit-hook.py`, `orchestrator/tools/install-claude-role-hook.py` and `orchestrator/hosts/claude/agents/` from the kit. The hook reads `orchestrator/roles/` and the `orchestrator/tools/kanban/` package, which are already installed.
2. Preview, then apply, from the project root:

   ```sh
   python3 orchestrator/tools/install-claude-role-hook.py
   python3 orchestrator/tools/install-claude-role-hook.py --apply
   ```

   The command installs the three definitions in `.claude/agents/` and merges the hook into `.claude/settings.json`. It preserves unrelated settings/hooks, including hooks sharing a group. Recognized distributed copies can be updated/retired; customized files, extra files and symlinks are kept and reported. Reconcile unresolved copies before claiming complete migration. Missing or unsafe sources fail before writes. Rerunning a completed installation is idempotent.

## Start a session as a role

The User starts the session as one role: `claude --agent writer`, `claude --agent developer` or `claude --agent tester`. The names select KR Writer, KR Developer and KR Tester. Legacy session identities `specification-agent` and `development-agent` resolve to the same canonical policies; no duplicate limits are defined. The hook takes the role only from the identity that Claude Code gives such a session. Text in a file, a tool result or a web page never sets or changes it.

For a multi-module project, launch with `KR_MODULE` set to the assigned module ID or `@project` for project-scoped work. Use scoped board commands for filtered views, Card creation and approved reassignment. On the shared board, covered file tools use each Card's stored scope and the primary checkout. They allow body edits only within the assigned scope and role. The hook refuses raw searches of that board, recognized direct shell paths, direct file creation, linked Card paths and edits to Card front matter. For a direct, literal board CLI write, it checks the role and selected scope. The CLI still checks the Card scope and ownership.

When the check refuses an action, it names the rule and the agent to continue with. Continue in a new session, or in an existing one, with that agent. The check never offers to set the limit aside, and an instruction does not set it aside either (see [authority and exceptions](../guidelines/legacy-roles.md#authority-and-exceptions)).

## Protect the settings in a named CLI session

Optional. The hook handles recognized role decisions. The host profile below separately protects the hook's files from ordinary agent writes. Use Claude Code CLI on a supported sandbox host. The matrix below lists verified surfaces.

1. Close agent sessions that use this project. From the User's own terminal, install or update the hook as above.
2. Save this separate JSON settings profile outside the project, at the path substituted for `/absolute/path/to/role-protection.json`. Replace each `/absolute/project` with the canonical, absolute project path. Keep the profile outside directories writable by ordinary agent work. Include any additional hook policy state or local dependency used by your integration before reporting it protected.

   ```json
   {
     "permissions": {
       "deny": [
         "Edit(//absolute/project/.claude/**)",
         "Edit(//absolute/project/orchestrator/roles/**)",
         "Edit(//absolute/project/orchestrator/tools/role-limit-hook.py)",
         "Edit(//absolute/project/orchestrator/tools/kanban/**)",
         "Edit(//absolute/path/to/role-protection.json)"
       ]
     },
     "sandbox": {
       "enabled": true,
       "autoAllowBashIfSandboxed": false,
       "allowUnsandboxedCommands": false,
       "failIfUnavailable": true,
       "filesystem": {
         "denyWrite": [
           "/absolute/project/.claude",
           "/absolute/project/orchestrator/roles",
           "/absolute/project/orchestrator/tools/role-limit-hook.py",
           "/absolute/project/orchestrator/tools/kanban",
           "/absolute/path/to/role-protection.json"
         ]
       }
     }
   }
   ```

3. From the project root, launch the named role with that same User-supplied profile.

   ```sh
   claude --agent developer --settings /absolute/path/to/role-protection.json
   ```

   Keep ordinary permissions and require the sandbox to initialize. Sandboxed Bash still follows the project’s normal approval rules. Review effective settings and any unsandboxed or custom tool surfaces before relying on this profile. Refuse to classify a conflicting or unverified launch as protected.
4. Before using it on real work, verify the installation in a scratch project on the same host. Compare protected fixture files before and after ordinary file-tool writes, shell writes and deletion. Verify that an ordinary permitted project edit succeeds. Keep launch profile, host/version, role and results with the verification evidence.
5. For maintenance, close the protected sessions and run the approved installer, updater or remover in the User's terminal. Keep the managed additions separate from unrelated settings. Update the profile for moved paths or new dependencies and recheck coverage before restarting protected sessions. Stop choosing this launch profile to disable the additional protection. Removing the hook is a separate installer action.

See [Claude Code sandboxing](https://code.claude.com/docs/en/sandboxing) for supported hosts, path formats and effective settings.

## Remove

```sh
python3 orchestrator/tools/install-claude-role-hook.py --remove --apply
```

This removes only its hook entries and recognized distributed agent definitions. Customized copies remain for review. Preview first to inspect the exact actions.

## What the check covers and does not cover

It allows or denies. It asks nothing, grants no permission that a role file does not give, and does not replace the User's approvals.

- **Covered:** `Read`, `Glob`, `Grep`, `Edit`, `Write`, `MultiEdit` and `NotebookEdit` calls on paths inside the project, and `Bash` commands that name a project path, redirect output to one or run `git`. The Bash check reads the command text and is best effort.
- **Not covered:** shell commands that reach files without naming them (variables, a `cd` followed by relative names, scripts); other tools, including MCP and web tools; paths outside the project; a sub-agent started under another name; field-level limits inside ordinary records such as `tests.md`. The shared board checks Card front matter for the covered native file-edit tools.
- **New role limits:** covered Writer writes may reach `project/kanban/backlog/` but are refused for active or completed Cards. Covered Tester writes are limited to Batch acceptance records and evidence. The ordinary Orchestrator startup rule is advisory and does not declare a hook role.
- **Not protected:** a session started with no named agent, which the check does not restrict and never guesses a role for; Codex; the desktop chat applications. For these the limits are advisory.
- **Its own settings:** the hook alone does not verify settings protection. Use the optional host profile above for verified file and sandboxed shell surfaces.
- **When it fails:** a hook that errors or times out does not block the action. The hook reports the failure.

## Coverage by host

| Host and surface | Status | Evidence or missing prerequisite |
| --- | --- | --- |
| Claude Code CLI, named role, recognized tool calls | Native role identity verified. Shared-board policy checked locally with hook events. | Prior native CLI evidence verifies named role identity. Local tests cover Writer, Developer, Tester, legacy IDs and shared Card scope. |
| Claude Code CLI 2.1.323 on macOS, native file writes and sandboxed shell with the above profile | Verified on synthetic fixtures | Ordinary project edit succeeds. Protected setting and policy writes and shell deletion are refused. This applies to the tested filesystem surfaces. |
| Claude Code ordinary project startup | Advisory role | The User confirmed the project identifies KR Orchestrator. An unnamed session has no host role for the repository hook. |
| Codex CLI 0.169.0, including supported profiles | Advisory role | The [documented tool-call hook schema](https://learn.chatgpt.com/docs/hooks) lacks a trusted role field or a verified link to the selected profile. Role text at startup is not included as evidence of enforcement. [Native sandbox protections](https://learn.chatgpt.com/docs/permissions) are separate. |
| Codex resumption, delegated tool calls, check failure and launch environment | Unconfirmed for role enforcement | No candidate integration qualified. Delegated startup metadata does not establish the role for each tool call. |
| Desktop apps, IDE, hosted sessions and Codex MCP or other tool surfaces | Unconfirmed for this integration | The User confirmed advisory Orchestrator startup in Codex and Claude Code. Desktop and IDE hooks, desktop named-role launches and plain Code-tab instruction discovery stay unconfirmed. |

The project does not install a Codex role hook. Report any host/tool combination without verified role binding and protected settings as advisory or unconfirmed.
