---
id: "CARD-00000207"
module: "orchestrator"
---

# CARD-00000207 — Fusionner les deux lignes du dossier du kit dans install.md

- Dependencies: None. Fait suite à la Card 206.

## Expected outcome

Dans le tableau « Kit contents » de `install.md`, les lignes `kanban-rememory/orchestrator/` et `kanban-rememory/documentation/` forment une seule ligne `kanban-rememory/`.

## Scope and authorization

`install.md`, ce tableau seulement. Demande de l'utilisateur.

## Scope change

Décision de l'utilisateur : « on continue les modifications » ; s'ajoutent les six écarts de la relecture d'`install.md` : `name` demandé, permissions dans `GUARDRAILS.md`, définition de DIR, version du kit, droit de push et `__pycache__/`, vérification du chat neuf par l'utilisateur.

## Acceptance criteria

- Une ligne `kanban-rememory/` : « procedure, tools, templates, user guide, lean principles, Telegram guide », action « replace with the folder from KIT ».
- `kr validate` passe.

## History

- 2026-11-16T13:55:39+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T13:56:42+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T13:56:42+01:00 — Merge approved for the verified candidate `d8624e7ec5a7fbdbb58839ff26c39c6b7dd2c52d`: “corrige les 6 points. et commit.”.
