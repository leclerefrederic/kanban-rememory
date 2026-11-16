---
id: "CARD-00000192"
module: "orchestrator"
---

# CARD-00000192 — Ajouter GUARDRAILS.md lu par l'agent

- Dependencies: Aucune.

## Expected outcome

Un fichier `GUARDRAILS.md` à la racine, que l'utilisateur remplit avec ses interdits, et que l'agent lit avant chaque Card et respecte.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : fichier `GUARDRAILS.md` en majuscules à la racine. Travail sur `main`. Gabarit commenté à remplir, sans règle imposée ; règle de lecture dans `orchestrator/workflow.md`.

- Hors périmètre : hook, vérification par `kr`, copie du fichier par `install.md`.

## Acceptance criteria

- `GUARDRAILS.md` existe à la racine avec des sections à remplir.
- `workflow.md` demande de le lire avant chaque Card, de le suivre et de ne le modifier que sur demande.
- `validate` passe.
