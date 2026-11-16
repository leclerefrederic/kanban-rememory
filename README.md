# Kanban Rememory

**You call the shots. The agent does the work. The repo remembers.**

Building software with AI, even though you don’t code for a living? Kanban Rememory is for you. It’s a Git and Markdown toolkit that gives your agent a place to keep track of what you asked for, what you agreed to, and what shipped. You can run the project in plain language while the agent keeps the records beside the code.

## 🧠 Stop being the project’s human RAM

You ask for a contact form. Two chats later, you’re explaining the same form again and trying to remember which version you tested. Somehow there’s a settings screen now.

Kanban Rememory gives that information somewhere to live.

- **The card** records the job, what’s in scope, and how you’ll know it’s done. Its place on the board shows where the work stands.
- **The journal** records decisions and milestones you’ll want to find later.
- **Git** identifies the exact revision that passed the checks and the one that shipped.

When you switch chats, ask the next agent to resume work in the repository. It can pick up from the card and the recorded checks. You can retire the recap speech.

## 🌍 Keep world domination in the backlog

You decide what gets built, what counts as done, and when the agent can publish. The agent writes down the agreement, builds the form, and runs the checks. If it thinks the form needs a settings screen, it asks before adding one.

You can approve the exact revision after seeing what passed, or authorize publication up front. With that authorization, the agent can publish once the checks pass and the work stays within the agreed scope. You can work directly on `main` or group work on a release branch.

On this project, five cards went from request to merge in one pass. The owner never had to move a card by hand.

## 🚀 Start with one real task

You’ll need a Git repository and Python 3.9 or later. To check and publish work, your repository needs a remote named `origin` with a `main` branch. That remote can be on GitHub, another Git host, or your own machine.

[Set up Kanban Rememory with your agent](kanban-rememory/documentation/guide.md#start-a-project). Setup starts no background service.

Then try a request like this.

> Add a contact form with name, email, and message. A visitor should see a confirmation after submitting it. Show me what you checked and ask me before you publish.

- [User guide](kanban-rememory/documentation/guide.md) for giving work, approving changes, and picking up in a new chat.
- [Agent workflow](kanban-rememory/orchestrator/workflow.md) for the rules your agent follows.
- [Lean Specifications manifesto](kanban-rememory/documentation/lean-specifications.md) for keeping a contact form from turning into a whole admin panel.

This repository uses Kanban Rememory to build Kanban Rememory.
