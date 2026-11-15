---
type: tests
id: "Batch-011-Tests"
batch: "Batch-011"
---

# Acceptance tests

- Tested commit: `7b2e8b4d6ddb241a68bd2b939ed96386a18079ab` (published and verified on `origin/codex/batch-011`; same product bytes on integrated main).
- Environment or prerequisites: Start a fresh standard Codex or Claude Code session in the ordinary Kanban Rememory project on integrated main without naming a role or skill. Use the host’s normal project-trust and native subagent settings. Target only the designated fixture for disposable work. Fixture directories:
  - TEST-01: `/private/tmp/kr-batch011.lCSql2/uat/codex-card`
  - TEST-02: `/private/tmp/kr-batch011.lCSql2/uat/codex-batch`
  - TEST-03: `/private/tmp/kr-batch011.lCSql2/uat/claude-card`
  - TEST-04: `/private/tmp/kr-batch011.lCSql2/uat/claude-batch`
  - Each fixture starts on main with an independent local bare origin; never push test artifacts to the real remote. The Claude fixtures include the optional named-role hook.
- Technical evidence:
  - 33 board checks and 22 Telegram checks passed; approval verification, board validation, skill sync and scoped diff checks passed. The board tests cover covered Writer backlog writes, denial of active and closed Card writes, Tester path limits, named-agent installation and compatibility.
  - Codex CLI 0.169.0 and Claude Code 2.1.323 loaded the default role in fresh read-only probes without naming the skill. An explicit Claude Tester session retained its assignment and recognized that it cannot close a Batch. These are technical probes; real interactive journeys are the four separate UAT cases.
  - Checked all 83 candidate startup, role, agent and tool files against each clean fixture. Each fixture adds an explicit safety boundary to AGENTS.md and keeps a local-only origin. No case verdict is assigned.

| ID | Specifications | Action | Expected result | Verdict | Tested revision | Observation or evidence |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-01 | SPEC-017, SPEC-018 | Codex: execute a disposable standalone Card from the normal startup entry point. | Default Orchestrator, Writer prepares a backlog Card, Developer starts only after approval, uses the same Card, verifies and reports in the original chat. | OK | `7b2e8b4` | User verdict OK on 2026-11-15. Fixture commit `3474ade`; see scenario evidence below. |
| TEST-02 | SPEC-017, SPEC-018, SPEC-019 | Codex: execute a disposable Batch from the normal startup entry point. | Default Orchestrator coordinates Writer, Developer and Tester; explicit roles are preserved, Tester checks the exact delivery and guides the user, and closure follows the user's verdict. | OK | `7b2e8b4` | User confirmed the full Codex Batch journey on 2026-11-15. |
| TEST-03 | SPEC-017, SPEC-018 | Claude Code: execute the same standalone Card journey in its own fixture. | Same expected behavior as TEST-01 using a real Claude Code handoff. | OK | `7b2e8b4` | User confirmed the Claude Code standalone Card journey without debt on 2026-11-15. |
| TEST-04 | SPEC-017, SPEC-018, SPEC-019 | Claude Code: execute the same Batch journey in its own fixture. | Same expected behavior as TEST-02 using real Claude Code handoffs. | OK | `7b2e8b4` | User confirmed the Claude Code Batch journey without debt on 2026-11-15. |

## Startup and actions by case

Record the exact integrated main revision and fixture startup instructions before each journey. Record role identity and approved scope at each handoff. Cover permission, failure and compatibility assertions in technical checks or as observations within these journeys, without expanding the four UAT cases.

### TEST-01 — Codex Desktop standalone Card

Open a fresh standard Codex Desktop chat in the regular Kanban Rememory project on integrated main `380e8bb`, containing candidate `7b2e8b4`. Do not name a skill or role. The disposable work target is `/private/tmp/kr-batch011.lCSql2/uat/codex-card` on `main`; its origin is a local bare repository.

1. Ask the session to prepare a Card in the disposable target to create a root `status.txt` containing exactly the five bytes `ready`, and to wait before development.
2. Check that the session takes the KR Orchestrator role, KR Writer prepares a backlog Card with its scope and checks, and development does not begin.
3. Approve the displayed scope and authorize development in the same chat. KR Developer must take the same Card in the disposable target, perform the work and verify the file. If publishing as part of the fixture rules, publish exclusively to its local origin.
4. Stop after the Orchestrator returns verification evidence and the Card result. Record the User's OK or KO against the integrated candidate.

Observed on 2026-11-15 in the Codex Desktop workflow: KR Writer prepared the scratch Card before approval; the User then authorized development. A native KR Developer subagent took the same Card and completed it. Fixture commit `3474adef1dcf4e291f431fd50da58519360954fa` contains exactly the file, completed scratch Card and journal. The exact 5-byte check and board validation passed. The fixture's bare local origin confirms the commit. User verdict: OK on 2026-11-15.

### TEST-02 — Codex Desktop Batch

Open a new standard Codex Desktop chat in the normal project on integrated main `380e8bb`, containing candidate `7b2e8b4`. Do not name a skill or role. Use `/private/tmp/kr-batch011.lCSql2/uat/codex-batch` for all disposable work and its local bare origin for any test publication.

1. Ask for a draft Specification and a one-Specification Batch for a root `batch-status.txt` containing exactly the five bytes `ready`. Verify default Orchestrator and Writer preparation before approval.
2. Approve that exact scope and authorize development in the same chat. Observe the Developer handoff, dedicated branch, technical checks and exact delivered revision.
3. Observe the Tester handoff and a guided acceptance check against that revision. Give the disposable Batch its own verdict, then verify that closure follows it. Return OK or KO for this UAT journey separately.

### TEST-03 — Claude Code standalone Card

Open a fresh normal Claude Code session in the regular Kanban Rememory project on integrated main `380e8bb`, containing candidate `7b2e8b4`. Do not name a role or skill. Use only `/private/tmp/kr-batch011.lCSql2/uat/claude-card` and its own bare local origin for the disposable work. Confirm the target before authorization.

1. Ask for a Card to create root `status.txt` containing the five bytes `ready` without a newline. Ask the session to wait before development.
2. Verify default KR Orchestrator and that KR Writer prepares a backlog Card without starting development. Approve the exact scope and authorize development in the same session.
3. Verify that a Claude Code Development Agent takes that same Card, verifies the exact bytes and returns the result to the original chat. Stop and record the User's OK or KO.
