# Kanban Rememory

**You call the shots. The agent does the work. The repo remembers.**

You have an idea. An AI agent. A Git repository. Let's build something.

Then the chat gets long. You open another one. The agent forgets the agreement. You explain it again. You ask for a contact form; somehow you're reviewing an admin dashboard.

**Kanban Rememory exists so you can build software without becoming the project's human RAM.**

KR is a Git, Markdown and Python toolkit for people building with AI agents, including people who don't code for a living. It gives the agent a workflow and keeps the project's memory beside the code: what you asked for, what you agreed to, what's in progress, what passed the checks and what actually shipped.

[Install it in your repo ↓](#install-it-in-your-repo) · [User guide](kanban-rememory/documentation/guide.md) · [Agent workflow](kanban-rememory/orchestrator/workflow.md)

## 🧠 The chat ends. The project shouldn't forget.

Building with agents makes it easy to start. Keeping the thread across sessions is where things get messy.

The brief lives in one chat. A decision lives in another. The agent says “done”, but which revision did you test? What was approved? Where do you pick up tomorrow?

That's the problem KR grew around. Give the work a durable home in the repository, and let the agent maintain it as it builds.

The goal: **spend your attention on the product, instead of reconstructing its history.**

## 🎯 Your vision. Your scope. Your green light.

You describe the outcome and the constraints. The agent, acting as the **Orchestrator**, records the agreement, does the authorized work and checks the result.

You decide what counts as done and when it can publish. You can approve the checked revision when it's ready, or authorize publication in your original request. Work can happen directly on `main` or on a release branch.

If the agent thinks your contact form needs a settings screen, it asks. World domination can wait in the backlog.

KR follows a [lean specification manifesto](kanban-rememory/documentation/lean-specifications.md): every requirement earns its place, every outcome has a way to pass or fail, and scope changes need your agreement.

## 🗂️ A memory you can open, read and version

| Piece | What it keeps |
| --- | --- |
| **Cards** | The agreed outcome, scope, acceptance criteria and user decisions. Each Card's folder is its stage on the board. |
| **Kanbans by module** | What's waiting, active, completed or cancelled, with a limit on work in progress. |
| **Rememory journal** | Decisions and publication milestones, linked to the Cards. |
| **Git** | The exact revision that was checked and the history of what shipped. |
| **Guardrails** | Your rules and permissions for the agent, stored in `GUARDRAILS.md`. |

The agent keeps these records as part of the work. You can drive the project in plain language without moving Cards by hand.

Codex reads `AGENTS.md`. Claude Code follows the same entry point through `CLAUDE.md`. A new session can recover the recorded work and its next authorized action. The conversation itself stays in the application where it happened.

No background service runs. A session does the work, and the agent follows the repository instructions within its host's permissions.

## 🔥 Built with itself. Shipped for real.

**0.1.49 is the first version its creator calls stable.**

This repository uses Kanban Rememory to build Kanban Rememory. During development, five Cards went from request through merge in one pass, without intervention during execution. The owner never had to move a Card by hand.

That's the result KR is aiming for: an agent that carries agreed work through to a checked delivery, with a record you can inspect and a place to resume tomorrow.

## Install it in your repo

### 1. Bring a Git repository

You'll need:

- **Git** and **Python 3.9 or later**.
- An existing repository on **`main`**, with a clean checkout.
- A remote named **`origin`**, with a **`main` branch you can read and push to**.
- A repository-aware agent such as **Codex or Claude Code**.

The installer checks these prerequisites. It does not create the repository, branch or remote for you.

### 2. Grab two files

Download these files from this repository and put them **at the root of the repo you want to equip**:

- [**INSTALL.md**](dist/INSTALL.md) — the procedure your agent follows. Save the file contents as `INSTALL.md`.
- [**kanban-rememory-kit-0.1.49.zip**](dist/kanban-rememory-kit-0.1.49.zip) — the installation kit.

Your target repository should look like this:

```text
your-repo/
├── .git/
├── INSTALL.md
├── kanban-rememory-kit-0.1.49.zip
└── … your existing project files
```

Keep exactly one `kanban-rememory-kit-*.zip` there. Leave it zipped; the agent handles extraction. The two downloaded files are setup inputs: don't commit them.

### 3. Give your agent the keys

Open Codex or Claude Code **in that target repository** and say:

```text
Follow INSTALL.md.
```

The agent checks the repo and presents an installation plan. It asks for your project name, modules, workflow, work-in-progress limit, timezone, Git permissions and working folder (`project` by default). It previews the configuration and waits for your approval before applying it.

The installation adds:

| Path | Purpose |
| --- | --- |
| `kanban-rememory/` | The workflow, tools, templates and guides. |
| `kanban-rememory.json` | Your project's configuration. |
| `project/` or your chosen folder | The module boards and Rememory journal. |
| `AGENTS.md` and `CLAUDE.md` | The agent entry points. |
| `GUARDRAILS.md` | Your rules and approved permissions. |

It also adds the required ignore and line-ending rules. Existing root instruction files are preserved, with missing template lines appended where required; an existing `GUARDRAILS.md` is kept, with any permissions you approve added during setup.

**Setup commits locally on `main`. It never pushes.**

### 4. Check that the memory works

When the installer asks, open a fresh chat in the target repository. Confirm it recognizes the Orchestrator, the boards and the next authorized action. Report the result in the installation chat so setup can finish recording its checks.

The agent then offers to remove `INSTALL.md` and the ZIP. You're ready to give it a real task.

Already using KR? The same procedure upgrades the kit while preserving your project records and settings, apart from the installed kit version. It refuses a downgrade.

## 💬 Your first mission

Try something small enough to judge:

```text
Add a contact form with name, email and message.
Show a confirmation after submitting it.
Work directly on main. Show me what you checked
and ask me before you publish.
```

The agent records the scope and acceptance criteria, builds the agreed result and runs the relevant checks. You review the verified revision and decide whether it ships.

Tomorrow, or in another agent, pick it up with:

```text
Resume work in this repository. Recover the current phase and Card,
check what has really been verified and continue the next authorized
action. Ask me only for missing decisions.
```

Want an alert when your attention is needed or the work is delivered? **Remy**, the optional Slack or Telegram notifier, can send you back to the right chat. Follow the [Slack setup guide](kanban-rememory/documentation/slack-setup.md) or the [Telegram setup guide](kanban-rememory/documentation/telegram-setup.md).

## 📚 Go deeper

- [User guide](kanban-rememory/documentation/guide.md) — give work, approve changes and resume across sessions.
- [Orchestrator workflow](kanban-rememory/orchestrator/workflow.md) — the rules the agent follows.
- [Lean Specifications](kanban-rememory/documentation/lean-specifications.md) — keep the scope focused on the outcome.
- [Installation procedure](dist/INSTALL.md) — the complete install and upgrade instructions.

**Bring the idea. Keep the wheel. Let the repo remember.**
