---
id: "CARD-00000232"
module: "notifications"
---

# CARD-00000232 — Configurer les canaux Remy par dépôt

- Dependencies: CARD-00000231.

## Critères d’acceptation

- Les paramètres du dépôt et le modèle d’installation déclarent séparément si Slack et Telegram sont configurés et actifs.
- Les alertes de Remy peuvent aller à Slack, Telegram, aux deux ou à aucun. Désactiver un service conserve sa configuration privée.
- Un échec sur un service ne bloque pas l’autre. Tester la sélection, la validation et la publication sans réseau réel.

## History

- 2026-11-17T11:39:47+01:00 — Stage moved from `backlog` to `development`.
