---
id: "CARD-00000203"
module: "orchestrator"
---

# CARD-00000203 — Choisir le dossier de travail de KR avec un fichier .kr

- Dependencies: None.

## Expected outcome

Le dossier où KR range ses Kanbans (`settings.json`, `modules/`, `rememory/`) n'est plus figé à `project/`. Un fichier `.kr` à la racine du dépôt en donne le nom ; sans fichier, le défaut reste `project`.

## Scope and authorization

`kr` (`kanban/project.py`, `phase.py`, `validation.py`), ses tests, `install.md`, le guide et le workflow. Le nom du dossier est un seul segment, sans point initial, différent de `kanban-rememory`. Décision de l'utilisateur : le réglage vit dans un fichier à la racine.

## Acceptance criteria

- Avec `.kr` contenant `work`, `kr init`, `show`, `validate`, `new`, `start`, `check` et `publish` utilisent `work/`.
- Sans `.kr`, le comportement est inchangé (`project/`).
- Un nom invalide dans `.kr` est refusé avec un message clair.
- `install.md` : le dossier est DIR (nom dans `.kr`, `project` par défaut). Si DIR existe sans `kanban-rememory/`, l’étape 2 s’arrête et demande un autre nom dans `.kr`. Aucune question de plus à l’étape 3.
- Tests de `kr.py` et `kr validate` passent.

## History

- 2026-11-16T13:41:22+01:00 — Stage moved from `backlog` to `development`.
