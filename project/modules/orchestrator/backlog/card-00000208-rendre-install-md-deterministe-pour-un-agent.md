---
id: "CARD-00000208"
module: "orchestrator"
---

# CARD-00000208 — Rendre install.md déterministe pour un agent

- Dependencies: None. Fait suite à la Card 207.

## Expected outcome

`install.md` se déroule sans interprétation : chaque vérification est une commande avec son résultat attendu, chaque branche (mode, dossier existant, fichier existant) a une règle unique, le plan et la proposition ont un contenu fixé, chaque échec a une issue unique.

## Scope and authorization

`install.md` seulement. Demande de l'utilisateur : « fais en sorte de son efficacité pour être utilisé par un agent. L'outcome et les choix doivent être déterministes et sans équivoque ».

## Acceptance criteria

- Prérequis : commande et résultat attendu pour chacun.
- Ajouts idempotents (ligne déjà présente : rien).
- Plan, proposition, commit et vérification au contenu fixé.
- `GUARDRAILS.md` : la section réelle `## Standing permissions` remplace `## Overrides`, qui n'existe plus.
- `kr validate` passe.

## History
