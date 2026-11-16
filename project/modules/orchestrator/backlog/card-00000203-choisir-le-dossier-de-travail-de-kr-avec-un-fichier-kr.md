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
- `install.md` : l'étape 2 teste le dossier choisi, l'étape 3 le demande (défaut `project`), l'étape 4 écrit `.kr` si le nom diffère.
- Tests de `kr.py` et `kr validate` passent.
