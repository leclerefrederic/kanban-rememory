# Specification and Batch rules

Batches are optional. A standalone Card does not require one. Writer owns scope/record preparation and User decision, Developer technical/Git execution, Tester acceptance observations. Role files define access; [develop](../actions/develop-batch.md), [close](../actions/close-batch.md) and [resume](../actions/resume-work.md) own ordered procedures.

## Scope and records

A Specification has a stable ID and serves one Batch. Keep proposals in `draft/`. When selected in a Batch for scope review, move them to `ready/` and record their IDs and paths in that Batch. After scope approval, move them to `approved/` and preserve their exact contents through development and correction. At verified Batch closure, retire them in `retired/` for historical lookup. Later work starts with a new ID.

With the User’s decision, Writer may move a proposal from `draft/` or `ready/` to `retired/`. Keep its ID and record the reason. Retired Specifications are ineligible for Batch selection. Resolve any active draft Batch reference before moving its proposal.

Only one Batch may be open in a single-project repository, or in each configured module. Writer reads every applicable status before creating another. A module Batch in draft or ready does not reserve its delivery slot. After pickup, it reserves the slot through verified closure. A draft can have no selection and may omit tests/report while being prepared; select Specs from `ready/` for that Batch. Every existing record already needs matching IDs. Before `ready`, explicit scope approval moves selected Specifications to approved, completes all three records and fixes their ordered mission. Execution authorization is distinct; one explicit instruction may grant both. Developer records the Git approval snapshot before pickup.

Use `project/batches/batch-001/description.md`, `tests.md`, `report.md` and the [templates](../templates/). The Description is the Batch record: `type`, `id`, `status`, ordered `specifications` entries with `id` and repository-relative `path`. The pinned file must match the ID. The approval snapshot records exact Spec bytes and resource contents. Closure keeps the original pin and approval evidence for historical verification. The ordered list supplies priority; add only execution constraints it cannot express. Each companion has its own `id` and parent `batch`; filename identifies tests/report. Preserve exact headers understood by tools.

IDs use `Batch-001`, `SPEC-001`, `Batch-001-Tests`, `Batch-001-Report`; paths are lowercase (`spec-001.md`). Command Batch IDs also accept lowercase. Machine fields use the templates' YAML subset: one key per line and JSON-compatible quoted scalars/flow lists/mappings. Historical revision fields and revisioned filenames remain readable for approval verification. Historical Lot IDs, `lots/`/`Lots/`, `UAT.md` and digest approval remain supported; do not rewrite history.

Cards may reference Batch/Specs using `batch` and `specifications`; linked Specs must be selected by that Batch. A Batch Card may omit Specs for support work. Batch records contain no Card references. Record tested revision/results in tests, User decision and closure references in report, current state in Description. Git preserves only committed transitions; log significant changes and interruptions.

## Batch states and transitions

| Transition | Actor and required condition |
| --- | --- |
| New → draft | Writer; no open Batch, assign ID and propose scope. |
| draft → ready | Writer; explicit User scope approval, approved exact Specifications and complete records. |
| ready → in-progress | Developer; execution authorized, approval verified, ownership acquired, agreed branch/base. |
| in-progress → delivered | Developer; technical checks pass, exact candidate and reproducible startup recorded. |
| delivered → in-progress | Developer; documented blocking defect, authorized correction inside fixed scope, retain prior results. |
| delivered → validated | Writer; all required tests pass, no blocking debt, explicit User acceptance of that revision and nonblocking deferrals. |
| delivered → rejected | Writer; explicit User rejection of that revision, preserve debt/outstanding tests. |
| validated/rejected → closed | Developer; verified closure/publication; recover interruptions before new work. |

Correction delivers a new candidate; interruption resumes the same state/branch. Never reopen a closed Batch. `validate` checks structure/references, not User authority; `verify-approval` checks snapshot bytes, not permission to execute or accept.

## Resources

Store required attachments in the workspace's `specifications/resources/active/` and link each from the Spec's Resources section with its purpose. Use an existing legacy `specs/` directory at its original path. Existing repo files can be references; binding external files belong in this resource folder for approval protection. Include required resources in the approval commit and verify tracked links there. Changes to those requirements need a new Specification.

Writer archives a resource only when no ongoing/planned Spec needs it: move to `resources/archived/`, preserve filename and avoid collisions across both directories. Do not edit approved links. The approval snapshot retains exact historical bytes. Use the trusted snapshot to retrieve historical binary bytes.

## Debt and correction

Every observed defect opens one debt identity, even during OK tests. Report records: stable reference, affected Spec/test, severity, impact and whether acceptance is blocked. S0 = unusable system; S1 = essential workflow without acceptable workaround; S2 = degraded operation; S3 = minor. Test verdicts are independent. In tests.md preserve every blocked/unexecuted required case with original ID/expected result and reason/link.

Blocking debt prevents acceptance. Continue independent tests. Writer's correction request records candidate, failing case, expected/observed behavior, evidence, affected/blocked tests and execution authorization. Developer verifies scope and resumes the same Batch/branch; Tester replays failing/affected cases before newly unblocked cases against the new candidate. Keep earlier candidates/results. Acceptance needs verified correction and all required scenarios; nonblocking debt requires explicit User deferral.

On rejection retain open debt/outstanding tests. Retire the Specs on closure. If the work resumes in a new Batch, write a new Specification and reference the earlier evidence. Before a successor, review prior reports for selected Specs/dependencies; carry relevant debt, every outstanding required case with original expected result/reason and the failing regression case. Resolve blocking debt before dependent work.

Closed reports are immutable. Resolve inherited debt in the successor report using its original reference (for example `Batch-001-DEBT-01`) and original report link. Record fix revision, regression/outstanding-test results and the accepted delivery containing the correction. Search later reports by that identity; rejected successors do not resolve published-baseline debt. Do not create a second identity. See the [connected example](../../documentation/examples/batch-report.md).
