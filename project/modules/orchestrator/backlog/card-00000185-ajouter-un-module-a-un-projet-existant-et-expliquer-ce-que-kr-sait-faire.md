---
id: "CARD-00000185"
module: "orchestrator"
---

# CARD-00000185 — Ajouter un module à un projet existant et expliquer ce que KR sait faire

- Dependencies: Aucune.

## Expected outcome

Un projet qui grandit peut ajouter un module sans modifier les fichiers à la main, et l'utilisateur qui demande à l'agent ce que KR sait faire reçoit toujours le même texte.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : développer la capacité d'ajouter un module, sans que l'Orchestrator en propose la création de lui-même (cela alourdirait le workflow). Le travail comprend :

- une commande `kr module add <id>` qui ajoute l'ID à `project/settings.json`, crée les dossiers de stages du module et lance `validate` ;
- une section `## What you can ask` dans `documentation/guide.md`, fusionnée avec la table « Give work » pour ne pas la dupliquer, avec une phrase type par capacité et sans nom de commande ;
- une phrase dans `orchestrator/workflow.md` : à la question « que sait faire KR ? », l'agent affiche cette section telle quelle, sans la reformuler.

Hors périmètre : toute proposition automatique de module, tout déplacement de Cards existantes de `misc`, toute commande `/kr` propre à un hôte.

Card créée dans le backlog sur demande explicite, sans démarrage.

## Acceptance criteria

- `kr module add <id>` refuse un ID invalide, déjà présent ou absent du format des modules, et n'écrit rien dans ce cas.
- Après `kr module add <id>`, `settings.json` liste le module, ses dossiers de stages existent et `kr show` l'affiche avec son WIP.
- `kr new --module <id>` crée une Card dans le nouveau module.
- Les Cards existantes ne sont pas déplacées.
- `guide.md` contient la section `What you can ask`, sans doublon avec « Give work », et `workflow.md` y renvoie par une ancre que `validate` vérifie.
- `test-kr.py` couvre le succès et les refus de `kr module add`.

## History

- 2026-11-16 — Décision de l'utilisateur : développer la capacité, ne pas faire proposer le module par l'Orchestrator, et laisser la Card dans le backlog.
