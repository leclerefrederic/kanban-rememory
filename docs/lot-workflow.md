# Fiches, Lots, and Cards

Projects using Lots create `specs/draft/`, `specs/ready/`, `specs/frozen/`, and `Lots/` in the product repository. The folder determines a Fiche's state. Start from the [Fiche template](lot-templates/Fiche.md). Keep the Fiche ID across revisions and assign each revision its own filename.

A Lot groups one or more Fiches. On approval, freeze the selected revisions in `specs/frozen/` and create the Lot as `ready`. Copy the [Description](lot-templates/Description.md), [UAT](lot-templates/Tests.md), and [Journal](lot-templates/Report.md) templates into a folder such as `Lots/Lot-001/`. The directory name is the stable Lot ID. In the Description header, record each selected Fiche in the `fiches` list with `id`, `revision`, repository-relative `path`, and `sha256`. The pinned file must carry the same Fiche ID and revision. Keep frozen revisions at their approved paths. At approval, compute the digest of the frozen file with `shasum -a 256 specs/frozen/FICHE-001-r1.md` and record the 64-character value. Run validation at approval, before pickup, and before closure. If the digest differs, stop and recover the approved bytes from trusted evidence. For older Lots without a digest, verify the approved bytes before recording one. A digest detects edits against the recorded value. Use Git history to check changes to the approval record itself.

Cards track Development Agent's tasks. Leave `lot: null` and `fiches: []` for standalone work, or fill either field when relevant. Use a YAML flow list of quoted IDs for `fiches`. Cards may reference Fiches in `ready` or `frozen`. A Card that names a Lot and Fiches can name only Fiches selected in that Lot. A Lot-linked Card can omit Fiches for work such as preparing the acceptance environment.

Run `python3 tools/board.py validate` to check the mapping. See the [agent roles](../agents/working-instructions.md#lot-workflow-roles).

For Git approval evidence, pickup coordination, and closure recovery, follow the [Lot operations guide](lot-operations.md).

## Record headers

Use `type` and `id` on every record. Description is the Lot record. Its `tests` and `report` point to the two companion records. Both companions use `lot` to point back to Description and carry the ID of the other companion. The Fiche header carries its revision. A Card uses `lot` and `fiches` when applicable. Keep stable references in the header and the narrative and evidence in the body.

Use the templates' YAML subset for machine-read fields: one key per line and JSON-compatible quoted scalars, flow lists and mappings. Fiche state comes from its folder. Lot status comes from its Description header. Historical records retain their original format, including the former Tests filename `UAT.md`, so prior approvals and frozen hashes stay verifiable.

## Git provenance and state history

Use the stable ID to find a Card across stage directories. For example, inspect commits reachable from the locally fetched published main branch with:

```sh
git log origin/main --full-history --name-status -- ':(glob)kanban/**/TASK-00000029-*.md'
```

This identifies the commits that introduced or changed the Card on that branch. Fetch the remote first if you need its latest state. Record a tested code revision separately from the commit that published the Card. The publication commit cannot contain its own hash, and a Git commit date does not establish when it was pushed.

The move command records stage transitions in the Card's History section. Record changes within a stage, such as a blocker, when they happen. Git only shows transitions captured by commits. For a Lot, keep the current state in Description and record significant transitions, the decision, the tested revision and closing references in the Journal.
