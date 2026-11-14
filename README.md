# 🧠 Kanban Rememory

**New chat. Same project. Keep the plot.**

Kanban Rememory is a framework built on Git and Markdown for people building software with AI agents. It keeps the work, decisions, approved scope, and test evidence in the repository, so another session can pick up where the previous one left off.

A little structure. A lot less “wait, why did we build that?”

[Get started](docs/getting-started.md) · [Read the manifesto](docs/lean-specifications.md) · [Explore the workflow](docs/batches/batch-workflow.md)

## Why this project exists

Writing code is only part of building software. A project still needs a record of what was requested, what was approved, what changed, and whether it actually works.

With AI agents, that continuity needs a home. Conversations get long. Sessions end. A fresh agent arrives with a fresh context. A useful decision gets buried in a chat, a “small improvement” grows into an unrequested feature, or “done” turns out to mean “the code was written.”

Kanban Rememory gives that context a durable home in the project itself:

- **Direction:** the agreed outcome and scope.
- **Progress:** active Cards, dependencies, and blockers.
- **Context:** decisions and the reasons behind them.
- **Evidence:** results tied to the revision that was tested.
- **Continuity:** an explicit next action for the next session.

Less archaeological digging through chats. More building the thing you asked for. ✨

## Meet the moving parts

| Part | What it does | Where it lives |
| --- | --- | --- |
| **Cards** | Track executable tasks, their dependencies, blockers, and completion evidence. One folder represents one stage. | `project/kanban/` |
| **Rememory** | Keeps a concise journal of decisions, verified milestones, and next actions for handoffs. | `project/rememory/` |
| **Specifications** | Describe the intended outcome, approved scope, and observable acceptance criteria. | `project/specs/` |
| **Delivery Batches** | Group one or more approved Specifications for a delivery, with tests, a report, and your acceptance decision. | `project/batches/` |

Start with Cards and Rememory. Add the optional Specification and Batch workflow when you need an explicit agreement about what a delivery includes and how to accept it.

**A Batch groups Specifications. Cards track the work independently.** A Card can reference a Batch or Specification, and standalone work can have its own Card without a Batch.

The files stay readable in your editor and versioned alongside your code. Stable IDs connect related records; Git preserves their history. Tiny files. Long memory.

## From “could we…” to a verified delivery

Say you need a booking export that preserves accents and commas.

1. **Describe the outcome.** The Specification defines the export behavior and examples that will prove it works. Suggestions stay separate until you approve them.
2. **Agree on the delivery.** A Batch selects the exact Specification revisions and records the work priorities. Its approved scope stays fixed.
3. **Build and track.** The Development Agent creates its Cards, implements the export, and runs the applicable technical checks.
4. **Try the actual result.** Acceptance tests identify the revision to test, explain the preparation and actions, and record what passed, failed, or remains untested.
5. **Make the decision.** You accept or reject the delivery. The report preserves that decision and its evidence for the next session.

Every observed defect becomes open debt, even when the test otherwise passes. A blocking defect sends the open Batch through correction and renewed acceptance. Outstanding tests remain visible. Rejected work keeps its records so the next attempt can learn from it.

The Specification Agent handles the intended behavior and guides acceptance. The Development Agent handles implementation and technical evidence. You approve scope and decide whether to accept the delivery. These are vendor-neutral roles, which can be carried out by the same agent at different stages.

## Lean by design. Enthusiastic by permission.

> Build what earns its place. Write only the code needed to deliver it.

Our [Lean Development Through Lean Specifications manifesto](docs/lean-specifications.md) gives every requirement three questions to answer:

- What value or protection does it provide?
- Who explicitly agreed to it?
- How will we verify it?

Agents can propose improvements. Adding them requires agreement. When expected behavior is unclear, the affected work waits for clarification. The aim is the smallest complete experience that delivers the approved outcome.

Yes, even that clever little extra button has to earn its place.

## Start small. Keep it yours.

Bring a Git repository, Python 3.9 or later, and the agent you work with.

The [getting started guide](docs/getting-started.md) walks you through installing the reusable files and choosing a short, standard, long, or custom workflow. Agree on the stages and work-in-progress limit, then validate the board. Add Batches when your delivery process needs them.

The kit includes templates, shared agent instructions, and commands to create, move, display, and validate Cards. Checks cover structural issues such as broken local links, duplicate IDs, and incomplete acceptance checklists. Your project's tests and acceptance results establish whether the software works.

This repository uses its own Cards and Rememory to evolve the framework. Its project history is an example; the installation guide identifies the reusable pieces for your own project.

## A little company on your Mac

**Kanban Rememory Runner (KRR)** is the native Swift macOS companion for managing Codex and Claude Code watchers: background jobs associated with a repository. Current watchers request a read-only board summary; autonomous Batch dispatch is still to be implemented. Follow the [KRR startup guide](docs/runner/getting-started.md) to build and run it. The core Markdown workflow can be used independently of the app.

## Find your next step

| You want to… | Start here |
| --- | --- |
| Adopt the framework in a project | [Getting started](docs/getting-started.md) |
| Understand the board and its policies | [Kanban guide](docs/kanban/board-guide.md) |
| Write a useful task Card | [Card guide](docs/kanban/write-task-cards.md) |
| Keep requirements focused | [Lean Specifications manifesto](docs/lean-specifications.md) |
| Organize a delivery and its acceptance | [Specification and Batch workflow](docs/batches/batch-workflow.md) |
| See filled-in delivery records | [Worked delivery example](docs/batches/delivery-example.md) |
| Build and start the macOS companion | [KRR getting started](docs/runner/getting-started.md) |
| Understand the project layout | [Directory template](docs/templates/project-layout.md) |
