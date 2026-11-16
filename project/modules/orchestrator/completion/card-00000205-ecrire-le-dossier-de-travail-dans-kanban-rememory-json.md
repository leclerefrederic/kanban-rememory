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

## History

- 2026-11-16T13:49:57+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T13:53:32+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T13:53:32+01:00 — Merge approved for the verified candidate `d6636dd00870c44550837f2b8fbfd1a5a8a5fb93`: “commit”.
