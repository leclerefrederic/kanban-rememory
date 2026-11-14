# Specifications, Delivery Batches, and Cards

Write and review Specifications using the [Lean Specifications manifesto](../lean-specifications.md). Apply its approval test before proposing a ready Specification for Batch approval. Record value in Expected outcome, agreed behavior and binding mockup details in Scope, and setup, action, and expected result in Acceptance criteria. Use the existing template sections; link test results and debt records from the Batch records during delivery.

| Directory | Specification state |
| --- | --- |
| `draft/` | Being written or revised. |
| `ready/` | Ready to propose for Batch approval. Return it to draft if it needs clarification. |
| `approved/` | Exact revision approved for a Batch. Keep its contents and path stable. |

Start a new revision in draft when an approved Specification changes. Reuse an approved revision as-is in another Batch when it still fits, including after rejection of a delivery. The Batch records the delivery decision.


See the [project directory template](../templates/project-layout.md). Projects using Batches create `project/specs/draft/`, `project/specs/ready/`, `project/specs/approved/`, and `project/batches/` in the product repository. The folder determines a Specification's state. Start from the [Specification template](../templates/project-specification.md). Keep the Specification ID across revisions and assign each revision its own filename.

A ready Batch groups one or more approved Specifications. Prepare it as `draft` using the [description](../templates/batch-description.md), [tests](../templates/batch-tests.md), and [report](../templates/batch-report.md) templates in a folder such as `project/batches/batch-001/`. Assign the Batch ID on creation. A draft may have an empty selection and may omit the tests or report while being prepared; any records already present need their IDs and matching Batch reference. A selected Specification must be ready or approved. This permits preparation without making the Batch executable.

On explicit scope approval, move the selected revisions to `project/specs/approved/`, complete all three records, and set the Batch to `ready`. In `description.md`, record each selection in the `specifications` list with `id`, `revision`, and repository-relative `path`. The list order sets priority; add execution constraints only when the list cannot express them. The pinned file must carry the same ID and revision. Keep approved revisions and their paths stable. The approval commit records the exact contents. Run `validate` for reference consistency and `verify-approval` against the trusted commit before pickup and closure. Historical Batches with a digest retain their original validation.

Batch records reference Specifications and delivery evidence. Keep Card IDs and links out of Batch records. A Card may reference a Batch or Specification from its own header.

Cards track Development Agent's tasks. Leave `batch: null` and `specifications: []` for standalone work, or fill either field when relevant. Use a YAML flow list of quoted IDs for `specifications`. Cards may reference Specifications in `ready` or `approved`. A Card that names a Batch and Specifications can name only Specifications selected in that Batch. A Batch-linked Card can omit Specifications for work such as preparing the acceptance environment.

Run `python3 tools/manage-kanban-board.py validate` to check the mapping. See the [agent roles](../agents/work-in-a-project.md#batch-workflow-roles).

For Git approval evidence, pickup coordination, and closure recovery, follow the [Batch operations guide](start-and-close-batches.md).

## Batch states and transitions

The state lives in `description.md`. The following transitions are procedural rules; `validate` checks record structure, not User authorization or acceptance evidence. A passing `verify-approval` compares scope with its approval snapshot and does not authorize execution or acceptance.

| Transition | Actor | Required condition |
| --- | --- | --- |
| New → `draft` | Specification Agent | No other open Batch; assign the Batch ID and prepare scope. |
| `draft` → `ready` | Specification Agent | Explicit User scope approval, approved Specification revisions, and complete records. Development Agent records the Git approval snapshot before pickup. |
| `ready` → `in-progress` | Development Agent | Execution authorized, approval verified, ownership acquired, and recorded branch created from the agreed base. |
| `in-progress` → `delivered` | Development Agent | Technical checks pass; commit, artifact, and startup instructions identify the candidate to test. |
| `delivered` → `in-progress` | Development Agent | A documented blocking defect and authorized correction within the approved scope; preserve the previous candidate and results. |
| `delivered` → `validated` | Specification Agent | All required tests pass, no blocking debt remains, and the User explicitly accepts that revision with any nonblocking deferrals. |
| `delivered` → `rejected` | Specification Agent | The User explicitly rejects that revision; retain defects and outstanding tests. |
| `validated` or `rejected` → `closed` | Development Agent | Follow the closure procedure, recording the decision and verifying final publication. Retry an interrupted closure before starting anything new. |

Correction returns to `delivered` with a new candidate. An interruption resumes the existing state and branch; a closed Batch is never reopened. Approval of scope and authorization to execute are distinct, but one explicit User instruction may grant both. See the [worked delivery example](delivery-example.md).

## Record headers

Use `Batch-001` as the Batch ID and `batch-001/` as its directory. Use `SPEC-001` with `spec-001-r1.md` for a Specification revision, and distinct companion IDs such as `Batch-001-Tests` and `Batch-001-Report`. Filenames and directories are lowercase; identifiers retain their documented spelling. Keep exact IDs in cross-references. Command arguments also accept the lowercase Batch spelling, for example `verify-approval batch-001 COMMIT`. Historical `Lot` identifiers remain supported; do not rewrite approved history.

Fill all IDs and selected approved Specifications before marking a Batch ready. Record the tested commit and verdicts in `tests.md`. Record approval handoff, decision, closing trailer, and delivery tag or archive branch in `report.md`.

Use `type` and `id` on every record. Description is the Batch record. The fixed filenames tests.md and report.md identify the companion records within the Batch folder. Each companion carries its own ID and the parent `batch`. The Specification header carries its revision. A Card uses `batch` and `specifications` when applicable. Keep stable references in the header and the narrative and evidence in the body.

Use the templates' YAML subset for machine-read fields: one key per line and JSON-compatible quoted scalars, flow lists and mappings. Specification state comes from its folder. Batch status comes from its Description header. Older projects may still use `UAT.md` for acceptance tests. The board also reads older projects using `lots/` or `Lots/`, and approval verification can read that historical path from Git.

## Git provenance and state history

Use the stable ID to find a Card across stage directories. For example, inspect commits reachable from the locally fetched published main branch with:

```sh
git log origin/main --full-history --name-status -- ':(glob)project/kanban/**/task-00000029-*.md'
```

This identifies the commits that introduced or changed the Card on that branch. Fetch the remote first if you need its latest state. Record a tested code revision separately from the commit that published the Card. The publication commit cannot contain its own hash, and a Git commit date does not establish when it was pushed.

The move command records stage transitions in the Card's History section. Record changes within a stage, such as a blocker, when they happen. Git only shows transitions captured by commits. For a Batch, keep the current state in `description.md`, the tested revision and results in `tests.md`, and significant transitions, the decision and closing references in `report.md`.

## Specification resources

Store shared attachments in `project/specs/resources/active/`. In the Specification's Resources section, link each required file and explain its purpose. Link existing repository files directly when they already serve that purpose.

Include every required resource in the Git approval snapshot. Check that each link resolves to a tracked file in that snapshot. Use the recorded approval commit to open the Specification and its resources together when reconstructing a historical delivery. Change a required resource through a new Specification revision.

When no Specification still needs a file for ongoing or planned work, move it to `project/specs/resources/archived/` and preserve its filename. Keep approved Specifications unchanged. Historical links resolve within the approval snapshot, which retains the exact file at its original path. For a later Batch reusing an approved revision, restore required resources at their approved paths before execution rather than changing the approved links.

For example, two Specifications may share `resources/active/export-layout-v1.png`. Leave it active while either still needs it. A changed design gets `export-layout-v2.png` and a new Specification revision; do not overwrite v1. When v1 is no longer needed for planned or ongoing work, move it to archived. Keep resource filenames unique across both directories so an archive move never overwrites an earlier file. Use `git show APPROVAL_COMMIT:project/specs/resources/active/export-layout-v1.png` to recover the historical bytes (redirect binary output to a file). Include any required restored resources in the next approval snapshot.
