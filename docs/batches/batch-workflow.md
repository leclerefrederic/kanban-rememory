# Specifications, Delivery Batches, and Cards

| Directory | Specification state |
| --- | --- |
| `draft/` | Being written or revised. |
| `ready/` | Ready to propose for Batch approval. Return it to draft if it needs clarification. |
| `approved/` | Exact revision approved for a Batch. Keep its contents and path stable. |

Start a new revision in draft when an approved Specification changes. Reuse an approved revision as-is in another Batch when it still fits, including after rejection of a delivery. The Batch records the delivery decision.


See the [project directory template](../templates/project-layout.md). Projects using Batches create `project/specs/draft/`, `project/specs/ready/`, `project/specs/approved/`, and `project/batches/` in the product repository. The folder determines a Specification's state. Start from the [Specification template](../templates/project-specification.md). Keep the Specification ID across revisions and assign each revision its own filename.

A Batch groups one or more Specifications. On approval, move the selected revisions from ready to `project/specs/approved/` and create the Batch as `ready`. Copy the [Description](../templates/batch-description.md), [UAT](../templates/batch-tests.md), and [Journal](../templates/batch-report.md) templates as `description.md`, `tests.md`, and `report.md`, respectively, in a folder such as `project/batches/batch-001/`. The directory name is the stable Batch ID. In the Description header, record each selected Specification in the `specifications` list with `id`, `revision`, and repository-relative `path`. The list order sets the priority. Add execution constraints only when the list cannot express them. The pinned file must carry the same Specification ID and revision. Keep approved revisions at their approved paths. The approval commit records the exact contents. Run `validate` for reference consistency and `verify-approval` against the trusted commit before pickup and closure. Historical Batches with a digest retain their original validation.

Batch records reference Specifications and delivery evidence. Keep Card IDs and links out of Batch records. A Card may reference a Batch or Specification from its own header.

Cards track Development Agent's tasks. Leave `batch: null` and `specifications: []` for standalone work, or fill either field when relevant. Use a YAML flow list of quoted IDs for `specifications`. Cards may reference Specifications in `ready` or `approved`. A Card that names a Batch and Specifications can name only Specifications selected in that Batch. A Batch-linked Card can omit Specifications for work such as preparing the acceptance environment.

Run `python3 tools/manage-kanban-board.py validate` to check the mapping. See the [agent roles](../agents/work-in-a-project.md#batch-workflow-roles).

For Git approval evidence, pickup coordination, and closure recovery, follow the [Batch operations guide](start-and-close-batches.md).

## Record headers

Fill in the IDs and selected Specifications before marking a Batch ready. Record the tested commit and verdicts in tests.md. Record the decision, closing trailer, and delivery tag or archive branch in report.md.

Use `type` and `id` on every record. Description is the Batch record. The fixed filenames tests.md and report.md identify the companion records within the Batch folder. Each companion carries its own ID and the parent `batch`. The Specification header carries its revision. A Card uses `batch` and `specifications` when applicable. Keep stable references in the header and the narrative and evidence in the body.

Use the templates' YAML subset for machine-read fields: one key per line and JSON-compatible quoted scalars, flow lists and mappings. Specification state comes from its folder. Batch status comes from its Description header. Older projects may still use `UAT.md` for acceptance tests. The board also reads older projects using `lots/` or `Lots/`, and approval verification can read that historical path from Git.

## Git provenance and state history

Use the stable ID to find a Card across stage directories. For example, inspect commits reachable from the locally fetched published main branch with:

```sh
git log origin/main --full-history --name-status -- ':(glob)project/kanban/**/task-00000029-*.md'
```

This identifies the commits that introduced or changed the Card on that branch. Fetch the remote first if you need its latest state. Record a tested code revision separately from the commit that published the Card. The publication commit cannot contain its own hash, and a Git commit date does not establish when it was pushed.

The move command records stage transitions in the Card's History section. Record changes within a stage, such as a blocker, when they happen. Git only shows transitions captured by commits. For a Batch, keep the current state in Description and record significant transitions, the decision, the tested revision and closing references in the Journal.

## Specification resources

Store shared attachments in `project/specs/resources/active/`. In the Specification's Resources section, link each required file and explain its purpose. Link existing repository files directly when they already serve that purpose.

Include every required resource in the Git approval snapshot. Check that each link resolves to a tracked file in that snapshot. Use the recorded approval commit to open the Specification and its resources together when reconstructing a historical delivery. Change a required resource through a new Specification revision.

When no Specification still needs a file for ongoing or planned work, move it to `project/specs/resources/archived/` and preserve its filename. Keep approved Specifications unchanged. Historical links resolve within the approval snapshot, which retains the exact file at its original path.
