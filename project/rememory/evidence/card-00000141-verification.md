# CARD-00000141 — Verified migration

Implementation candidate: `98ac495347b3da93b71aa449c45f43656e131b30`, branch `codex/card-00000141-docs`. Baseline: `308b747c82dbe290bbd14a53d791be90c2949646`. The User approved the plan and execution in the original Codex chat. The final closure commit changes records and reference-only closure updates.

## Outcome and checks

Canonical instructions now separate guidelines, actions, setup, roles and host adapters. Writer/Developer names and launch policies agree; legacy IDs resolve to those same policies. Upgrades preserve customized/current/legacy copies and third-party hooks. Shared permissions did not widen. Installation owns one approval/copy/application sequence; option setup owns its commands. SPEC-020 was consolidated under Writer ownership; SPEC-013 behavior remains unapproved and outside implementation.

Executed on the exact candidate: **36 board tests, 14 migration tests and 22 Telegram setup tests passed**. Board validation, installed skill consistency and diff checks passed. The role suite covers real distributed fingerprints, old/new identity parity, incomplete upgrades, custom current/old sources, symlinks, missing sources, shared hook groups, safe removal and idempotence. Telegram tests use fake credentials/responses and send nothing.

The earlier `8f69fc3` candidate gained one setup correction: copy the Telegram verification script so the documented command works in an adopted project, plus its reproducible adoption evidence script. All three suites and adoption checks were rerun on `98ac495`; both native probes target that final candidate.

[Obligation matrix](card-00000141-obligations.csv): **33/33 content obligations reviewed** across 23 canonical documents. This is a semantic review, not 33 additional execution tests. The [Codex native report](card-00000141-native-codex.md) separates observed startup from reported child-role behavior and explicitly does not claim Codex hook enforcement.

The [Claude native report](card-00000141-native-claude.md) and [sanitized observations](card-00000141-native-claude-summary.json) record **five successful probes and 17 permitted Read calls** on the exact candidate. Native hook inputs identify Writer, Developer, Tester and both legacy identities; all resolve to the canonical policies. The User explicitly authorized sending only isolated fixture instructions to Claude/Anthropic after automatic review rejected the earlier attempt. No bypass was used. Legacy identities were launched using original adapters; a process started before upgrade and resumed afterward was not exercised. Negative permission cases are the unit matrix, not claimed native denials.

## SPEC-020 scenarios

Run [the adoption check](card-00000141-adoption-check.py) against the candidate checkout. [Results](card-00000141-adoption-results.json) record six checks, including a separate frozen-content/ACL check.

| Original scenario | Result and evidence |
| --- | --- |
| 1. Fresh core | PASS: exact static package copied; preview makes no board; approved apply creates Standard/timezone/WIP; validate/show pass; rerun leaves bytes unchanged. |
| 2. Existing project and selected modules/hosts | PASS local adoption: existing instructions/product preserved; both host skill targets, Claude installer and Batch directories configured in the existing fixture. Native host observations are reported separately. |
| 3. Later option and repeat setup | PASS: options added after core; rerun unchanged; personal skill, existing model/Stop hook, project instructions and product bytes preserved. Fourteen migration regressions additionally cover customized kit copies and old sources. |
| 4. Missing prerequisite and recovery | PASS: missing canonical Writer adapter refuses before changing settings/files; restoring it permits setup. This exercises a missing module prerequisite, not an unavailable Python/OS installation. |
| 5. Links/commands and honest Telegram verification | PASS: validation and copied verification command run; 22 simulated Telegram cases pass. No live delivery is inferred from them. |

Exact Git blob comparison preserves **188 frozen Markdown records and six resource entries** across completed/cancelled Cards, closed Batches, approved Specs and resources. Existing daily-journal content is retained verbatim with new milestones inserted. The three user deletions and unrelated draft/graph changes remain outside this work. Fourteen old Markdown references remain usable through 11 small relays; the historical README anchor and software example anchor also remain valid. Role relays carry no policy frontmatter.

## Measured context costs

[File measurements](card-00000141-measured-files.csv) and [journey measurements](card-00000141-measured-journeys.csv) use UTF-8 bytes, with tokens estimated as `ceil(bytes/4)`; these are not tokenizer or runtime billing counts. Canonical active Markdown goes from **62 files / 218,567 bytes** to **66 files / 161,689 bytes**. Eleven compatibility relays add **2,569 bytes**: total **164,258 bytes**, a **24.8% reduction including compatibility**. The four additional canonical files reflect phase separation; relays are never active reading routes.

| Journey | Before estimated tokens | After | Change |
| --- | ---: | ---: | ---: |
| Orchestrator startup | 8,806 | 4,395 | −50.1% |
| Developer startup | 6,120 | 2,593 | −57.6% |
| Orchestrator intake | 12,063 | 6,470 | −46.4% |
| Standalone development | 9,608 | 4,879 | −49.2% |
| Tester acceptance | 5,203 | 2,947 | −43.4% |
| Authorized direct Developer core setup | 13,566 | 7,144 | −47.3% |
| Full Developer Batch recovery route | 15,722 | 9,392 | −40.3% |

Each row is one agent's required-file union, excluding project scope/evidence and optional skill entry. Tester acceptance adds the relevant debt section, consistently with the baseline comparison; the CSV also gives the cost of loading the whole Batch guide. Intake conservatively adds the full board-command reference, omitted from the proposed target budget. Across three separate intake/development/acceptance agents, repeated common reads are counted again: **107,494 → 57,180 bytes (−46.8%)**. A new chat incurs its own reads; no cross-agent deduplication is claimed.

Budgets were indicative, not permission to drop rules. Largest operational guide is Batch invariants at **6,487 bytes**, down from the 15,533-byte mixed procedure; the largest human entry is README at 6,998. Modest target exceptions preserve approval/debt/resource/guard details: development +443 bytes, recovery +200, scheduling +327, Batch guide +487, lean +383, shared +31, Tester +66, installation +471. Template Card +85 adds already-required scope/authority; report example +1,255 consolidates the deleted duplicate's inherited-debt example; human Telegram +1,211 retains private setup/failure protections; User responsibilities +280 retains decisions/interfaces. These do not force unrelated files into startup.

Native Windows behavior and real Telegram delivery were not exercised by this documentation migration. Existing tests distinguish simulated ACLs from a native Windows run. The earlier unconfirmed attention alert was not retried.
