---
id: "CARD-00000206"
module: "orchestrator"
---

# CARD-00000206 — Détecter l'installation existante par kanban-rememory.json

- Dependencies: None. Fait suite à la Card 205.

## Expected outcome

Dans `install.md`, la présence de `kanban-rememory.json` à la racine signale une installation existante (mode upgrade) et donne le dossier de travail, les modules et le workflow. Son absence signale une nouvelle installation.

## Scope and authorization

`install.md` seulement. Décision de l'utilisateur : le fichier de configuration, et non le dossier `kanban-rememory/`, sert à détecter une installation.

## Acceptance criteria

- Étape 2 : fichier présent = upgrade, absent = install ; plus de STOP sur « projet sans kit ».
- En upgrade, `kanban-rememory/` est remplacé en bloc, ou installé s'il manque ; le fichier et le dossier de travail restent, sauf `kit`.
- `kr validate` passe.

## History

- 2026-11-16T13:54:17+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T13:54:35+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T13:54:35+01:00 — Merge approved for the verified candidate `e345e81aaadec39cba61b53f49b191389a68db5b`: “commit”.
