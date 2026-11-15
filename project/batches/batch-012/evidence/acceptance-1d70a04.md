# KR Tester observations for 1d70a04

Candidate `1d70a04e39b39492bfac502045095cede7cc5317` from the Developer's verified handoff. The five candidate test drivers were rerun in their disposable fixtures: 42 board, 6 delivery, 4 publication, 17 role and 23 Telegram checks passed. App-specific probes used a synthetic project. Product code, user records and product remotes were not used for fixture writes or publication.

## MM-04 — Native role invocations

Four fresh invocations in Claude Code and four in Codex CLI read the synthetic manifest, global memory and selected module A memory in order. The fixture held a distinct B marker, which did not appear in the startup results. The named Claude roles produced three expected denials and three expected allowed operations. The allowed Developer change affected the synthetic shared source. No forbidden write changed the fixture. Codex sessions were read-only and the role policy remained advisory, as was the unnamed Claude Orchestrator policy. These probes do not test skill discovery or add host-level enforcement.

Candidate copies used by the hook:

- `role-limit-hook.py` SHA-256 `da4532c112f9c4c98e6ecd7d73567421a6e242b9a8d06c94e4550ddbc63c662a`.
- `kanban/project.py` SHA-256 `62b62db683f2b80a4ab146ab73c68a403565531359808c53312421236e70b39d`.

Fixture logs and verification output: `/private/tmp/kr-mm04-uat.7Ei0eN/summary.py` and neighboring synthetic traces.

## MM-05 — Publish and retain separate journals

Both synthetic modules published accepted fixture deliveries to a local bare origin. Fixture closing commits were `c7387ecfbab6f99234190cf705891d743c5ccfd1` for A and `c2002c2e3b733f22062ee79db895c54ea833f00d` for B. Concurrent writes recorded one local entry per module and two global entries with the exact closing commits and valid local evidence links. Retrying A's entry did not change journal bytes. Each slot was released after its closure. Fresh startup context was checked independently in the native probes.

## MM-08, MM-09 and MM-15 — Additional fixture observations

- MM-08 used a claimed A Batch with two associated Cards. The unassigned helper was refused when attempting an active move. The owner moved the first Card and the separate Card WIP limit refused the second.
- MM-09 attempted a different-owner takeover while the original owner's runtime check was still alive. The takeover failed. A fresh process with the original owner and base recovered the recorded checkpoint. The delivery suite also refused a pickup from a separate clone.
- MM-15 preview left the project tree unchanged. The activation command refused a legacy project with an active Card. After that Card was closed in the fixture, explicit activation preserved the exact paths and bytes of a frozen Card, an approved Spec and the closed Batch description and report. The two new module slots were empty.

The separate [MM-12 stale acceptance case](mm-12-stale-acceptance.md) is a technical KO. This evidence does not record a decision on the overall Batch.
