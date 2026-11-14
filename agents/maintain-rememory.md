# Maintain Rememory

Keep one `YYYY-MM-DD.md` file per working day and owner, using the [daily template](templates/daily-template.md). Insert each new milestone below the date heading and above earlier entries.

Record decisions, integrations, checks actually run, changes in priority, and where to resume. For each entry, include the card, result, validation status, evidence, and next action. Distinguish proposed or approved decisions from changes that have been tested, merged, published, or deployed. Never write that a publication is pending, local or not done: the entry is committed in the commit that gets published, so the statement turns false at the push. Git shows the publication state. Mention a publication only afterward, as a done fact with its commit range, in a later entry.

For shared work, each owner records their contribution and links to the other journals. Use a shared journal for cross-team coordination if the repository provides one. Keep secrets and personal data out of the journal.

Before handing work over, check that someone else can find the evidence and resume from the journal. The Kanban card remains the source of truth for task status.
