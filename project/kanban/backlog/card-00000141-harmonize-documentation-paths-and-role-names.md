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

## Proposed scope

- Inventory the entire repository documentation corpus: root entry points, reader documentation, agent rules and procedures, roles, host adapters, skills, templates, examples and project records/references. Account for every area in a coverage map; distinguish active material that may be refactored from frozen historical evidence. The examples below illustrate problems to investigate throughout the corpus and do not bound the scope.
- Inventory active documentation paths, role names, links and entry points. Examples include `agents/roles/` versus `agents/claude/agents/`, and `development-agent.md` / `specification-agent.md` versus the current Developer / Writer names. These folders may serve different purposes; do not merge them merely because they contain similar names.
- Review the mixed contents at the root of `agents/`: distinguish agent rules (`guidelines`), operational procedures (`actions`) and configuration/adoption (`setup`). Propose clear placement criteria, including documents spanning categories, and a small navigable root. These are the User's requested categories; the exact target paths belong in the before/after proposal.
- Audit responsibility boundaries within each document, not only folder names. Each document must have one clear purpose and delegate related procedures through links rather than repeat their normative instructions. Inventory duplicated rules, overlapping sequences and contradictory prerequisites; propose merging, splitting or referencing only where needed.
- Specifically review `configure-a-project.md` and `install-in-a-project.md`: both currently describe workflow preview/application/validation and project conventions. Installation says workflow agreement precedes installation, while step 2 performs that agreement after copying files. Clarify the single sequence and which document owns each step; this is an observed ambiguity, not evidence of an execution failure. Coordinate this boundary with SPEC-020 rather than creating two competing installation rewrites.
- Propose a consistent naming convention and before/after path map for the repository documentation, including common role definitions and host-specific adapters. Prefer `developer` and `writer` for the renamed roles, consistent with Orchestrator and Tester. Resolve naming, placement, responsibility, duplication and consistency issues across the corpus under the approved mapping; the scope is not limited to the examples already reported.
- Identify dependent launch IDs, role checks, skills, installation/synchronization procedures, templates, links and tests before renaming anything. Make the selected renames and reference updates together after approval, preserving role permissions and host behavior.
- Define how upgrades preserve customized host files and how existing references remain usable. Preserve completed Cards, closed Batch records and approved Specifications as historical evidence; propose compatibility handling for their old references rather than silently rewriting them.
- Coordinate with draft SPEC-020 (installation review) and completed CARD-00000138 (short role skill names). This Card owns the repository-wide documentation audit and refactoring, including content responsibilities and coherence. Identify overlap with SPEC-020 and propose how to consolidate that work so installation documentation is not excluded or rewritten twice. New product behavior and changes to role permissions require separate approval.

## Acceptance criteria

- [ ] A repository-wide coverage map accounts for every documentation area, its documents and findings, with justified historical exclusions; the audit is not limited to the User's examples.
- [ ] Inventory and before/after mapping identify every proposed rename, its rationale, affected consumers and any compatibility exception; the User approves the concrete implementation scope.
- [ ] A document-responsibility map identifies normative sources, overlaps and contradictions. Every active document in the audited corpus has a clear purpose; shared rules and procedures have one authoritative definition.
- [ ] The installation/adoption example has one coherent order for prerequisites, choices, approval, copying/configuration and validation; no duplicated commands or approval steps create competing instructions.
- [ ] Active documentation and entry points use the agreed naming convention. Remaining legacy names are explicitly justified by history or compatibility.
- [ ] The proposed `agents/` layout separates guidelines, actions and setup with clear placement criteria; the root has a documented purpose and does not remain a miscellaneous collection.
- [ ] Shared roles and host adapters are distinguishable without duplicating their source-of-truth responsibilities.
- [ ] Links, role checks and host launch/discovery paths still resolve after migration; applicable checks pass against the exact delivered revision.
- [ ] Fresh installation and upgrade checks cover the affected Codex and Claude Code paths, preserve unrelated/customized settings and verify current role discovery.
- [ ] Historical references remain usable, with no unapproved edits to frozen records or changes to role permissions.

## Execution and evidence

- State: waiting
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-15 — While CARD-00000135 was in Development, the User requested a backlog Card for documentation refactoring, citing the shared/Claude role folders and legacy development-agent/specification-agent filenames. Backlog preparation only is authorized by this request; implementation awaits the concrete naming/migration proposal.

- 2026-11-15 — User additionally identified the root of `agents/` as a mixture of guidelines, actions and setup. Added category separation and root navigation to the proposed refactoring scope.

- 2026-11-15 — User required coherent responsibilities inside each file and specifically questioned overlap/contradictions between configure-a-project and install-in-a-project. Read-only review confirmed repeated workflow setup/validation and ambiguous ordering; added responsibility mapping and reconciliation to the proposal scope.

- 2026-11-15 — User clarified that the scope is global to the repository. Role paths, the agents root and installation/adoption guides are illustrative examples only. Expanded the outcome, coverage inventory and acceptance criteria accordingly.
