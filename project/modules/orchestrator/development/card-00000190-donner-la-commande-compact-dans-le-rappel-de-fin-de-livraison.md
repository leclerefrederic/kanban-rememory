---
id: "CARD-00000190"
module: "orchestrator"
---

# CARD-00000190 — Donner la commande /compact dans le rappel de fin de livraison

- Dependencies: Aucune.

## Expected outcome

Le rappel de fin de livraison nomme la commande à taper, pour qu'un utilisateur néophyte sache comment compacter la session ou en ouvrir une nouvelle.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, successeur de CARD-00000182 : modifier la dernière phrase du paragraphe Publish de `orchestrator/workflow.md`. Travail sur `main`.

- Le rappel cite `/compact` pour compacter et `/clear` pour repartir d'une session vide (Claude Code), en une ligne.
- Hors périmètre : hook, alerte Telegram, code de `kr`.

## Acceptance criteria

- `workflow.md` contient les deux commandes dans la phrase de rappel.
- `validate` passe.

## History

- 2026-11-16T08:50:22+01:00 — Stage moved from `backlog` to `development`.
