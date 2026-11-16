---
id: "CARD-00000219"
module: "orchestrator"
---

# CARD-00000219 — Fermer quatre écarts restants d'INSTALL.md

- Dependencies: None. Fait suite à la Card 218 et au second essai en bac à sable.

## Expected outcome

`dist/INSTALL.md` dit : que les modèles `.gitignore` et `.gitattributes` sont des fichiers cachés ; que la liste `modules` du JSON contient toujours `misc` en dernier, donc `["misc"]` par défaut ; qu'un fichier existant sans saut de ligne final en reçoit un avant l'ajout ; que `init --apply` se lance sans tube pour lire son code de sortie.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « traite les points 1 à 4 ».

## Acceptance criteria

- Les quatre points sont écrits sans équivoque dans `INSTALL.md`.
- `kr validate` passe.
