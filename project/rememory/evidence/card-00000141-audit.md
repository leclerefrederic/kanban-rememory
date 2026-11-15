# CARD-00000141 — Global audit, 2026-11-15

Audit authorized with GPT-6 Astra / xhigh; **no refactoring authorized yet**. Owner: KR Developer, one active Card. Baseline `308b747c82dbe290bbd14a53d791be90c2949646` (`main` = locally recorded `origin/main`). The plan and budgets are proposals, not implemented results.

## Coverage and method

[Inventory](card-00000141-inventory.csv): **266 Markdown paths**, comprising **264 present** files (736,255 UTF-8 bytes, about 184,064 tokens) and two pre-existing deletions. The snapshot excludes these audit outputs and uses the baseline bytes for the Card and daily journal changed by audit pickup. Tokens use `ceil(bytes / 4)`, not a model tokenizer.

| Present area | Files | Bytes | Review |
| --- | ---: | ---: | --- |
| Root entries, `documentation/`, agent instructions, templates/adapters/skills including 8 installed copies | 62 | 218,567 | Full content read by owner and two bounded Astra xhigh helpers |
| Active Cards 128 and 141 | 2 | 11,409 | Full content; 128 remains an unapproved independent request |
| Draft Specifications 005, 013, 014, 020 | 4 | 12,361 | Metadata here; full content through authorized Writer handoff |
| 33 closed Batch records, 139 completed/cancelled Cards, 16 approved Specs, 8 journal/evidence records | 196 | 493,918 | Size/reference/structure coverage; preserve historical content, targeted reading only |

Deleted `agents/runner/build-and-run.md` and draft SPEC-010 are inventoried separately. The non-Markdown deletion `agents/VERSION`, untracked drafts 013/020 and `graphify-out/` are preserved. The old graph was not used as evidence; conclusions come from current sources. Resources contain four historical PNGs and placeholders, no additional prose. Technical coverage includes installers, synchronizer, role hook, board modules, guards, pre-push hook, both test suites and Telegram CI; no application sources remain after Runner removal.

## Principal findings

| ID | Finding and exact source | Proposed owner of the rule |
| --- | --- | --- |
| F1 | Competing adoption order: `install-in-a-project.md:3,9,45,53`; `configure-a-project.md:39-44` repeats agreement/preview/application. | `setup/install.md` sequences adoption; `setup/configure-workflow.md` owns workflow choices and commands. |
| F2 | `roles/user.md:15` still assigns guided tests to Writer; `batches/resume-a-batch.md:3` requires a separate Developer session despite current Orchestrator delegation. Human entry guides also retain old routing. | Tester for cases; Orchestrator for same-chat handoffs; explicit roles remain supported. |
| F3 | Example report says scope approval authorized work (`documentation/examples/batch-report.md:21`); agent example confuses acceptance with merge (`agents/batches/delivery-example.md:54`). | Shared approval gates; examples illustrate distinct recorded decisions. |
| F4 | Developer repeats notification policy in its role; Telegram mixes human secret setup, cadence, arguments, recovery and historical Batch-008 advice. | Separate setup and `actions/notify-user.md`; preserve all event/dedup rules from Card 135. |
| F5 | Batch state/schema, preparation, debt, correction, closure and guard setup overlap roles and two large procedures. All roles currently load operational details outside their phase. | Batch guidelines for invariant/state/debt policy; phase actions for execution. |
| F6 | Duplicate CSV examples and normative prose in templates drift (`delivery-example.md:5-136`, `templates/batch-tests.md:19`, `templates/batch-report.md:17-21`). | One connected example set; templates retain record shape and required evidence. |
| F7 | Human host guide duplicates low-level hook limitations; `understand-the-framework.md:33` promises alerts “once” despite unknown delivery states. | Technical limits in setup; human guides state consequences without stronger guarantees. |
| F8 | Hook indexes exact `role` / `agent_type`; unknown roles pass (`role-limit-hook.py:24-36,121-125`). Isolated ID rename would silently unrestrict old sessions. | Canonical writer/developer policy plus explicit legacy identity aliases. |
| F9 | Installer overwrites/removes named adapters; skills sync overwrites divergent current copies (`install-claude-role-hook.py:35-69`, `sync-skills.py:75-95`). Historical hash fixtures are synthesized from current text (`test-kanban-board.py:660-662`). | Safe recognized-byte migration, preserved custom files, genuine historical fixtures. |

The [link inventory](card-00000141-link-consumers.csv) lists 203 incoming Markdown links to audited active documents; [technical consumers](card-00000141-technical-consumers.csv) covers launch IDs, backtick paths, hard-coded source lists and tests. Outgoing relative links must also be recalculated after moves. Root/source/installed adapters are distinct responsibilities, not duplicate folders to merge.

## Context cost and checks

[Journey calculations](card-00000141-journeys.csv) separate unique required instructions, conditional additions, per-session rereads and project records. Largest active files: Batch pickup/closure 15,533 bytes; Telegram 15,149; README 12,344; orchestration 11,471; Batch workflow 10,035. **15 KB is a review signal, not a hard cap.** The 86,951-byte historical journal should be searched for relevant entries, not read in full by default.

Observed checks only: all 25 human/template/example files had valid local links (78) and anchors (12); all eight installed skills match their sources. Live board validation reports exactly two links to the pre-deleted Runner guide; skills `--check` stops on the pre-deleted VERSION. These are preserved baseline limitations, not audit regressions. No product tests, native host execution, external-link verification or refactoring verification is claimed.

Next decision: review the [migration plan](card-00000141-plan.md). Card 141 stays in Development; all implementation criteria remain open.
