# Instructions de travail

## Reprendre

1. Lire le [guide Kanban](kanban/README.md) et examiner les cartes en cours, puis le backlog pertinent.
2. Identifier la carte et son propriétaire. Lire le dernier Rememory pertinent, les spécifications et l’état Git avant de poursuivre.
3. Vérifier les dépendances et reprendre à la prochaine action autorisée. Signaler tout écart entre la carte, le journal et les preuves.

## Exécuter

- Chercher une carte correspondante dans toutes les colonnes avant d’en proposer une. Qualifier le résultat, le périmètre, le propriétaire, les dépendances et les critères vérifiables.
- Enregistrer en backlog après accord. Passer en cours avant de modifier les livrables, une fois l’exécution autorisée. Une carte ou une spécification approuvée ne vaut pas autorisation de développer ou de publier.
- Mettre à jour le [journal du propriétaire](Rememory/README.md) à chaque jalon significatif. À la clôture, vérifier les critères et consigner les preuves, la révision et la suite. Distinguer les tests, la fusion, la publication, le déploiement et la validation utilisateur.
- Suivre les autorisations Git du dépôt. En leur absence, conserver les modifications localement jusqu’à autorisation de publier. Signaler les traces qui n’ont pas pu être écrites.

## Conventions par défaut

Préfixe des cartes : `TASK`. Journal : `Rememory/` à la racine pour un seul propriétaire. Utiliser la date du projet et préciser son fuseau à l’adoption.
