---
id: "CARD-00000200"
module: "orchestrator"
---

# CARD-00000200 — Définir kr dans install.md

- Dependencies: Aucune.

## Expected outcome

`install.md` définit `kr` avant de l'utiliser, pour qu'un agent qui n'a pas encore lu `workflow.md` sache quelle commande lancer.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, successeur de CARD-00000199. Travail sur `main`. Seul `kanban-rememory/orchestrator/install.md` change. Contrôle des liens de la base documentaire : aucun lien cassé ni ancien chemin trouvé, rien d'autre à corriger.

## Acceptance criteria

- `install.md` définit `kr` dans ses Instructions et l'utilise ensuite.
- `validate` passe.

## History

- 2026-11-16T13:23:30+01:00 — Stage moved from `backlog` to `development`.
