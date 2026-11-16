---
id: "CARD-00000214"
module: "orchestrator"
---

# CARD-00000214 — INSTALL.md et ZIP suivis dans dist/, START.md supprimé

- Dependencies: None. Fait suite à la Card 213.

## Expected outcome

`dist/` est la version distribuée du kit, choisie par l'utilisateur indépendamment du développement en cours : `dist/INSTALL.md` (la procédure, écrite à la main, sortie du kit) et le ZIP, tous deux suivis par Git. L'utilisateur dépose les deux à la racine de son dépôt et dit à son agent « Follow INSTALL.md ». `START.md`, son modèle et leur génération disparaissent. Le ZIP n'est reconstruit que sur demande, par `build-kit.py`.

## Scope and authorization

`install.md` déplacé en `dist/INSTALL.md` (étape 0 : décompresser le ZIP hors du dépôt ; liens remplacés par des chemins dans le kit), `build-kit.py` et son test, `start.md` supprimé, `.gitignore`, message d'erreur de `project.py`, ZIP 0.1.0 construit et commité. Décisions de l'utilisateur : « on peut sortir install du dossier KR et le mettre dans dist », « dist doit être suivi dans Git », « le zip est commit, c'est intentionnel : je décide de la version distribuée ».

## Acceptance criteria

- `kanban-rememory/orchestrator/install.md` et `templates/start.md` n'existent plus ; `dist/INSTALL.md` et `dist/kanban-rememory-kit-0.1.0.zip` sont suivis.
- Le ZIP ne contient pas `INSTALL.md`.
- `kr validate` passe.

## History

- 2026-11-16T14:58:41+01:00 — Stage moved from `backlog` to `development`.
