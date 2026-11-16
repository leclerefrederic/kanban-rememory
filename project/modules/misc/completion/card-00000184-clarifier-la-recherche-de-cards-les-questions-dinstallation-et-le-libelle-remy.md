---
id: "CARD-00000184"
module: "misc"
affected_modules: ["orchestrator", "notifications"]
---

# CARD-00000184 — Clarifier la recherche de Cards, les questions d’installation et le libellé Remy

- Dependencies: None.

## Résultat attendu

Les instructions d’intake et d’installation évitent les appels et échanges superflus. Le guide Telegram indique le titre réellement affiché.

## Périmètre et autorisation

Les trois corrections textuelles de l’audit sont autorisées par « Fais les 3 corrections dans ce cas. » L’utilisateur a choisi `main`. Modules concernés (`affected_modules`) : orchestrator et notifications. Aucun changement du code ni des fichiers Graphify.

## Critères d’acceptation

- Le workflow réserve `kr path` aux identifiants connus et décrit quand rechercher dans l’historique.
- Les deux guides d’installation regroupent les questions indépendantes avec des valeurs proposées et gardent les questions dépendantes dans l’ordre utile.
- Le guide Telegram reprend le libellé anglais émis par Remy.

## History

- 2026-11-16T07:44:27+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T07:50:44+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T07:50:44+01:00 — Merge approved for the verified candidate `1e5c93a296328d8925e027f188eef4394dd613c8`: “Oui, publie 1e5c93a sur origin/main.”.
