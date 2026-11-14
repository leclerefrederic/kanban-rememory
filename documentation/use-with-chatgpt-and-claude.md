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
| Role limits | Written in the role instructions; checked by a script any agent can run | A `PreToolUse` hook calls the script and blocks a forbidden action | A `PreToolUse` hook calls the script and denies a forbidden action; sandbox and approval settings add a second limit |
| Distribution | Files of the kit | A skill or plugin for Claude Code | A skill or plugin for Codex |

Both assistants find the same skill file format in their own folder, so one skill text can serve both. Hooks differ. Claude Code can attach a hook to a skill. Codex loads project hooks only after you trust the project and review the hook. Codex does not support an "ask" answer from a hook, so branch hooks must only allow or deny.

A hook is a safety net, not the only protection. The role instructions and the guard script remain the rule; a hook only makes an assistant stop earlier.

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
