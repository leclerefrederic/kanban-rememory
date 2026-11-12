# Fiches, Lots, and Cards

Projects using Lots create `specs/draft/`, `specs/ready/`, `specs/frozen/`, and `Lots/` in the product repository. The folder determines a Fiche's state. Start from the [Fiche template](lot-templates/fiche.md). Keep the Fiche ID across revisions and assign each revision its own filename.

A Lot groups one or more Fiches. On approval, freeze the selected revisions in `specs/frozen/` and create the Lot as `ready`. Copy the [Description](lot-templates/Description.md), [UAT](lot-templates/UAT.md), and [Journal](lot-templates/Report.md) templates into a folder such as `Lots/Lot-001/`. The directory name is the stable Lot ID. In Description, record each selected Fiche with a line in the form `- Fiche: ID | revision | repository-relative path`. The pinned file must carry the same Fiche ID and revision. Keep frozen revisions at their approved paths.

Cards track Claude Code's tasks. Leave `Lot ID` and `Fiche IDs` empty for standalone work, or fill either field when relevant. List multiple Fiche IDs separated by commas. Cards may reference Fiches in `ready` or `frozen`. A Card that names a Lot and Fiches can name only Fiches selected in that Lot. A Lot-linked Card can omit Fiches for work such as preparing the acceptance environment.

Run `python3 tools/board.py validate` to check the mapping. See the [agent roles](../agents/working-instructions.md#lot-workflow-roles).
