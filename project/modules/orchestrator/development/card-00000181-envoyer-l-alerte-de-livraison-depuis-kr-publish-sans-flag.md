---
id: "CARD-00000181"
module: "orchestrator"
---

# CARD-00000181 — Envoyer l'alerte de livraison depuis kr publish sans flag

- Dependencies: Aucune.

## Expected outcome

`kr publish` envoie l'alerte Remy `completed` (id `delivery`) de lui-même quand Telegram est configuré, sans `--notify`. Les livraisons ne passent plus sans notification.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : aucune notification de livraison entre les Cards 172 et 180, parce que l'alerte ne partait que si `--notify` était passé. L'exception « pas d'alerte de merge quand l'approbation est dans la demande » reste en place : elle ne concerne pas la livraison.

- `publish` envoie l'alerte quand `telegram.py status` montre une configuration ; sans configuration, il n'envoie rien, comme aujourd'hui.
- `--summary` devient obligatoire quand Telegram est configuré : c'est le texte de l'alerte.
- `--notify` devient facultatif et nomme le chat ; sans lui, le nom du chat est le nom du projet (`settings.json`).
- Un échec d'envoi est signalé clairement ; la publication reste faite. Une nouvelle exécution de `publish` n'envoie pas de doublon (ledger).
- Mettre à jour `orchestrator/notify.md` et `orchestrator/workflow.md` : l'alerte de livraison ne dépend plus du flag.
- Hors périmètre : alertes rétroactives pour les Cards 172 à 180.

## Acceptance criteria

- `publish` sans `--notify`, Telegram configuré, envoie l'alerte `completed` avec le nom du projet comme chat.
- `publish --notify "Chat"` envoie l'alerte avec ce nom de chat.
- Telegram non configuré : `publish` aboutit sans alerte et sans erreur.
- Telegram configuré et `--summary` absent : `publish` refuse avant toute écriture.
- Un échec d'envoi est signalé et n'annule pas la publication ; une relance n'envoie pas de doublon.
- `notify.md` et `workflow.md` décrivent le nouveau comportement.
- `test-kr.py`, `test-telegram.py` et `validate` passent.

## History

- 2026-11-16T01:05:45+01:00 — Stage moved from `backlog` to `development`.
