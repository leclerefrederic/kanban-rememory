---
id: "CARD-00000220"
module: "orchestrator"
---

# CARD-00000220 — INSTALL.md : ne détruit rien et ne valide pas un dossier invalide

- Dependencies: None. Fait suite à la Card 219 et à l'essai en dépôt déjà rempli.

## Expected outcome

`dist/INSTALL.md` : (1) en mode install, un dossier `kanban-rememory/` déjà présent arrête l'installation avant tout changement, au lieu d'être supprimé ; (2) quand l'utilisateur garde un dossier de travail existant, la procédure refuse, avant le commit, ce qui ferait échouer `kr validate` : entrée de `modules/` qui n'est pas un module choisi, entrée de `modules/<module>/` qui n'est ni une étape ni `resources`, fichier `.md` dans un dossier d'étape, lien symbolique. Les chemins fautifs sont montrés, puis l'utilisateur choisit un autre nom.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « Oui, corrige ».

## Acceptance criteria

- Le plan de la section 2 ne peut plus afficher `kanban-rememory/ replaced` en mode install.
- Un dossier de travail qui ferait échouer `kr validate` est refusé avant toute écriture.
- `kr validate` passe.
