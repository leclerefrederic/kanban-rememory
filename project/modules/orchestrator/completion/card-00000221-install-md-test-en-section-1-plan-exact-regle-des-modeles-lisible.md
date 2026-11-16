---
id: "CARD-00000221"
module: "orchestrator"
---

# CARD-00000221 — INSTALL.md : test en section 1, plan exact, règle des modèles lisible

- Dependencies: None. Fait suite à la Card 220 et aux deux essais en dépôt rempli.

## Expected outcome

`dist/INSTALL.md` : (1) le contrôle « `kanban-rememory/` existe sans CONFIG » est un prérequis de la section 1, et un STOP supprime les dossiers temporaires créés ; (2) le message de STOP dit de committer le déplacement ou la suppression ; (3) le plan n'annonce « lines appended » que pour des lignes réellement ajoutées ; (4) la règle des modèles garde une ligne vide entre deux blocs ajoutés dans un fichier Markdown ; (5) les `.gitkeep` créés par `init` sont dits suivis ; (6) un contrôle de dossier de travail qui échoue renvoie sans « Confirm? » à la saisie d'un autre nom.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « corrige les points 1 à 6 ».

## Acceptance criteria

- Les six points sont écrits sans équivoque dans `INSTALL.md`.
- `kr validate` passe.

## History

- 2026-11-16T18:37:51+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T18:38:19+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T18:38:19+01:00 — Merge approved for the verified candidate `0570523826c8704b76dd8315b752df5ab426b284`: “Oui, commit”.
