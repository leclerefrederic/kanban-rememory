# 🧠 Kanban Rememory

**You bring the intent. The agents do the work. The repository remembers.**

Kanban Rememory is a Git and Markdown framework for running software projects with AI agents. It gives them a shared way to understand requests, organize work, implement changes, verify results, and continue across sessions.

You explain what you want, approve the scope, authorize work and judge the result. **The agents write the records and maintain the board.**

[Read the guides](documentation/index.md) · [Start a project](documentation/start-a-project.md) · [Read the manifesto](documentation/lean-specifications.md)

## Why this box exists

You ask for a form. You get two extra buttons, a settings screen, and a cheerful explanation of why you needed them. You ask to test it. The agent forgets to tell you which build to open. A new session starts. Time to explain the whole bloody project again.

Congratulations. You are now the project's human RAM.

Kanban Rememory keeps agreed behavior, work state and evidence beside the code. Agents can resume authorized work and leave a useful handoff. You can inspect the records. Less chat archaeology; more software you can use.

## The guiding principles: every feature pays rent

The [Lean Specifications manifesto](documentation/lean-specifications.md) sets the shared principles:

- **Start with the outcome.** Explain who needs to achieve what and how success will be checked.
- **Make each requirement earn its place.** Keep behavior that provides value or necessary protection.
- **Specify the smallest complete experience.** Include relevant failure recovery and binding mockup details. Ambiguous behavior becomes a question.
- **Give requirements a way to pass or fail.** Observable criteria and evidence identify what was checked and on which revision.
- **Change scope only by agreement.** Suggestions stay separate; the approved baseline of an active Batch stays fixed. Every observed defect remains debt until its correction is verified.
- **Build the simplest thing that meets the criteria.** Reuse what works, preserve required protections, and stop when the agreed outcome is verified.

## The records that keep the work together

A **Card** carries the outcome, agreed scope, decisions and delivery evidence. Add a Resources section when it needs attachments or references. **Rememory** keeps the project journal of decisions, milestones and publications with links to the relevant Cards. Earlier Specifications and Batches are available in the archived project or Git history.

## One Kanban per module

Each declared module stores its Cards and their resources in its own Kanban. Cards without a natural owner go to `misc`. A cross-module change that ships together has one Card, linked by its stable ID from the affected modules. The shared workflow and project settings live in `project/settings.json`. The project journal is in `project/rememory/`, with one file per date.

## One agent follows the Card

In a normal chat, the same agent clarifies the request, updates the Card, implements the authorized change, runs the applicable automated checks and publishes under the project's permissions. It uses the relevant skills as guides. You decide scope and acceptance where your decision is required.

## Pick your next move

[Start a project](documentation/start-a-project.md) with your agent. It checks prerequisites, proposes a short, standard, long or custom workflow, then installs and verifies the approved setup. The tools require Git and Python 3.9 or later.

Agent sessions execute the kit instructions and checks. Installing the kit starts no background development service.

This repository uses the same Cards and records to develop the kit; your agent installs the reusable pieces in yours.

The [guide index](documentation/index.md) routes requests, resumption, defects and switching assistants. Human guides live in `documentation/`; the separate [agent index](agents/index.md) routes operating instructions and templates.
