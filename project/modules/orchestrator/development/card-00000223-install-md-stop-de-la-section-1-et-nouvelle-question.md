---
id: "CARD-00000223"
module: "orchestrator"
---

# CARD-00000223 — INSTALL.md : STOP de la section 1 et nouvelle question

- Dependencies: None. Fait suite à la Card 222 et à la série d'essais E à H.

## Expected outcome

`dist/INSTALL.md` : (1) la section 1 lance tous les contrôles même après un échec, puis s'arrête en listant tous ceux qui échouent, chacun avec sa consigne de correction ; (2) les lignes Python, Branch, Clean checkout et Remote ont leur consigne ; (3) une réponse invalide à la section 3 est redemandée en un seul message pour tous les champs invalides.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « Oui, corrige ».

## Acceptance criteria

- Les trois points sont écrits sans équivoque.
- `kr validate` passe.

## History

- 2026-11-16T18:52:24+01:00 — Stage moved from `backlog` to `development`.
