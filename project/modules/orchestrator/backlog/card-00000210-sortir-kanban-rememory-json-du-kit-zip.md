---
id: "CARD-00000210"
module: "orchestrator"
---

# CARD-00000210 — Sortir kanban-rememory.json du kit ZIP

- Dependencies: None. Fait suite à la Card 209.

## Expected outcome

Le ZIP ne contient plus `kanban-rememory.json` : c'est la configuration de ce dépôt, pas celle d'un projet cible. Il contient à la place un fichier `VERSION` (la version du kit, ligne unique) à sa racine, et `install.md` lit KIT_VERSION dans `KIT/VERSION`.

## Scope and authorization

`build-kit.py`, son test, `install.md` (définition de KIT et KIT_VERSION, prérequis « KIT is a kit »). Un KIT est désormais l'archive décompressée seulement. Demande de l'utilisateur : « Ça ne doit pas être dans le kit, c'est la conf de mon KR ici ».

## Acceptance criteria

- L'archive n'a pas `kanban-rememory.json` et a `VERSION` avec la version de `HEAD`.
- `install.md` ne mentionne plus `KIT/kanban-rememory.json`.
- `kr validate` passe.

## History
