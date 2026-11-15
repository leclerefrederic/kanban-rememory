# Maintain Rememory

Use `project/rememory/project/` for the project journal and `project/rememory/modules/<module-id>/` for module journals. With a custom `shared.memory`, apply the same structure there. Existing journal locations remain in use until an approved [migration](../setup/project-layout.md#migrate-existing-journals).

Keep one `YYYY-MM-DD.md` file per working day and owner, using the [daily template](../templates/rememory-day.md). Insert each new milestone below the date heading and above earlier entries.

Record decisions, integrations, checks actually run, changes in priority, and where to resume. For each entry, include the card, result, validation status, evidence, and next action. Distinguish proposed or approved decisions from changes that have been tested, merged, published, or deployed. Never write that a publication is pending, local or not done: the entry is committed in the commit that gets published, so the statement turns false at the push. Git shows the publication state. Mention a publication only afterward, as a done fact with its commit range, in a later entry.

Record solution decisions and one concise milestone per verified publication in project Rememory. Give scope, outcome, actual published revision and a link to the Card or Batch. A Batch publication gets one milestone for the Batch. On interruption, verify published Git evidence and add the missing milestone once. Use [delivery coordination](coordinate-modules.md) to serialize writes and deduplicate retried module-aware publications.

Keep durable module-specific reasons and resumption notes in that module's Rememory. Keep project scope notes in project Rememory. A Card/Spec/Batch with sufficient detail only needs its publication milestone. Link to the record that owns each detail. Keep secrets and personal data out of journals.

For status across modules, combine the shared board, active Batches and the latest project publication milestone per scope. Follow the assigned module's linked work note when resuming a delivery.

Before handing work over, check that someone else can find the evidence and resume from the journal. The Kanban card remains the source of truth for task status.
