# Report a defect

Tell your agent when delivered behavior differs from what was agreed. Every observed defect is debt, including a visual problem noticed during a test that otherwise passes. The agent records it; you do not have to create a Card or edit the report.

## Describe what happened

Share the version or build you used if you know it, the steps that led to the problem, what you expected and what happened instead. Include the exact error and a screenshot when available. Say whether it prevents the work, affects only one path or has an acceptable workaround.

> In the candidate we are testing, selecting the repository opens a blank window and the app stops responding. I expected the creation form. I cannot continue the remaining cases. Here is a screenshot.

If you cannot identify the build or reproduce the problem, say so. The agent records that uncertainty and helps establish the evidence; it must not invent a cause or mark the problem resolved.

## During Batch acceptance

Give the verdict for the behavior the current case checks. A failed requirement is KO. A separate cosmetic defect can accompany an OK result; it still becomes debt.

After KO, the agent asks why and requests a screenshot. It links the supplied evidence to the case, records severity and identifies which other tests are blocked. If the screenshot is unavailable, that fact remains in the result. Independent cases can continue.

The [Batch acceptance guide](test-and-accept-a-batch.md) explains severity, correction and the conditions for acceptance. A blocking defect requires an authorized correction of the agreed behavior in the open Batch, or a rejection decision. The approved scope stays fixed.

## After a delivery has closed

Identify the earlier delivery when possible. Its report remains historical evidence. In a project using Batches, the agent prepares the corrective Specification and proposed delivery, carrying forward the original defect reference and any required tests still due. A new report records the verified resolution without rewriting the closed source report.

The defect describes what is wrong and what must be restored. Development Agent's Cards track the work needed to fix it independently. Rewriting the defect as a task does not resolve the debt.

## Distinguish a correction from a new idea

A correction restores agreed behavior. A request for different behavior goes through scope approval. If the difference is unclear, the agent asks before implementation. You can propose improvements alongside a defect, but they stay separate from the authorized correction.

Debt closes when the correction has been verified and included in the accepted delivery. Merely writing it down, writing code or accepting a delivery with an explicit nonblocking deferral does not resolve it.

See the [example report](examples/batch-report.md) for a defect followed through correction and closure, or [assign a task](assign-a-task.md) for a new request.
