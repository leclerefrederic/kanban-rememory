---
id: "CARD-00000204"
module: "orchestrator"
---

# CARD-00000204 — Fusionner les réglages du projet dans kanban-rememory.json

- Dependencies: None. Fait suite à la Card 203.

## Expected outcome

Un seul fichier de configuration à la racine, `kanban-rememory.json`, remplace `project/settings.json`. Il contient `directory` (facultatif, défaut `project`), `kit` (facultatif, version du kit installé), `name`, `modules`, `workflow` et `version` (release du projet). Le dossier de travail ne garde que les Cards et le journal.

## Scope and authorization

`kr` (`project.py`, `phase.py`, `validation.py`, `kr.py`), ses tests, `install.md`, `workflow.md` et le guide. Ce dépôt est migré : `project/settings.json` devient `kanban-rememory.json`. Décisions de l'utilisateur : fusionner les réglages dans ce fichier, `kit` et `version` sont deux champs distincts, `settings.json` est supprimé. Le champ `kit` est écrit par l'installateur et jamais modifié par `kr` ; ce dépôt, qui est le kit, ne l'a pas.

## Acceptance criteria

- `kr init` écrit `kanban-rememory.json` à la racine et crée les tableaux dans `directory`.
- `load_project`, `validate`, `start`, `check` et `publish` lisent ce fichier ; `publish` y relève `version` et le commit de clôture l'inclut.
- Clés inconnues ou `kit` invalide refusées avec un message clair.
- Ce dépôt est migré sans perte ; `kr validate` passe.
- `install.md`, `workflow.md` et le guide parlent de `kanban-rememory.json` ; l'installateur écrit `kit`.
- Tests de `kr.py` et `kr validate` passent.

## History

- 2026-11-16T13:46:30+01:00 — Stage moved from `backlog` to `development`.
