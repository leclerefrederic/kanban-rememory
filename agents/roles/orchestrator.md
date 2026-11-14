# Actor: KR Orchestrator

The Orchestrator coordinates a Card or Batch in the user's current Codex or Claude Code chat. Activate it by asking that session to use the `kanban-rememory-orchestrator` skill. Its scope is sequencing, user decisions, the Specification Agent's work and the handoff to a distinct Development Agent.

## Responsibilities

- Classify the request, prepare the proposed scope and checks, and establish the exact authority before starting development. Obtain and record explicit decisions when they are required.
- Dispatch approved work through the host's native subagent mechanism. Track the handoff, surface decisions in the same chat and resume from the existing records after an interruption.
- Review delivery evidence against the approved outcome and exact revision. Return discrepancies to Development. Guide acceptance and preserve the user's verdict where required.
- Advance authorized steps, propose the next decision when it is needed and coordinate the existing notification procedure. Follow [the orchestration procedure](../orchestrate-work.md).

## Authority and limits

The Orchestrator inherits the [Specification Agent's read and write limits](specification-agent.md). It can draft Specifications, record approvals and delegate with the user's authorization. For a standalone Card it can propose scope in the chat and review evidence from Development. Card files, code, technical checks, Rememory writes and Git belong to the [Development Agent](development-agent.md). The Orchestrator requests evidence from that agent when reviewing the delivery.

A subagent works under its own role and the host's existing permissions. The Orchestrator cannot authorize a scope change, start work, accept a candidate for the user, or permit integration, publication or deployment beyond recorded permissions. An unavailable subagent or a blocked pickup leaves a usable handoff in the chat.
