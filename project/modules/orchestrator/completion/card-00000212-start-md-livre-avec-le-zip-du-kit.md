---
id: "CARD-00000212"
module: "orchestrator"
---

# CARD-00000212 — START.md livré avec le ZIP du kit

- Dependencies: None. Fait suite à la Card 211.

## Expected outcome

`build-kit.py` écrit `dist/START.md` à côté du ZIP : trois étapes pour démarrer une installation (décompresser hors du dépôt cible, ouvrir l'agent dans le dépôt, lui donner la phrase qui pointe vers `install.md`), avec la version et le nom du ZIP.

## Scope and authorization

Modèle `kanban-rememory/orchestrator/templates/start.md`, `build-kit.py`, son test. `START.md` est livré à côté du ZIP, pas dedans ni dans Git. Demande de l'utilisateur : « Fais le START.md et mets-le dans dist, régénère le zip aussi ».

## Acceptance criteria

- `dist/START.md` contient la version et le chemin `install.md` du kit.
- Le ZIP est régénéré.
- `kr validate` passe.

## History

- 2026-11-16T14:42:15+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T14:43:14+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T14:43:14+01:00 — Merge approved for the verified candidate `e1cd9a855c4df0518c5e322d20ebc83d593d29d5`: “Oui, commit”.
