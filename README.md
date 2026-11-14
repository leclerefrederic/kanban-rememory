# 🧠 Kanban Rememory

**Build what we agreed. Prove it works. Remember why.**

Kanban Rememory is a Git and Markdown framework for building software with AI agents. It keeps tasks, decisions, approved scope, and test results in your repository, ready for the next session or the next agent.

Your project has a memory now. Please use it.

[Get started](docs/getting-started.md) · [Read the manifesto](docs/lean-specifications.md) · [See a complete example](docs/batches/delivery-example.md)

## We built this because “done” got expensive

You ask for a form. You get two extra buttons, a settings screen, and a cheerful explanation of why you needed them.

You ask to test it. The agent forgets to tell you which build to open.

Something breaks. The next session starts. Time to explain the whole bloody project again.

Sound familiar?

Kanban Rememory grew out of exactly that frustration. Writing code gets easier. Keeping the work coherent still takes care: what was agreed, what was actually built, what passed, what failed, and what happens next.

So we put that information where the work lives: **in the repository**. The next agent can read the decisions, find the current task, inspect the evidence, and resume from a known point. You get something concrete to review when it says “done.”

Less chat archaeology. More software you can actually use.

## Give every piece of work a home

| Piece | Its job | Its home |
| --- | --- | --- |
| **Cards** | Track executable tasks, dependencies, blockers, and proof of completion. | `project/kanban/` |
| **Rememory** | Keep the decisions, verified milestones, and next actions needed to resume work. | `project/rememory/` |
| **Specifications** | Define the outcome, scope, and observable acceptance criteria. | `project/specs/` |
| **Batches** | Group one or more approved Specifications into a delivery with tests, a report, and your decision. | `project/batches/` |

**Start with Cards and Rememory.** A task gets a Card. Its folder tells you the stage; the Card tells you whether work is moving, waiting, or blocked. Rememory keeps the useful context between sessions.

Add Specifications and Batches when you need to agree on a delivery before building it. A Batch groups Specifications. Cards track the implementation independently and can reference the relevant Batch or Specifications. Standalone tasks can stay standalone.

Everything is readable in an ordinary editor. Stable IDs connect the records. Git keeps their history. You choose the agent and keep the project context with your code.

Tiny files. Long memory. 🧠

## From “I want this” to “yes, this works”

Say you need a CSV export that preserves names with accents and commas.

1. **Agree on the result.** Write a Specification with the expected behavior and concrete examples. Keep suggestions separate until you approve them.
2. **Set the delivery scope.** Select the approved Specification revisions in a Batch and record priorities. That baseline stays fixed while the Batch is active.
3. **Do the work.** The Development Agent creates its Cards, implements the change, reviews the diff, and runs the applicable technical checks.
4. **Test the actual thing.** Each acceptance case starts with the exact revision, build, setup, actions, and expected result. Record your verdict, then move to the next case.
5. **Decide with evidence.** You accept or reject the delivery. Its report keeps the decision, results, and remaining debt available for the next session.

The Specification Agent handles the intended behavior and guides acceptance. The Development Agent implements, verifies, and handles Git. One agent can wear both hats at different stages. You approve the scope and decide whether the delivery is accepted.

The [worked example](docs/batches/delivery-example.md) shows what those files actually contain.

## When it breaks, keep the plot

Software has defects. Our process needs to handle them without losing the work or pretending an untested scenario passed.

Every observed defect becomes open debt, even when the test otherwise passes. A blocking defect keeps the Batch from being accepted: correct it within the agreed scope, deliver a new candidate, and resume the failing, affected, and previously blocked tests. Preserve the earlier results.

Nonblocking debt can be deferred explicitly. Rejected code stays on an archive branch; the closing records preserve the findings and tests still owed. A successor Batch carries forward the relevant debt and outstanding checks.

“We'll remember to fix it” gets a reference and a place in the record. Future you has suffered enough.

## Every feature pays rent

> Build what earns its place. Write only the code needed to deliver it.

That is our [Lean Development Through Lean Specifications manifesto](docs/lean-specifications.md). Every requirement has to answer:

- What value or protection does it provide?
- Who explicitly agreed to it?
- How will we verify it?

An agent can suggest an improvement. Implementing it requires agreement. That extra button, configuration option, or “helpful” message needs to earn its place, too.

Aim for the smallest complete experience. Reuse what works. Protect correctness, security, accessibility, and data where required. Stop when the agreed outcome is achieved and verified.

**Be lazy about writing unnecessary code. Be stubborn about delivering what was agreed.**

## Bring your repo. Keep your habits that work.

You need Git, Python 3.9 or later, and an agent that can work with repository files.

The [getting started guide](docs/getting-started.md) walks through installing the reusable kit and choosing a short, standard, long, or custom workflow. Agree on the stages and work-in-progress limit. Add the optional Batch module when you need it.

The kit includes document templates, agent instructions, and commands to create, move, display, and validate Cards. Validation catches structural problems such as duplicate IDs, broken local links, and incomplete completion checklists. Product tests and acceptance provide the evidence that the delivered software works.

We use the framework to build the framework. Very meta. Also a good way to find its rough edges. This repository's Cards and delivery records are its own history; the installation guide shows which reusable files belong in your project.

## A small companion for your Mac

**Kanban Rememory Runner (KRR)** is the native Swift macOS app for managing repository watchers using Codex or Claude Code.

Today, those watchers request a read-only board summary. Autonomous Batch dispatch still needs implementation. The [KRR startup guide](docs/runner/getting-started.md) explains how to build and run the current app. The Markdown framework works independently of it.

## Pick your next move

| You want to… | Start here |
| --- | --- |
| Use this in your project | [Getting started](docs/getting-started.md) |
| Understand the board | [Kanban guide](docs/kanban/board-guide.md) |
| Write a useful task Card | [Card guide](docs/kanban/write-task-cards.md) |
| Keep scope lean | [The manifesto](docs/lean-specifications.md) |
| Organize a delivery and its acceptance | [Specification and Batch workflow](docs/batches/batch-workflow.md) |
| See filled-in records | [Worked delivery example](docs/batches/delivery-example.md) |
| Run the macOS companion | [KRR getting started](docs/runner/getting-started.md) |
| Find where things belong | [Directory template](docs/templates/project-layout.md) |
