# TASK-0001 — Intégrer les pratiques Kanban au kit générique

- Propriétaire : demandeur
- Dépendances : aucune
- Accord d’inscription et autorisation d’exécution : « Oui fait », 2026-11-10

## Résultat attendu

Permettre à un projet de configurer son flux et de suivre une carte de sa sélection à sa clôture.

## Critères d’acceptation

- [x] Le guide définit les choix à faire pour adopter le flux et ses règles de passage.
- [x] Le guide couvre la sélection par capacité et le traitement des blocages.
- [x] Les modèles et le guide permettent de calculer les quatre mesures et de revoir le flux.
- [x] Les conventions du projet sont séparées des pratiques communes.

## Exécution et preuves

- Début réel et fin réelle : 2026-11-10, Europe/Paris.
- Base Git vérifiée : `285e5c2`. Livrables dans les modifications locales.
- Parcours vérifié : une carte démarrée occupe l’unique place, reste comptée pendant un blocage, puis libère la place à sa clôture. Sur un exemple commencé le 10 et terminé le 14, son âge au 12 est de 2 jours, son temps de cycle de 4 jours et sa clôture ajoute une unité au débit.
- Contrôles locaux : structure des colonnes, unicité de la carte, champs du modèle et `git diff --check`.
- [Journal du jalon](../../Rememory/2026-11-10.md).
