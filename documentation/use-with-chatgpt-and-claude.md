# Use Kanban Rememory with ChatGPT and Claude

Kanban Rememory works with ChatGPT (Codex) and Claude (Claude Code). The method is the same for both. Each assistant can also have extra capabilities of its own, kept apart so they never change the method.

## One shared core

The shared core is what makes a project behave the same whichever assistant you use:

- the roles, Cards, Specifications, Batches, tests and reports;
- the approval rules and the limit on work in progress;
- the Rememory journal and the evidence it records;
- the checks that agents run before acting, such as the Batch guard script.

A rule in the core means the same thing for every assistant. An assistant that starts a session reads the core first and can recover the project state from it alone.

## Two optional branches

A branch adds help for one assistant. It can make a rule easier to follow or enforce it mechanically. It cannot add, remove or reinterpret a rule.

| | Shared core | Claude branch | Codex branch |
| --- | --- | --- | --- |
| Skills | Same `SKILL.md` content (`name`, `description`, instructions) | Discovered in `.claude/skills/` | Discovered in `.agents/skills/` |
| Role limits | Written in the role instructions. The role files also carry their read and write limits in a header that the Claude check reads | Optional check for a session started as a named agent (`claude --agent`): a `PreToolUse` hook refuses an action outside the role and names the agent to use. Sessions without a named agent are not restricted | Advisory in this version: the tool call carries no agent identity and no tested per-session setting declares a role. Sandbox and approval settings can add their own limit |
| Distribution | Files of the kit, copied into each discovery folder by a script | Same copy; a plugin is possible but not built | Same copy; a plugin is possible but not built |

Both assistants find the same skill file format in their own folder, so one skill text can serve both. The kit's skills live in `agents/skills/`; they point to their operating instructions. A script in the kit copies them into the two discovery folders, and can report a copy that has drifted from the kit. Hooks differ. Claude Code can attach a hook to a skill. Codex loads project hooks only after you trust the project and review the hook. Codex does not support an "ask" answer from a hook, so branch hooks must only allow or deny.

A hook is a safety net, not the only protection. The role instructions and the Batch checks remain the rule; a hook only makes an assistant stop earlier. Two optional checks exist today: the push check for Batches, and the Claude Code role check described in [Configure the Claude Code role check](../agents/configure-claude-role-hook.md). Neither protects a session or tool that is not listed there.

## Coordinate from one chat

Open a normal session in an adopted project. Codex reads `AGENTS.md`; Claude Code reads it via `@AGENTS.md` in `CLAUDE.md`. [KR Orchestrator](../agents/roles/orchestrator.md) starts by default unless a role was explicitly chosen. The Orchestrator frames the Card or Batch, asks for approval and delegates to KR Developer or KR Tester as needed. If the host cannot delegate, the session keeps the approved handoff available and explains the blocker.

## Where each assistant draws its lines

The two assistants do not organize their projects the same way, so the kit does not rely on the assistant to keep the roles apart.

- **Claude:** a Cowork project and the Code tab are separate spaces. A Cowork project holds its folders and its instructions for every session in it. In the Code tab you choose the folder for each session.
- **ChatGPT and Codex:** one project space can hold Chat, Work and Codex conversations, so nothing in the product separates the roles. A local project gives its chats access to one or more folders; a ChatGPT project has no folder access. Each product keeps its own conversation history.
- **Instructions:** project instructions exist on both sides, but the documentation does not say that they carry from ChatGPT Work into Codex. The repository's `AGENTS.md` and the kit documents remain the instructions every assistant can find.

Because the roles can blur, the kit protects the **hand-offs**, not the conversations. Approval of a Specification is proven in Git. Your verdict on a delivery is recorded for the exact tested revision. A closed Card never changes. An optional check can also refuse a push that would close a Batch without your recorded acceptance. An agent asked to do the other role's work names the rule and sends you to the right agent. It cannot move work past these points without your decision. Assistants that cannot enforce rules in their own chat window, such as the chat apps, rely on these records and on the instructions only.

Some details are not confirmed, in particular whether repository hooks run in the desktop apps. The kit does not depend on them.

## What the Claude Code role check protects

It protects a Claude Code session started as the named Writer, Developer or Tester role, and only for the file reads, file writes, searches, Git commands and visible shell paths of that role's limits. It does not protect: a session with no named agent, Codex, the chat applications, shell commands that hide the file they touch, other tools, or the check's own settings file, and it lets an action through when it fails. For these the limits are advisory. It was tested with the command line, which gives the session identity to the hook; whether it runs in the Claude Code desktop app is unconfirmed, and so are the Codex questions about the shell environment, sub-agents and a per-session role. The agent procedure lists each limit and each unconfirmed fact.

## What this means for you

- You can switch assistants, or use both on one project, without changing the project records.
- A project works without either branch. Install a branch to get its extra help.
- A branch never grants an agent more permission. Approval of scope, acceptance and publication stays with you.

## Checked sources

The skill folders and hook behavior above come from the vendors' documentation, checked on 2026-11-14. Check it again before relying on a detail, because both products change.

- [Codex skills](https://developers.openai.com/codex/skills)
- [Codex hooks](https://developers.openai.com/codex/hooks)
- [Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Claude Code hooks](https://code.claude.com/docs/en/hooks)
