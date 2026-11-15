# Your decisions and responsibilities

You own the project and make its product and delivery decisions. In a normal project chat, KR Orchestrator helps clarify the need, records your answers and routes work to the responsible agents. You do not need to maintain the framework's files.

## Decide what should be delivered

Explain the desired outcome, priorities and constraints. Review the proposed scope using the [Lean Specifications approval test](lean-specifications.md#the-approval-test). For a Batch, approve the exact Specification revisions and their priority.

Make the intended next step clear: preparing a proposal, approving its scope, authorizing execution and publishing are distinct. One instruction can grant several permissions together, and recorded standing authorization remains usable. Changes to the agreed workflow or role definitions also need your approval.

## Review the result

KR Tester runs eligible acceptance checks and guides the cases that need your action or judgment. Choose OK or KO for each human case. After KO, explain the observed behavior and provide a screenshot when relevant, or say it is unavailable. The agent records your answer against the exact candidate.

After reviewing the results and report, explicitly accept or reject that tested revision. Individual case verdicts do not accept the Batch. Required tests must pass and blocking debt must be resolved before acceptance; decide explicitly whether to defer any remaining nonblocking defect. The [acceptance guide](test-and-accept-a-batch.md) explains correction and outstanding tests.

## Leave recordkeeping to the agents

KR Writer prepares Specifications and backlog Cards. KR Developer maintains execution records, technical evidence and Rememory, and performs authorized Git operations. KR Tester records acceptance results. You can inspect the board and request changes through conversation; the agents record them within their roles.

Answer requests in the original project chat. Optional Telegram alerts point you back there; a Telegram reply does not authorize work or record a delivery decision. No particular editor or document viewer is required.

## When work waits

A delivered Batch waits for its required acceptance checks and your decision. Another Batch can start after closure. Queued standalone tasks become eligible at delivery within the work-in-progress limit and must preserve the acceptance candidate.

If a defect blocks acceptance, authorize correction of the agreed behavior in the open Batch or reject the delivery. Rejection preserves the debt and tests still owed. Later work carries those obligations forward without rewriting closed records.
