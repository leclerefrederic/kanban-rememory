---
id: "CARD-00000226"
module: "orchestrator"
---

# CARD-00000226 — Corriger la référence à test-telegram.py que le kit installé ne contient plus

- Dependencies: None. Régression de la Card 225, trouvée par l'essai de mise à jour.

## Expected outcome

`kr validate` passe dans un projet installé depuis le ZIP. `telegram-setup.md` ne cite plus le chemin de `test-telegram.py` (absent du kit) sous une forme que `validate` lit comme un outil à vérifier ; ZIP reconstruit.

## Scope and authorization

`kanban-rememory/documentation/telegram-setup.md`, ZIP. Défaut introduit par la Card 225 ; correction à la suite des essais demandés (« jusqu'à ce que tout passe »).

## Acceptance criteria

- `kr validate` passe dans un dépôt où le ZIP est installé.
- `kr validate` passe dans ce dépôt.

## History

- 2026-11-16T19:19:43+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T19:35:08+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T19:35:08+01:00 — Merge approved for the verified candidate `588c49ecbdae2d36783441d8a9463c27c3e9c31a`: “Oui, commit”.
