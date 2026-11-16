---
id: "CARD-00000183"
module: "orchestrator"
---

# CARD-00000183 — Aligner la définition de phase du guide sur le travail possible sur main

- Dependencies: Aucune.

## Expected outcome

La définition de « Phase » dans `documentation/guide.md` dit qu'une phase se déroule sur `main` ou sur une branche de release, comme le workflow depuis CARD-00000173.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, après l'audit du dépôt : corriger la ligne 10 du guide dans une Card sur `main`. Une seule ligne change ; aucun autre fichier.

## Acceptance criteria

- La puce « Phase » de `documentation/guide.md` mentionne `main` et la branche de release, et ne contredit plus le reste du guide ni `orchestrator/workflow.md`.
- `validate` passe.

## History

- 2026-11-16 — Décision de l'utilisateur : travailler sur `main`.

- 2026-11-16T07:27:05+01:00 — Stage moved from `backlog` to `development`.
