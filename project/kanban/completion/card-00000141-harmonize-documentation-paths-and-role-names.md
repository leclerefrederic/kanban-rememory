---
type: card
id: "CARD-00000141"
batch: null
specifications: []
---

# CARD-00000141 — Refactor repository-wide documentation structure and responsibilities

- Owner: KR Developer
- Dependencies: Complete CARD-00000135 before execution under the WIP limit. Agree on the concrete naming and migration plan before implementation.

## Expected outcome

Users and agents can navigate and apply the entire repository documentation through coherent names, clear document responsibilities and consistent instructions. The audit and refactoring cover the repository-wide documentation corpus, not only role files, the agents root or installation guides. Each document has a clear purpose, each shared rule has an authoritative source, and related procedures compose without duplication or contradictions.

## Agent-first design principle

The User explicitly confirmed that `agents/` is internal machinery for Codex and Claude Code, not human-facing reading material. Optimize for fast routing, minimal necessary context and unambiguous execution. Use concise operational instructions, explicit inputs/prerequisites, decisions, actions and expected outputs where useful. Remove repeated explanations and narrative that do not help an agent act. Keep human-facing explanations in `documentation/`; preserve binding constraints and exceptions. Brevity is measured by total task-reading cost and reliable execution, not just shorter files or more folders.

## Proposed scope

- Inventory the entire repository documentation corpus: root entry points, reader documentation, agent rules and procedures, roles, host adapters, skills, templates, examples and project records/references. Account for every area in a coverage map; distinguish active material that may be refactored from frozen historical evidence. The examples below illustrate problems to investigate throughout the corpus and do not bound the scope.
- Inventory active documentation paths, role names, links and entry points. Examples include `agents/roles/` versus `agents/claude/agents/`, and `development-agent.md` / `specification-agent.md` versus the current Developer / Writer names. These folders may serve different purposes; do not merge them merely because they contain similar names.
- Review the mixed contents at the root of `agents/`: distinguish agent rules (`guidelines`), operational procedures (`actions`) and configuration/adoption (`setup`). Propose clear placement criteria, including documents spanning categories, and a small navigable root. These are the User's requested categories; the exact target paths belong in the before/after proposal.
- Audit context cost across all Markdown documents: record file sizes and estimated token counts, and the cumulative required reading for representative agent tasks (startup, intake, development, acceptance, installation and recovery). The User flagged a 15 KB file as a concern, not an approved hard limit. Propose an evidence-based size/reading budget and flag oversized or repeatedly loaded content for review. Keep concise entry points and load detailed task-specific instructions only when needed; avoid fragmentation that forces more files to be read or hides binding rules.
- Audit responsibility boundaries within each document, not only folder names. Each document must have one clear purpose and delegate related procedures through links rather than repeat their normative instructions. Inventory duplicated rules, overlapping sequences and contradictory prerequisites; propose merging, splitting or referencing only where needed.
- Specifically review `configure-a-project.md` and `install-in-a-project.md`: both currently describe workflow preview/application/validation and project conventions. Installation says workflow agreement precedes installation, while step 2 performs that agreement after copying files. Clarify the single sequence and which document owns each step; this is an observed ambiguity, not evidence of an execution failure. Coordinate this boundary with SPEC-020 rather than creating two competing installation rewrites.
- Propose a consistent naming convention and before/after path map for the repository documentation, including common role definitions and host-specific adapters. Prefer `developer` and `writer` for the renamed roles, consistent with Orchestrator and Tester. Resolve naming, placement, responsibility, duplication and consistency issues across the corpus under the approved mapping; the scope is not limited to the examples already reported.
- Identify dependent launch IDs, role checks, skills, installation/synchronization procedures, templates, links and tests before renaming anything. Make the selected renames and reference updates together after approval, preserving role permissions and host behavior.
- Define how upgrades preserve customized host files and how existing references remain usable. Preserve completed Cards, closed Batch records and approved Specifications as historical evidence; propose compatibility handling for their old references rather than silently rewriting them.
- Coordinate with draft SPEC-020 (installation review) and completed CARD-00000138 (short role skill names). This Card owns the repository-wide documentation audit and refactoring, including content responsibilities and coherence. Identify overlap with SPEC-020 and propose how to consolidate that work so installation documentation is not excluded or rewritten twice. New product behavior and changes to role permissions require separate approval.

## Acceptance criteria

- [x] A repository-wide coverage map accounts for every documentation area, its documents and findings, with justified historical exclusions; the audit is not limited to the User's examples.
- [x] Inventory and before/after mapping identify every proposed rename, its rationale, affected consumers and any compatibility exception; the User approves the concrete implementation scope.
- [x] The audit reports Markdown sizes, estimated tokens and cumulative reading by representative agent journey. A proposed readability/context budget is reviewed with the User; large files (including around 15 KB) have an explicit keep/simplify/split rationale.
- [x] `agents/` contains concise execution-oriented instructions for Codex and Claude Code, with effective routing and task-relevant loading. Human pedagogy and redundant narrative are removed or placed in reader documentation; permissions and mandatory rules remain explicit.
- [x] The revised reading paths are concise and task-relevant, with before/after context-cost evidence. Splitting preserves discoverability and all binding rules without forcing every agent to load every detail.
- [x] A document-responsibility map identifies normative sources, overlaps and contradictions. Every active document in the audited corpus has a clear purpose; shared rules and procedures have one authoritative definition.
- [x] The installation/adoption example has one coherent order for prerequisites, choices, approval, copying/configuration and validation; no duplicated commands or approval steps create competing instructions.
- [x] Active documentation and entry points use the agreed naming convention. Remaining legacy names are explicitly justified by history or compatibility.
- [x] The proposed `agents/` layout separates guidelines, actions and setup with clear placement criteria; the root has a documented purpose and does not remain a miscellaneous collection.
- [x] Shared roles and host adapters are distinguishable without duplicating their source-of-truth responsibilities.
- [x] Links, role checks and host launch/discovery paths still resolve after migration; applicable checks pass against the exact delivered revision.
- [x] Fresh installation and upgrade checks cover the affected Codex and Claude Code paths, preserve unrelated/customized settings and verify current role discovery.
- [x] Historical references remain usable, with no unapproved edits to frozen records or changes to role permissions.

## Execution and evidence

- State:
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker: none.

## Audit proposal

- Baseline: `308b747c82dbe290bbd14a53d791be90c2949646` on main, matching the locally recorded origin/main at audit start.
- [Audit and findings](../../rememory/evidence/card-00000141-audit.md), [migration plan awaiting approval](../../rememory/evidence/card-00000141-plan.md).
- Detailed evidence: [266-path inventory](../../rememory/evidence/card-00000141-inventory.csv), [Markdown link consumers](../../rememory/evidence/card-00000141-link-consumers.csv), [technical consumers](../../rememory/evidence/card-00000141-technical-consumers.csv), [journey readings](../../rememory/evidence/card-00000141-journeys.csv), [proposed budgets](../../rememory/evidence/card-00000141-target-budgets.csv).
- Audit only: all 62 active non-project documents read, active Cards reviewed, historical evidence scanned and preserved, draft Specifications assessed through Writer handoff. Proposed before/after readings are estimates awaiting implementation; no product refactoring or native-host behavior test has occurred.
- Live board/skills checks remain affected only by pre-existing deleted Runner documentation/VERSION. No unrelated edits were restored. Refactoring, implementation verification, acceptance and closure remain outstanding.

## Verified delivery

- User approved the concrete plan and execution; implementation candidate `98ac495347b3da93b71aa449c45f43656e131b30` on `codex/card-00000141-docs`.
- [Verification and limits](../../rememory/evidence/card-00000141-verification.md): 36 board, 14 migration and 22 Telegram tests passed on the exact candidate; six adoption checks cover SPEC-020 plus frozen content/ACLs. Thirty-three obligations were reviewed as content, not counted as execution tests.
- [Measured files](../../rememory/evidence/card-00000141-measured-files.csv) and [journeys](../../rememory/evidence/card-00000141-measured-journeys.csv): active documentation including compatibility falls 24.8%; representative reading falls 40–58%. Budget exceptions retain required protections and are recorded.
- Native [Codex](../../rememory/evidence/card-00000141-native-codex.md) startup and reported Tester delegation passed; native [Claude](../../rememory/evidence/card-00000141-native-claude.md) discovered/ran three current and two legacy identities, with 17 permitted Read/hook observations. Unit cases cover negative permissions; no pre-upgrade live-process resume, native Windows or real Telegram verification is claimed.
- Frozen records/resources and role ACLs remain byte-identical. Writer supplied SPEC-020 consolidation and draft terminology/link updates. Unrelated local deletions, draft SPEC-013 and graph output remain outside this change.
- Reviewed the complete diff, checks and flow in Development. CARD-00000128 still requires approved Specification scope; all Batches remain closed. No new work is started.

## History

- 2026-11-15 — While CARD-00000135 was in Development, the User requested a backlog Card for documentation refactoring, citing the shared/Claude role folders and legacy development-agent/specification-agent filenames. Backlog preparation only is authorized by this request; implementation awaits the concrete naming/migration proposal.

- 2026-11-15 — User additionally identified the root of `agents/` as a mixture of guidelines, actions and setup. Added category separation and root navigation to the proposed refactoring scope.

- 2026-11-15 — User required coherent responsibilities inside each file and specifically questioned overlap/contradictions between configure-a-project and install-in-a-project. Read-only review confirmed repeated workflow setup/validation and ambiguous ordering; added responsibility mapping and reconciliation to the proposal scope.

- 2026-11-15 — User clarified that the scope is global to the repository. Role paths, the agents root and installation/adoption guides are illustrative examples only. Expanded the outcome, coverage inventory and acceptance criteria accordingly.

- 2026-11-15 — User required Markdown to remain digestible within agent context windows and expressed concern about 15 KB files. Added corpus-wide file/token sizing and cumulative task-reading review; no hard size threshold is assumed.

- 2026-11-15 — User confirmed that agents/ is exclusively internal agent machinery, optimized for Codex/Claude navigation, consultation and execution rather than human exposition (“Voilà exactement”). Recorded agent-first efficiency as the governing design principle.

- 2026-11-15T11:29:29+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15 — User explicitly prioritized and authorized the global audit with GPT-6 Astra / xhigh and requested the migration plan before refactoring. KR Developer owns this single active Card; audit and evidence only are authorized. Refactoring, closure and publication await the concrete plan approval. Baseline: `308b747c82dbe290bbd14a53d791be90c2949646` on `main`, matching `origin/main`. Preserve unrelated workspace changes.

- 2026-11-15 — Completed the global audit and submitted the concrete mapping, responsibilities, preservation strategy, proposed reading budgets and verification matrix. One owning Developer remains in Development while the User reviews the plan. Notifications are coordinated with the Orchestrator after the question is posted in the original chat.

- 2026-11-15 — After the Orchestrator posted the approval question in the original Codex chat, KR Developer attempted one Telegram attention alert with task `Refonte documentaire du dépôt` and event `card141-migration-plan-v1`. The tool returned exit 2 and delivery could not be confirmed. No automatic resend; the decision remains in the original chat.

- 2026-11-15 — User approved the concrete plan and authorized execution: “Valider le plan et lancer le refactoring”. KR Developer continues the same Card on `codex/card-00000141-docs` in `/private/tmp/kr-card141-docs`, preserving the original workspace changes. The approved plan/CSV mapping, compatibility, SPEC-020 consolidation and verification matrix define the scope. No resend of the unconfirmed Telegram alert.

- 2026-11-15 — Completed the approved refactoring, verified candidate and evidence, reviewed flow and met all Card criteria. Close under the repository’s standing publication authorization; preserve the unrelated main-workspace changes.

- 2026-11-15T12:26:24+01:00 — Stage moved from `development` to `completion`.
