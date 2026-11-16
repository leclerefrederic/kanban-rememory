# User guide

Kanban Rememory keeps your project's agreed work, its state and its evidence in the repository, so any agent session can resume it. You describe outcomes and make the decisions. The agent, called the Orchestrator, writes the records and does the authorized work. You never need the commands or the file formats.

## What the records mean

- **Card**: one outcome, with its scope, acceptance criteria, decisions and delivery evidence. Its folder on the module's Kanban is its stage: Backlog, Development, Completion or Cancellation, plus any stage your workflow adds, such as a review. A Card in progress can be waiting or blocked. Blocked work stays visible and counts toward the work-in-progress limit.
- **Module**: each part of the project has its own Kanban. Work without a natural owner, including a change that spans modules, goes to `misc`.
- **Rememory**: the journal in `project/rememory/`, one file per day, with decisions and each publication linked to its Cards.
- **Phase**: the agent works on one or more Cards, directly on `main` or on a release branch, and asks for your approval once, before publishing.

Completed Cards are history. A correction or a new idea gets a new Card that refers to the old one.

## Start a project

Tell the agent which repository to use and that you want Kanban Rememory. It checks the prerequisites, Git and Python 3.9 or later. It groups independent setup questions and suggests defaults. If one decision depends on another, it asks for the first decision before following up. Setup covers modules, workflow, the work-in-progress limit, the timezone, what counts as delivered and Git permissions. Developing, accepting a delivery and publishing are separate permissions; one instruction can grant several. The agent proposes the setup, applies it after your approval and checks it. If the repository already uses Kanban Rememory, the agent resumes instead.

## Give work

Describe the result, the constraints that matter and how to check success. Add an example, a screenshot or a mockup when it helps. For example:

> Fix the broken links in the setup guide without changing the instructions. Check that every local link opens the right section. You can execute this and publish under the project's permissions.

Say what you want next; the wording is free:

| You want to… | You can say |
| --- | --- |
| Explore first | "Compare the options and recommend one before implementing." |
| Keep it for later | "Put this in the backlog; do not start it." |
| Start agreed work | "Execute this within the agreed scope." |
| Change priority | "Prioritize this and tell me what it means for the work in progress." |

The agent looks for an existing Card, records the scope and your decisions, and asks about any ambiguous behavior instead of inventing it. Every requirement should pass the [approval test](lean-specifications.md#the-approval-test).

## Review and approve

You can also run the tool yourself: `python3 orchestrator/tools/kr.py show` lists the boards, the active phase and its next action; `python3 orchestrator/tools/kr.py versions` lists the published versions.

Once authorized, the agent implements, runs the relevant automated checks and fixes what it can within scope. It hands control back only when it needs a decision or an action from you, or when the work is done. Before starting, the agent asks whether to work directly on `main` or in a release. A release groups Cards on one branch, and publishing it raises the version number and tags it `vX.Y.Z` (patch by default; tell the agent if you want minor or major). Work on `main` commits there and creates no tag. Before merging into `main`, it shows you the verified revision, what was checked and anything that merging or pushing triggers, such as a deployment. Then it waits for your explicit approval. A changed revision needs a new approval. If your request already says to merge, for example "do it and merge", that approval covers the verified result and the agent publishes without asking again. It asks again when a check fails or the change goes beyond what you asked. Checks that need you are done on that exact revision, and the agent records your verdict.

## Resume work

After an interruption, a change of agent or a break, ask:

> Resume work in this repository. Recover the current phase and Card, check what has really been verified and continue the next authorized action. Ask me only for missing decisions.

The agent reports the active Card, the revision and the latest verified result, any blocker and the next action. It compares the files and the Git state with the Card and reports any conflict before continuing. Approvals that still cover the action remain valid. Work waiting for your merge approval is shown to you again, and an interrupted publication is finished first. No background service runs: a session does the work.

## Report a defect

Tell the agent when delivered behavior differs from what was agreed: the version if known, the steps, what you expected, what happened, and the exact error or a screenshot. Say whether it blocks you. A defect in work in progress sends that Card back to rework; a defect in completed work gets a new Card. A correction restores the agreed behavior, while a different behavior goes through scope approval. The defect stays open until its correction is verified.

## Codex and Claude Code

Both use the same records: Codex reads `AGENTS.md`, and Claude Code reads it through `CLAUDE.md`. A conversation does not carry from one application to another, so name the repository and, if known, the Card, and ask the new session to resume. No host enforces these instructions: they rely on the agent and on each product's own sandbox and approvals.

## Telegram alerts

Telegram is optional. Remy sends **Action required** when the agent needs you, including for a merge approval, and **Work completed** once the agreed outcome is verified, nothing else. Each alert names the project, the Card and the chat to return to. You answer in that chat, never in Telegram. Set it up with the [Telegram guide](telegram-setup.md).
