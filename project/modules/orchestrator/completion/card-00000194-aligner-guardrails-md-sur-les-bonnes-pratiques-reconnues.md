---
id: "CARD-00000194"
module: "orchestrator"
---

# CARD-00000194 — Aligner GUARDRAILS.md sur les bonnes pratiques reconnues

- Dependencies: Aucune.

## Expected outcome

`GUARDRAILS.md` reprend les bonnes pratiques reconnues de sécurité des agents (OWASP Top 10 for Agentic Applications 2026, guides AGENTS.md), dans un style homogène et court.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, successeur de CARD-00000193. Travail sur `main`. Sources : OWASP Gen AI Security Project et guides AGENTS.md, lus par recherche web (résumés tiers, texte OWASP non consulté directement).

- Chaque règle : une ligne, à l'impératif, en anglais, sans doublon avec `workflow.md`.
- Ajout demandé le 2026-11-16 : une section `Overrides`, vide par défaut avec exemples en commentaire, où l'utilisateur accorde une autorisation permanente (commit direct sur `main`, fusion automatique).
- Hors périmètre : hooks, bac à sable, section Comply.

## Acceptance criteria

- Les sections reprennent : moindre agence, contenu lu traité comme donnée, accord avant action destructive ou sortante, secrets.
- Style homogène : une ligne par règle, même forme.
- Une section `Overrides` existe, sans autorisation active par défaut.
- `validate` passe.

## History

- 2026-11-16T09:26:22+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T09:28:57+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T09:28:57+01:00 — Merge approved for the verified candidate `e6aaa5a5a0453d035639c937f51dede575ff87de`: “Approuvé”.
