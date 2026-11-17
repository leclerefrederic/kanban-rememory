---
id: "CARD-00000233"
module: "misc"
---

# CARD-00000233 — Mettre à jour la documentation et le wiki pour Remy v0.2.0

- Dependencies: CARD-00000229, CARD-00000230, CARD-00000231, CARD-00000232.
- affected_modules: `notifications`, `orchestrator`.

## Résultat attendu

Le wiki GitHub et la documentation du dépôt décrivent le kit v0.2.0 et les réglages actuels de Remy.

## Critères d’acceptation

- Mettre à jour le wiki en anglais, notamment les pages d’installation, de notifications et d’aide qui renvoient à l’ancien kit ou à la commande Telegram.
- Vérifier les autres pages du wiki et la documentation du dépôt. Corriger les liens ou instructions obsolètes qui concernent l’installation v0.2.0 et Remy.
- Décrire la commande `notifications.py`, la configuration Slack et Telegram, les flags `configured` et `active`, ainsi que la désactivation d’un canal et l’activation des deux.
- Vérifier les liens de téléchargement, les commandes et les exemples de configuration avec le kit publié.

## Resources

- [Wiki GitHub](https://github.com/leclerefrederic/kanban-rememory/wiki)
- [Procédure d’installation](../../../../dist/INSTALL.md)
- [Guide utilisateur](../../../../kanban-rememory/documentation/guide.md)

## Vérification

Révision publiée du wiki : `b12141a4acb1da43f16f024f2414d05aa398dce4`. Les 41 liens internes et cibles du dépôt, le ZIP, les commandes et l’exemple JSON ont été vérifiés. La révision a été confirmée sur le dépôt GitHub du wiki.

## History

- 2026-11-17T11:52:01+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-17T11:55:12+01:00 — Stage moved from `development` to `completion`.

- 2026-11-17T11:55:12+01:00 — Merge approved for the verified candidate `cf4898fda0ef70b430276045f7ce77be3955508c`: “publie”.
