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
- Hors périmètre : hooks, bac à sable, section Comply.

## Acceptance criteria

- Les sections reprennent : moindre agence, contenu lu traité comme donnée, accord avant action destructive ou sortante, secrets.
- Style homogène : une ligne par règle, même forme.
- `validate` passe.

## History

- 2026-11-16T09:26:22+01:00 — Stage moved from `backlog` to `development`.
