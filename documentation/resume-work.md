# Resume work

Use this guide after an interrupted session, a change of agent or a break in the project. The records should let the agent recover the work without asking you to reconstruct the conversation.

## Ask for recovery

Identify the repository. If you know the relevant Card or Batch, mention it; otherwise the agent reads the current board and delivery records.

> Resume work in this repository. Recover the current task or Batch, check what has actually been verified, and continue the next authorized action. Ask me only for decisions that are still missing.

If you only want a status report, say so. The agent should distinguish recovering context from starting new work.

## What the agent should establish

- The active task or Batch, its approved scope and current state.
- The candidate or revision involved and the latest verified result.
- Any blocker, open debt or required test still outstanding.
- The next action and whether it is already authorized or needs your decision.

The agent checks the files and Git state against the records. A conflict between them is reported before affected work continues. Existing approval is reused where it still covers the action; resumption does not require you to approve the same work again.

## Continue from the actual stopping point

| Work stopped… | What happens next |
| --- | --- |
| During implementation | Resume the existing task or Batch and its branch, keeping completed checks and remaining work visible. |
| On an unresolved question or dependency | Explain the blocker and the decision or event needed to clear it. |
| With a delivered candidate | Resume acceptance on that identified candidate, starting with the outstanding or affected cases. |
| After a blocking acceptance failure | Follow the recorded correction request within the same open Batch when authorized, then test the new candidate. |
| During closure | Verify and finish the interrupted closure before starting another Batch. |
| After closure | Use the closed records as history; track new work separately. |

Passed tests remain associated with their original revision. A correction does not erase earlier failures or automatically validate cases that could not run. Closed Batches and completed Cards are not reopened to record new work.

The agent leaves a concise journal entry and the next action when handing work over. Recovery is performed by the agent session; it does not imply that a background scheduler is running.

Continue with [assign a task](assign-a-task.md) for new work, or [test and accept a Batch](test-and-accept-a-batch.md) for a delivered candidate.
