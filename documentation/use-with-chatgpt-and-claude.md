# Use Kanban Rememory with ChatGPT and Claude

Kanban Rememory uses the same project records and working method with Codex and Claude Code. Optional integrations help an assistant find the instructions or check some role limits. They do not change your decisions or grant more permission.

## Coordinate from one chat

Open a normal session in an adopted project. Codex reads `AGENTS.md`; Claude Code reads it through `@AGENTS.md` in `CLAUDE.md`. **KR Orchestrator** starts by default unless a role was explicitly chosen. It prepares scope with you, records decisions and delegates approved execution to KR Developer and acceptance to KR Tester.

Continue in that chat when you clarify a requirement, answer a test case or decide on delivery. The Orchestrator routes the answer to the responsible agent. Explicitly selected roles and assigned subagents retain their roles. If the host cannot delegate, the session explains the blocker and leaves an actionable handoff; it does not take over a role it cannot perform.

## One shared core

The repository keeps the roles, Cards, Specifications, Batches, tests, reports and Rememory journal. Agents recover the applicable instructions, approved scope and evidence from those records. Switching assistants does not require another format or erase earlier decisions.

The same boundaries apply:

- You decide the scope, authorize execution and make the final delivery decision. Publication follows the project's permissions.
- KR Writer prepares scope and backlog Cards. KR Developer owns execution, technical checks, journal entries and Git. KR Tester owns acceptance results.
- Tests identify the exact candidate. A passed case does not by itself accept a Batch.
- Completed Cards and closed Batch records stay unchanged. New work and inherited defects receive their own follow-up records.

The [framework guide](understand-the-framework.md) explains these responsibilities and records. The [lean manifesto](lean-specifications.md) supplies the shared principles.

## Optional integrations

| Integration | What it adds |
| --- | --- |
| Role skills | The same four `kr-*` skills route each assistant to the shared instructions. They are discovered in `.agents/skills/` for Codex and `.claude/skills/` for Claude Code. |
| Claude Code role check | A check for sessions launched as named Writer, Developer or Tester agents refuses covered actions outside their role limits. |
| Batch publication check | An optional Git hook checks guarded Batch closure pushes before publication. |

Your agent installs and verifies selected options, preserving customizations during updates. Copying alone does not prove activation. See the agent procedures for [skills](../agents/setup/skills.md), the [Claude Code role check](../agents/setup/claude-role-check.md), and [Batch setup](../agents/setup/batches.md).

A project works without these integrations. Instructions and approval rules still apply; an integration only provides the checks documented for it.

## Understand what a check covers

The Claude role check covers selected tools and visible project paths in named sessions. It does not enforce role limits in Codex or ordinary chat applications, and it does not cover every shell command or tool. A session without a named agent is not restricted by that check. Role instructions remain applicable in all these cases.

The [role-check procedure](../agents/setup/claude-role-check.md#what-the-check-covers-and-does-not-cover) lists its precise coverage, failure behavior and unconfirmed host details. Do not infer enforcement from an assistant's name or from the presence of a hook file. Other sandbox and approval controls can impose their own limits.

Project interfaces and conversation histories differ between products. Do not assume that instructions from another chat application carry into a coding session. The repository's entry files and project records provide the shared starting point.

## Change assistants or resume later

Identify the repository and, if known, the Card or Batch. Ask the new session to recover the current state and continue the next authorized action. It checks the records and obtains Git evidence through KR Developer before resuming affected work. Existing authorization remains usable where it still covers that action.

For a delivered candidate, resume acceptance on its recorded revision. For interrupted closure, recover the existing closure before starting new work. [Resume work](resume-work.md) explains what you should expect.

## Sources and verification

Vendor documentation for the skill locations and hooks was checked on 2026-11-14. Product details can change; the setup procedures distinguish verified behavior from unconfirmed coverage.

- [Codex skills](https://developers.openai.com/codex/skills) and [approval controls](https://developers.openai.com/codex/agent-approvals-security)
- [Claude Code skills](https://code.claude.com/docs/en/skills) and [hooks](https://code.claude.com/docs/en/hooks)
