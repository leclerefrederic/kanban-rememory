---
id: "CARD-00000230"
module: "notifications"
---

# CARD-00000230 — Envoyer les alertes Remy dans Slack

- Dependencies: Aucune.

## Résultat attendu

Recevoir les alertes Remy dans le salon Slack personnel choisi avec un webhook entrant. L’utilisateur a demandé de travailler sur une branche de release.

## Critères d’acceptation

- Configurer le webhook par saisie masquée et le conserver hors du dépôt.
- Envoyer sur Slack les alertes d’intervention, d’approbation et de livraison lorsque Slack est configuré. Utiliser Telegram si seul Telegram est configuré.
- Conserver l’aperçu, la déduplication et le traitement des livraisons incertaines.
- Documenter la configuration et la commande de test. Vérifier les envois par simulation.

## History

- 2026-11-17T11:25:01+01:00 — Stage moved from `backlog` to `development`.
