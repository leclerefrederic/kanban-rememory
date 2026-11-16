---
id: "CARD-00000205"
module: "orchestrator"
---

# CARD-00000205 — Écrire le dossier de travail dans kanban-rememory.json

- Dependencies: None. Fait suite à la Card 204.

## Expected outcome

`kanban-rememory.json` dit toujours où se trouve le dossier de travail : la clé `directory` devient obligatoire, au lieu d'un défaut implicite à `project`.

## Scope and authorization

`kr` (`project.py`), ses tests, `install.md`, `workflow.md` et le fichier de ce dépôt. Décision de l'utilisateur : le fichier doit indiquer littéralement le dossier de travail.

## Acceptance criteria

- Sans `directory`, `kr validate` refuse le fichier avec un message clair.
- Le fichier de ce dépôt contient `"directory": "project"`.
- `install.md` écrit toujours `directory` dans la proposition, `project` par défaut.
- Tests de `kr.py` et `kr validate` passent.
