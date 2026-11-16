---
id: "CARD-00000224"
module: "orchestrator"
---

# CARD-00000224 — Kit sans project/ en dur ; précisions section 0 et dossier de travail

- Dependencies: None. Fait suite à la Card 223 et à la série d'essais I à L.

## Expected outcome

(1) `workflow.md` et `guide.md` du kit désignent le dossier de travail par `DIR`, sans écrire `project/` en dur ; (2) `dist/INSTALL.md` donne une consigne au STOP « un seul ZIP » de la section 0 ; (3) les contrôles du dossier de travail disent qu'un `modules/` absent est valide, et que `misc` est un nom de module permis ; (4) ZIP du kit reconstruit.

## Scope and authorization

`kanban-rememory/orchestrator/workflow.md`, `kanban-rememory/documentation/guide.md`, `dist/INSTALL.md`, ZIP. Demande de l'utilisateur : « Oui, corrige ».

## Acceptance criteria

- Aucun `project/` en dur dans le kit (hors modèles).
- `kr validate` passe.
- Le ZIP contient les deux textes corrigés.

## History

- 2026-11-16T18:58:06+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T19:14:01+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T19:14:01+01:00 — Merge approved for the verified candidate `8d21eb923b2ec9c97b05a95fcf1bfa9711622c93`: “Oui, commit”.
