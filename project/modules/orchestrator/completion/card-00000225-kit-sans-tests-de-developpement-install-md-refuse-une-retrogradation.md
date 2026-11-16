---
id: "CARD-00000225"
module: "orchestrator"
---

# CARD-00000225 — Kit sans tests de développement ; INSTALL.md refuse une rétrogradation

- Dependencies: None. Fait suite à la Card 224 et à la série d'essais M à P.

## Expected outcome

(1) Le ZIP du kit ne contient plus `test-kr.py` ni `test-telegram.py` : ils dépendent de la config et de la mise en page de ce dépôt ; `workflow.md` dit que ces tests existent seulement dans le dépôt source du kit. (2) `dist/INSTALL.md` s'arrête, avant le plan, quand le `kit` installé est plus récent que `KIT_VERSION`. (3) Précisions : consigne quand `origin` n'existe pas, « below » remplacé par « dans ton message à l'utilisateur », `N lines appended` calculé avant d'afficher le plan. (4) ZIP reconstruit.

## Scope and authorization

`dist/build-kit.py` et son test, `kanban-rememory/orchestrator/workflow.md`, `dist/INSTALL.md`, ZIP. Demande de l'utilisateur : « Oui, corrige ».

## Acceptance criteria

- Le ZIP ne contient aucun `test-*.py` du kit.
- Le test du builder le prouve.
- `kr validate` passe.

## History

- 2026-11-16T19:16:43+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T19:17:51+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T19:17:51+01:00 — Merge approved for the verified candidate `fee61461636222833f28f6835fbb490b46e77254`: “Oui, commit”.
