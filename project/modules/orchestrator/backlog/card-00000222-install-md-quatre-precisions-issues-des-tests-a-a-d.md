---
id: "CARD-00000222"
module: "orchestrator"
---

# CARD-00000222 — INSTALL.md : quatre précisions issues des tests A à D

- Dependencies: None. Fait suite à la Card 221 et aux quatre essais en bac à sable.

## Expected outcome

`dist/INSTALL.md` : (1) le plan dit `GUARDRAILS.md` `created` s'il est absent, `kept` s'il existe, avec la mention des permissions en mode install ; (2) en mode upgrade, `kit` s'ajoute par insertion d'une ligne sans reformater `kanban-rememory.json` ; (3) `N lines appended` compte les lignes non vides ajoutées ; (4) `HH:MM` du journal est l'heure du fuseau du projet.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « Oui, corrige ».

## Acceptance criteria

- Les quatre points sont écrits sans équivoque.
- `kr validate` passe.
