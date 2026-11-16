---
id: "CARD-00000185"
module: "orchestrator"
---

# CARD-00000185 — Ajouter un module à un projet existant et expliquer ce que KR sait faire

- Dependencies: Aucune.

## Expected outcome

Un projet qui grandit sait comment ajouter un module, et l'utilisateur qui demande à l'agent ce que KR sait faire reçoit toujours le même texte.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : documenter la capacité d'ajouter un module, sans que l'Orchestrator en propose la création de lui-même (cela alourdirait le workflow). Aucun code : un essai sur une copie du dépôt a montré qu'ajouter l'ID à `modules` dans `project/settings.json` suffit. `validate` passe, `kr show` affiche le module avec le WIP du projet, `kr new --module <id>` crée la Card et les dossiers. Un ID invalide est déjà refusé par `validate`. Une commande `kr module add` n'apporterait rien de plus et est écartée.

Le travail comprend :

- une section `## What you can ask` dans `documentation/guide.md`, fusionnée avec la table « Give work » pour ne pas la dupliquer, avec une phrase type par capacité et sans nom de commande, dont l'ajout d'un module avec l'accord de l'utilisateur ;
- une phrase dans `orchestrator/workflow.md` : à la question « que sait faire KR ? », l'agent affiche cette section telle quelle, sans la reformuler ; et pour ajouter un module, il ajoute l'ID à `modules` dans `project/settings.json` avec l'accord de l'utilisateur, puis lance `validate`.

Hors périmètre : toute proposition automatique de module, toute commande `kr module`, tout déplacement de Cards existantes de `misc`, toute commande `/kr` propre à un hôte.

Card créée dans le backlog sur demande explicite, sans démarrage.

## Acceptance criteria

- `guide.md` contient la section `What you can ask`, sans doublon avec « Give work ».
- `workflow.md` y renvoie par une ancre que `validate` vérifie, et indique comment ajouter un module.
- Suivre cette consigne sur une copie du dépôt ajoute un module : `validate` passe et `kr show` l'affiche.
- Les Cards existantes ne sont pas déplacées.

## History

- 2026-11-16 — Décision de l'utilisateur : ne pas faire proposer le module par l'Orchestrator, et laisser la Card dans le backlog.
- 2026-11-16 — Décision de l'utilisateur : retirer `kr module add` après l'essai sur une copie, la Card devient de la documentation seule.

- 2026-11-16T08:21:41+01:00 — Stage moved from `backlog` to `development`.
