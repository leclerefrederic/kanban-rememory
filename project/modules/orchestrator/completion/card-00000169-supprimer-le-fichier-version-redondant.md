---
id: "CARD-00000169"
module: "orchestrator"
---

# CARD-00000169 — Supprimer le fichier VERSION redondant

- Dependencies: Aucune. Suit CARD-00000168.

## Expected outcome

Le kit ne porte plus de numéro de version manuel que rien ne lit. La mise à jour d’un projet installé repère le format par `schema_version` dans `project/settings.json`.

## Scope and authorization

Constat du 2026-11-15 : aucun outil ne lit `orchestrator/VERSION`, seul `orchestrator/install.md` le cite, et `schema_version` couvre déjà la migration des réglages. Décision de l’utilisateur le même jour : « Oui, supprime ». La demande autorise l’exécution. Supprimer le fichier et ses mentions dans `install.md` ; la note de migration vise le schéma 1 des réglages.

## Acceptance criteria

- [x] `orchestrator/VERSION` n’existe plus et aucun fichier hors historique ne le cite.
- [x] `install.md` décrit la mise à jour depuis le schéma 1 des réglages, sans numéro de version.
- [x] `validate` passe.

## Execution and evidence

- State: done
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur.

- 2026-11-15T23:31:41+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — `orchestrator/VERSION` supprimé ; `install.md` repère la version installée par `schema_version`. Seule de la documentation change : `validate` suffit.

- 2026-11-15T23:32:44+01:00 — Stage moved from `development` to `completion`.

- 2026-11-15T23:32:44+01:00 — Merge approved for the verified candidate `6026b8d08b0244e083836a1009499b3bcf592a8b`: “Oui, fusionne”.
- 2026-11-15 — Alerte Remy `merge-6026b8d08b0244e083836a1009499b3bcf592a8b` envoyée avant l’accord : livraison confirmée par Telegram.
