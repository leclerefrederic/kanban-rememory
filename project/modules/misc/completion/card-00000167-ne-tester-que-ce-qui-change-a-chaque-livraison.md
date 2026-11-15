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

- [x] La règle figure dans `deliver-card.md`, une seule fois, sans modifier `AGENTS.md`.
- [x] La séquence de commandes indique `validate` seul pour la vérification du commit de clôture.
- [x] `validate` passe.

## Resources

Aucune.

## Execution and evidence

- State: done
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur après le constat que des suites de tests complètes étaient relancées à chaque Card, y compris sur le commit de clôture.

- 2026-11-15T22:39:39+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Règle ajoutée (section « Test only what changes ») ; séquence de commandes mise à jour. Aucun test d’outil lancé : seule de la documentation change, `validate` suffit.

- 2026-11-15T22:39:47+01:00 — Stage moved from `development` to `completion`.
- 2026-11-15 — Approbation explicite de l’utilisateur pour le candidat vérifié `78fa97d`, livré directement sans nouvelle branche ; `validate` OK, aucun déploiement automatique.
