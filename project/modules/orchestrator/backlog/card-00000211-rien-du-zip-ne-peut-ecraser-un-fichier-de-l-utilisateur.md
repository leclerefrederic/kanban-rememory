---
id: "CARD-00000211"
module: "orchestrator"
---

# CARD-00000211 — Rien du ZIP ne peut écraser un fichier de l'utilisateur

- Dependencies: None. Fait suite à la Card 210.

## Expected outcome

Tout le contenu du ZIP est sous `kanban-rememory/`, le seul dossier que le kit remplace. `AGENTS.md`, `CLAUDE.md` et `GUARDRAILS.md` ne sont plus à la racine de l'archive : même déplacé à la racine d'un dépôt, le contenu ne peut écraser aucun fichier de l'utilisateur. Le modèle de `GUARDRAILS.md` est dans `kanban-rememory/orchestrator/templates/`, la version du kit dans `kanban-rememory/VERSION`.

## Scope and authorization

`build-kit.py`, son test, `install.md` (définition de KIT_VERSION, source de `GUARDRAILS.md`, prérequis, tableau du kit). Demande de l'utilisateur : « s'il décompresse le zip... il peut écraser son agents.md etc... ».

## Acceptance criteria

- Tous les noms de l'archive sont sous `<dossier>/kanban-rememory/`.
- `install.md` ne cite plus `KIT/AGENTS.md`, `KIT/CLAUDE.md`, `KIT/GUARDRAILS.md` ni `KIT/VERSION`.
- `kr validate` passe.

## History
