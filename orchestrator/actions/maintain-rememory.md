# Maintain Rememory

Keep one project journal in `project/rememory/`, one `YYYY-MM-DD.md` file per date with an entry, following the [daily template](../templates/rememory-day.md). Insert each new entry below the date heading. Use the project timezone.

Record project decisions, priority changes, useful resumption notes and one concise milestone per verified publication: result, Card link and published revision. A cross-module delivery has one milestone. Keep secrets and personal data out.

Write milestones with `manage-module-delivery.py milestone`; it serializes writes and avoids duplicate publication entries. A publication milestone is written in the primary checkout after the push; commit it with the next closing commit. Search by stable Card ID when resuming; do not load every daily file. The module Kanban stays the source of truth for Card stages.
