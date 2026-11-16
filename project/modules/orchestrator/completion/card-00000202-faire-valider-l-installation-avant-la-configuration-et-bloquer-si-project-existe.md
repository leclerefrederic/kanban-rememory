---
id: "CARD-00000202"
module: "orchestrator"
---

# CARD-00000202 — Faire valider l'installation avant la configuration et bloquer si project/ existe

- Dependencies: None.

## Expected outcome

Dans `install.md` :
- L'utilisateur valide le plan d'installation (étape 2) avant toute décision de configuration (étape 3).
- Si `kanban-rememory/` est absent et que `project/` existe, l'installation s'arrête : `project/` est le dossier de travail de KR.

## Scope and authorization

`install.md` seulement. Un dossier de travail choisi par l'utilisateur n'est pas traité ici : il demanderait un changement de `kr`, à décider à part.

## Acceptance criteria

- Étape 2 : STOP si `project/` existe sans `kanban-rememory/`.
- Étape 2 : le plan est présenté puis approuvé avant l'étape 3 ; sans approbation, STOP et rien n'est modifié.
- Étape 3 : seule la proposition de configuration reste à approuver.
- `kr validate` passe.

## History

- 2026-11-16T13:36:55+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T13:37:53+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T13:37:53+01:00 — Merge approved for the verified candidate `0f4df1cea1689bc9e044590cd67f78184d4ccdd6`: “oui valide et commit.”.
