# Resume work

Use this guide after an interrupted session, a change of agent or a break. The records let the agent recover the work without asking you to reconstruct the conversation.

## Ask for recovery

Identify the repository and, if known, the Card.

> Resume work in this repository. Recover the current Card, check what has actually been verified, and continue the next authorized action. Ask me only for decisions that are still missing.

If you only want a status report, say so.

## What the agent establishes

- The active Card, its approved scope and current stage.
- The revision involved and the latest verified result.
- Any blocker or check still outstanding.
- The next action and whether it is already authorized.

The agent checks files and Git state against the Card. It reports a conflict before affected work continues. Existing approval is reused where it still covers the action.

## Continue from the actual stopping point

| Work stopped… | What happens next |
| --- | --- |
| During implementation | The agent resumes the same Card and branch, keeping completed checks visible. |
| On a question or dependency | It explains the blocker and what clears it. |
| Waiting for merge approval | It shows the verified revision again; a changed candidate needs new approval. |
| During publication | It verifies and finishes the interrupted publication before new work. |
| After completion | The completed Card stays history; new work gets a new Card. |

Recovery is performed by an agent session; no background service runs. Continue with [assign a task](assign-a-task.md) for new work.
