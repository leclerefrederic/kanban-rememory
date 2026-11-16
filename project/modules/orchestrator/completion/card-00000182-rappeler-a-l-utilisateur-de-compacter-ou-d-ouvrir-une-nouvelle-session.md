---
id: "CARD-00000182"
module: "orchestrator"
---

# CARD-00000182 — Rappeler à l'utilisateur de compacter ou d'ouvrir une nouvelle session

- Dependencies: Aucune.

## Expected outcome

Après chaque `kr publish`, le message final de l'agent rappelle en une ligne à l'utilisateur de compacter la session ou d'en ouvrir une nouvelle, pour économiser des tokens.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : règle dans `orchestrator/workflow.md`, pas de hook ni de changement de l'alerte Telegram.

- Ajouter une phrase au paragraphe Publish de `orchestrator/workflow.md` : une fois la livraison vérifiée, le message final dit en une ligne de compacter la session ou d'en ouvrir une nouvelle.
- Hors périmètre : hook Claude Code, texte de l'alerte Telegram, code de `kr`.

## Acceptance criteria

- `workflow.md` contient la règle, dans la langue du fichier, en une phrase.
- `validate` passe.

## History

- 2026-11-16T07:10:37+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T07:11:15+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T07:11:15+01:00 — Merge approved for the verified candidate `9f094df26bb0d2cb7220a29816bc19763852c744`: “Approuvé”.
