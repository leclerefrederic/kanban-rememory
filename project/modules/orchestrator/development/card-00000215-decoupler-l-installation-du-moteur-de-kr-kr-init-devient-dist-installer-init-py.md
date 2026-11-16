---
id: "CARD-00000215"
module: "orchestrator"
---

# CARD-00000215 — Découpler l'installation du moteur de KR : kr init devient dist/installer/init.py

- Dependencies: None. Fait suite à la Card 214.

## Expected outcome

Le moteur `kr` ne contient plus rien d'installation : la sous-commande `init`, `init()` et `check_new_workflow` de `kanban/project.py` et leur test disparaissent de `kanban-rememory/`. Le script d'installation vit dans `dist/installer/init.py`, autonome (il ne partage aucun code avec `kr`), avec son test `dist/installer/test-init.py`. `build-kit.py` le place dans le ZIP à `<dossier>/installer/init.py`, hors de `kanban-rememory/`. Comme il n'a plus besoin du kit installé, `INSTALL.md` lance l'aperçu avant l'approbation de la proposition.

## Scope and authorization

`kr.py`, `kanban/project.py`, `test-kr.py` (les fixtures créent leurs tableaux elles-mêmes), `dist/installer/init.py` et son test, `dist/build-kit.py` et son test, `dist/INSTALL.md`, ZIP reconstruit. Décisions de l'utilisateur : « tous les scripts d'install ou les ressources d'installation vont dans dist », « on décorrèle l'installation de l'engine de KR ».

## Acceptance criteria

- `kr init` n'existe plus ; `kr validate` valide ce que `init.py` a écrit (test de bout en bout).
- Le ZIP contient `installer/init.py` et rien d'autre hors de `kanban-rememory/`.
- `INSTALL.md` : aperçu en section 3 avant l'approbation, `--apply` en section 4.
- `kr validate` passe.

## History

- 2026-11-16T15:02:21+01:00 — Stage moved from `backlog` to `development`.
