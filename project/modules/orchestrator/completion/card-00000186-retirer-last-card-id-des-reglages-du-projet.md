---
id: "CARD-00000186"
module: "orchestrator"
---

# CARD-00000186 — Retirer last_card_id des réglages du projet

- Dependencies: Aucune.

## Expected outcome

`project/settings.json` ne contient plus `last_card_id`. L'identifiant d'une nouvelle Card est le plus grand identifiant des Cards existantes, plus un.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, après l'analyse des réglages et le test de suppression du manifeste (« if removing it loses no value and no needed protection, remove it ») : retirer `last_card_id`, l'exécuter et fusionner dans `main` (accord de fusion donné dans la demande).

Constat : `kr new` calcule déjà le maximum des Cards existantes (`board.py`). Le champ ne servait que de plancher si des Cards disparaissaient du dépôt, ce que la règle 6 interdit. Ici il valait 172 pour des Cards allant jusqu'à 187, sans conséquence.

Perte acceptée : dans un projet dont des Cards auraient été supprimées hors de KR, un identifiant supprimé pourrait être réattribué.

Le travail comprend :

- le code : `last_card_id` n'est plus une clé requise, n'est plus validée ni stockée, et `kr new` part de zéro ;
- la compatibilité : un `settings.json` déjà installé qui contient encore la clé reste valide, et la clé est ignorée ;
- `project/settings.json` de ce dépôt, `orchestrator/install.md` et `orchestrator/tools/test-kr.py`.

Hors périmètre, à décider séparément : `workflow.completed` (constante `completion` à l'installation) et `schema_version`, conservés.

## Acceptance criteria

- `kr new` donne le numéro suivant le plus grand identifiant existant, ou `00000001` sur un dépôt sans Card.
- Un `settings.json` sans `last_card_id` est accepté ; un `settings.json` qui le contient encore l'est aussi, et la valeur n'a aucun effet sur la numérotation.
- `project/settings.json` ne contient plus la clé, et `install.md` ne la mentionne plus.
- `validate` et `test-kr.py` passent.

## History

- 2026-11-16 — Décision de l'utilisateur : retirer `last_card_id`, exécuter la Card et fusionner dans `main`.

- 2026-11-16T08:40:27+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T08:41:17+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T08:41:17+01:00 — Merge approved for the verified candidate `df124b7d79de1d791b3e2d0a2a0971ed69caa767`: “Oui, crée la Card dans le backlog execute la et fusionne sur main.”.
