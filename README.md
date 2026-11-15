# Kanban Rememory

**You bring the intent. The agent ships the work. The repository remembers.**

Five cards went through in one pass, merge included. The project owner didn't have to touch the board or step in while the agent worked. The next session can open the repository and see what shipped.

Kanban Rememory is a Git and Markdown toolkit for running software projects with AI agents. It keeps the work beside the code so it can survive the chat that started it.

## Stop being the project's human RAM

You ask for a form. You get two extra buttons and a settings screen. Then you open a new chat and find yourself explaining the form again, trying to remember which build you tested.

Put the agreement in the repository. Give each record one job.

- **The card** says what should happen, what's in scope, and how to tell when it's done. Each module has its own board, and the card's folder shows its stage.
- **The journal** records decisions and milestones that matter beyond one card.
- **Git** keeps the history and identifies the exact revision that was checked and published.

The agent keeps those records current. You can switch chats without having to reconstruct the project from memory.

## From request to merge

You decide what you want. The agent records the agreement, implements it, and runs the checks that apply. Work can happen directly on `main` or on a release branch.

You can approve the verified revision at the end or authorize publication up front. With approval up front, the agent can publish once the checks pass and the result stays within the agreed scope.

If you asked for a form, the card should tell the agent what makes the form ready to ship. The settings screen can wait until someone actually asks for it.

## Start with a real task

[Start a project](documentation/guide.md#start-a-project) with your agent. You'll need Git and Python 3.9 or later. Installation starts no background service.

The [user guide](documentation/guide.md) covers requests, approvals, and handoffs. The agent follows the [workflow](orchestrator/workflow.md). The [Lean Specifications manifesto](documentation/lean-specifications.md) explains how to keep scope under control.

This repository uses Kanban Rememory to build Kanban Rememory.
