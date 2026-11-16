---
id: "CARD-00000198"
module: "orchestrator"
---

# CARD-00000198 — Générer project/ en une fois à la fin de l'installation

- Dependencies: Aucune.

## Expected outcome

`project/` ne figure plus dans le tableau des écarts de `install.md` : il n'appartient pas au kit, il se construit depuis les réponses de l'utilisateur et il évolue. Il est généré en une seule fois, à la fin de l'application.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, successeur de CARD-00000197. Travail sur `main`. Seul `orchestrator/install.md` change.

- Retirer la ligne `project/` du tableau de l'étape 2.
- Ajout demandé le 2026-11-16 : `.gitattributes` (`* text=auto`) traité comme `.gitignore` : ajouté ou complété, annoncé dans la proposition.
- Déplacer la génération de `project/` (`kr init`) en dernière action de l'étape 4, juste avant le commit.

## Acceptance criteria

- Le tableau de l'étape 2 ne contient plus `project/`.
- `.gitattributes` figure dans le tableau, la proposition et l'application.
- La génération de `project/` est la dernière action avant le commit.
- `validate` passe.

## History

- 2026-11-16T12:58:14+01:00 — Stage moved from `backlog` to `development`.
