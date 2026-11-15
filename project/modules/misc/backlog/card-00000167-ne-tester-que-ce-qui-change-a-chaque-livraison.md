---
type: card
id: "CARD-00000167"
module: "misc"
---

# CARD-00000167 — Ne tester que ce qui change à chaque livraison

- Owner: Orchestrator
- Dependencies: Aucune.

## Expected outcome

Chaque livraison ne lance que les contrôles qui couvrent ce qu’elle modifie, sans empiler de tests redondants d’une Card à l’autre.

## Scope and authorization

Écrire la règle dans `orchestrator/actions/deliver-card.md` : tests des outils seulement quand leur code change, aucun test pour une modification de documentation ou de Cards, pas de nouveau test pour ce qu’un test existant ou `validate` couvre déjà, et `validate` seul sur le commit de clôture, qui n’ajoute que des fichiers de Cards et de journal. Démarrage autorisé par l’utilisateur dans le chat (« on ne teste que ce qui change »).

## Acceptance criteria

- [ ] La règle figure dans `deliver-card.md`, une seule fois, sans modifier `AGENTS.md`.
- [ ] La séquence de commandes indique `validate` seul pour la vérification du commit de clôture.
- [ ] `validate` passe.

## Resources

Aucune.

## Execution and evidence

- State: waiting
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur après le constat que des suites de tests complètes étaient relancées à chaque Card, y compris sur le commit de clôture.
