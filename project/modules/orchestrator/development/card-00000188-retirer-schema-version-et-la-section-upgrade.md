---
id: "CARD-00000188"
module: "orchestrator"
---

# CARD-00000188 — Retirer schema_version et la section Upgrade

- Dependencies: Aucune.

## Expected outcome

`project/settings.json` ne contient plus `schema_version`, et `orchestrator/install.md` ne décrit plus de migration entre schémas.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, après le test de suppression du manifeste (« if removing it loses no value and no needed protection, remove it ») et le constat qu'aucun autre projet n'est installé : retirer `schema_version` et la section « Upgrade ». Card créée dans le backlog, sans démarrage ni fusion tant que l'utilisateur ne les demande pas.

Constat : rien ne s'exécute selon la valeur de `schema_version` ; `parse_settings` refuse seulement tout ce qui n'est pas `2`. Sa seule protection, repérer un projet en schéma 1 à migrer, n'a plus de public.

Conséquence acceptée : CARD-00000169 en faisait le repère de la version du kit installée dans un projet. Sans lui, une future évolution incompatible du format des réglages ne se détecte plus par un marqueur, et la décision de migration revient à cette future Card.

Le travail comprend :

- `orchestrator/tools/kanban/project.py` : retirer la clé de `KEYS`, son contrôle et le renvoi vers `install.md` ;
- `project/settings.json` et la fixture de `orchestrator/tools/test-kr.py` ;
- `orchestrator/install.md` : la mention de `schema_version` à l'étape 1 et la section « Upgrade », titre du fichier compris si besoin.

Hors périmètre : `workflow.completed` et toute autre clé.

## Acceptance criteria

- Un `settings.json` avec exactement `name`, `modules`, `workflow` et `version` est accepté ; un fichier qui contient encore `schema_version` est refusé avec le message des clés exactes.
- `project/settings.json` et `install.md` ne mentionnent plus `schema_version` ni de migration de schéma.
- `validate` et `test-kr.py` passent.

## History

- 2026-11-16 — Décision de l'utilisateur : retirer `schema_version` et la section « Upgrade ».

- 2026-11-16T08:44:16+01:00 — Stage moved from `backlog` to `development`.
