---
id: "CARD-00000187"
module: "orchestrator"
---

# CARD-00000187 — Retirer la tolérance de l'ancienne clé last_card_id

- Dependencies: Aucune.

## Expected outcome

`kr` n'accepte plus `last_card_id` dans `project/settings.json` : le fichier doit contenir exactement les clés `schema_version`, `name`, `modules`, `workflow` et `version`.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : retirer la compatibilité ajoutée par CARD-00000186, puisqu'aucun autre projet n'est installé, l'exécuter et fusionner dans `main` (accord de fusion donné dans la demande).

Le travail comprend `LEGACY_KEYS` et le contrôle de clés dans `orchestrator/tools/kanban/project.py`, et le test de `orchestrator/tools/test-kr.py` qui écrivait la clé.

Hors périmètre : `schema_version` et la section « Upgrade » de `install.md`. CARD-00000169 les garde comme seul repère de la version du kit installée dans un projet ; l'utilisateur peut décider de les retirer dans une Card séparée.

## Acceptance criteria

- Un `settings.json` qui contient `last_card_id` est refusé avec le message des clés exactes.
- Un `settings.json` avec les cinq clés est accepté.
- `validate` et `test-kr.py` passent.

## History

- 2026-11-16 — Décision de l'utilisateur : retirer la tolérance, exécuter la Card et fusionner dans `main`.

- 2026-11-16T08:42:42+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T08:43:08+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T08:43:08+01:00 — Merge approved for the verified candidate `4b5ca8af91b113035297060d4226b9c076ac5b0f`: “Oui, crée la Card, exécute-la et fusionne sur main.”.
