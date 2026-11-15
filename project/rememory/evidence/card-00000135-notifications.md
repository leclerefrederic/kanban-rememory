# CARD-00000135 — Notification review evidence

- Date: 2026-11-15, Europe/Paris.
- Candidate: `bbdf56d4bead674425f19f25abf9a8f1eb73ecc5`.
- Sender SHA-256: `039755c69073a790f2092febde61f7be0692a66e92c216c4f131867e192e0845`.
- Scope and implementation were authorized by the User. The Orchestrator reviewed the five-field preview and reported conformity. These are technical checks, not a fabricated User acceptance verdict.

## Findings and corrections

The previous Batch defaults omitted a concrete next action and used generic English text. Generic alerts did not require a Card/Batch reference; the deduplication key hashed wording, so a reworded resend was a new event. The sender now requires reference, summary and next action and renders one shared layout. French and English hooks/labels are supplied; agents provide translated labels for other known languages. The host/title is supplied from the actual conversation. The agent owns the meaning and brevity of the prose; the tool does not infer or translate it.

Cadence remains event-based: human action, delivered candidate, completed requested outcome. No progress alerts, intermediate Card completion alerts, timer or reminder was added. Orchestrator/Developer share one sender and stable task/event identifiers. Closed/completed aliases for one Batch share an outcome; corrected candidate revisions remain distinct.

Legacy rows contain no reversible task/text mapping. Exact original wording or `--previous-text` can prove a match, preserving confirmed and uncertain states and keeping the original row. The User explicitly preferred an extra alert over a missed request when uncertain; use a new identifier when an old match cannot be established. Universal automatic deduplication of old reworded messages is not claimed.

## Automated checks

- Full board suite: 36 tests passed, including new structure/language and legacy receipt scenarios.
- Telegram setup suite: 22 tests passed, with fake credentials and simulated responses.
- After a native probe supplied the emoji inside a translated hook, added prefix normalization and reran the affected language and CLI-validation tests: 2 passed against the exact candidate archive. A label that already starts with its event icon no longer duplicates it.
- Exact candidate archive: Kanban validation and skill synchronization check passed. `git diff --check` passed; implementation diff reviewed while the Card was in Development.
- The live workspace has unrelated deletions of `agents/VERSION` and `agents/runner/build-and-run.md`. They cause its skills check and two historical link checks to fail. The scoped archive retains the committed baseline files, passes, and those unrelated deletions were neither restored nor included.

## Native host exercises, simulated Telegram

Separate native Codex and Claude Code CLI sessions read the current instructions and executed actual wrapper/sender commands in isolated Git fixtures. No real token or recipient was used. The transport captured JSON payloads and simulated confirmed, refused and uncertain responses. The prompts explicitly represented simulated user decisions; no real acceptance or publication was claimed by these events.

| Scenario | Codex | Claude Code |
| --- | --- | --- |
| Actionable PDF/CSV question visible before first attention alert | Passed | Passed |
| Same ID, rewording and Orchestrator chat relay | No second capture | No second capture |
| Distinct request with a new ID | Captured | Captured |
| Batch delivery and corrected revision, no extra generic attention | Two captures | Two captures |
| Batch closed and completed alias | One capture | One capture |
| Standalone completed, explicit no action required | Captured | Captured |
| Disabled event | No capture | No capture |
| Definite refusal | Failed, no confirmed delivery | Failed, no confirmed delivery |
| Unknown outcome | Unconfirmed; no blind retry | Unconfirmed; no blind retry |
| French structure and actual host | Passed | Passed |
| English unknown-language fallback and supplied Spanish labels | Preview passed | Preview passed; duplicate icon corrected afterward |

Each host produced exactly six captured messages: two distinct interventions, two candidate deliveries, one Batch outcome, one standalone completion. The final sender change after these sequences only normalizes an already-supplied leading icon and clarifies help text; the affected rendering and CLI checks passed again on the final candidate. No cadence, key, storage or transport behavior changed afterward.

Codex's initial native CLI attempt could not write the production ledger path under protected `.git`; it captured zero messages. That restriction is retained as an integration limitation, not called a pass. Its subsequent bounded exercise used the existing `notify(..., ledger=...)` injection point to supply a permitted scratch SQLite file, keeping production argument parsing, rendering and sender logic. Claude exercised the normal `.git` ledger with mocked network. Initial fake-config permissions were corrected to 600 before the successful attempts. These tests do not prove access to production `.git` in every host sandbox, Windows execution, or actual Telegram delivery.

Scratch evidence (local, temporary):

- Codex native: `/var/folders/ql/x0h6wn_n6w77xfkvl42r2q240000gn/T/kr-card135-7d_q3jet/codex/evidence-native.md`.
- Codex scratch: `/var/folders/ql/x0h6wn_n6w77xfkvl42r2q240000gn/T/kr-card135-7d_q3jet/codex/evidence-scratch.md`.
- Claude: `/var/folders/ql/x0h6wn_n6w77xfkvl42r2q240000gn/T/kr-card135-7d_q3jet/claude/evidence.md`.

## Captured examples

```text
🔔 Action requise

Projet: CARD-135 fixture
Référence: CARD-00000135
Résumé: Simulation : quel format souhaitez-vous pour le rapport, PDF ou CSV ?

Prochaine action: Choisissez PDF ou CSV dans la conversation originale. — Codex · CARD-135 fixture
```

```text
🧪 Prêt à tester

Projet: CARD-135 fixture
Référence: Batch-010
Résumé: Simulation : le candidat testé attend votre acceptation. (révision aaaaaaa)

Prochaine action: Exécutez les tests d’acceptation dans la conversation originale. — Codex · CARD-135 fixture
```

```text
✅ Travail terminé

Projet: CARD-135 fixture
Référence: CARD-00000135
Résumé: Simulation : le rapport est exporté et son contenu vérifié.

Prochaine action: Aucune action requise. — Codex · CARD-135 fixture
```

## Closure boundary

All Card criteria were covered by the review, automated checks and explicitly simulated native-host exercises above. Real final completion delivery is performed only after verified publication and reported separately in the original chat; it is not represented by these fixture captures. No additional Windows or live acceptance claim is made.
