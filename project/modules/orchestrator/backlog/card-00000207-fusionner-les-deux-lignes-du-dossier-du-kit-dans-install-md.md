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

## Acceptance criteria

- Une ligne `kanban-rememory/` : « procedure, tools, templates, user guide, lean principles, Telegram guide », action « replace with the folder from KIT ».
- `kr validate` passe.
