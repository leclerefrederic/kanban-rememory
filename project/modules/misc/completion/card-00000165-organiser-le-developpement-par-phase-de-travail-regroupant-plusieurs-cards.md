---
type: card
id: "CARD-00000165"
module: "misc"
---

# CARD-00000165 — Organiser le développement par phase de travail regroupant plusieurs Cards

- Owner: Orchestrator
- Dependencies: Aucune. Complète CARD-00000164 (même sujet : réduire le coût d’une session longue), mais se livre indépendamment.

## Expected outcome

Une branche et un worktree correspondent à une phase de développement, pas à une Card. Une phase peut contenir plusieurs Cards, ce qui évite un cycle branche, commit, intégration et approbation par Card.

## Scope and authorization

Revoir les règles actuelles qui lient une Card à une branche et à une livraison : « Keep one active delivery per scope and one Card in Development per scope », « Integrate one delivery at a time », l’approbation avant fusion « of a Card » et le workflow `orchestrator/actions/deliver-card.md`. Définir :

- ce qu’est une phase (périmètre, durée, nommage de la branche et du worktree) ;
- le principe d’une seule branche de dev active à la fois, l’Orchestrator pilotant le processus : une Card créée pendant la phase reste sur la branche de la phase et part avec sa fusion, ce qui exclut les collisions d’ID entre branches ;
- la règle de démarrage : aucun travail ne commence sur une Card sans branche de phase active, jamais directement sur `main` ; la Card rejoint une phase existante ou en ouvre une ;
- comment plusieurs Cards partagent la phase : capacité en développement, un commit ou plus par Card pour garder la traçabilité, état et historique de chaque Card ;
- l’approbation de fusion au niveau de la phase, avec la liste des Cards couvertes, sans perdre la vérification du candidat exact ;
- la clôture : chaque Card reste fermée avec sa révision, l’entrée de journal peut être unique pour la phase et liée aux Cards ;
- l’effet sur les outils (`manage-module-delivery.py`, `manage-kanban-board.py`, jetons de propriétaire) et leurs tests.

Toute modification d’un outil ou des règles de `AGENTS.md` relève de cette Card. Mise au backlog à la demande de l’utilisateur ; le démarrage reste à autoriser. À ordonnancer avec CARD-00000162, qui touche les mêmes instructions.

## Acceptance criteria

- [x] La notion de phase est définie dans une seule source partagée et `AGENTS.md` y renvoie sans doublon.
- [x] Aucun travail ne démarre sur une Card sans branche de phase, et `main` ne reçoit aucun travail direct ; la règle est écrite et contrôlée par les outils ou garde-fous quand c’est faisable.
- [x] Une phase peut livrer plusieurs Cards avec une seule branche, un seul worktree et une seule approbation de fusion, sans perdre la traçabilité par Card.
- [x] La limite d’une Card en développement par scope est remplacée ou reformulée de façon cohérente avec les outils.
- [x] Les outils et leurs tests couvrent le cas à plusieurs Cards ; la validation du Kanban et les contrôles applicables passent.

## Resources

Aucune.

## Execution and evidence

- State: done
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur : une branche par phase de développement, plusieurs Cards par phase.
- 2026-11-15 — Décision de l’utilisateur : le travail sur une Card ne commence jamais sans branche, jamais directement sur `main`.
- 2026-11-15 — Décision de l’utilisateur : une seule branche de dev active à la fois, gérée par l’Orchestrator.

- 2026-11-15T22:20:00+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Démarrage autorisé par l’utilisateur (« fais 165 puis 164 »). Phase `claude/phase-cards-165-164` partagée avec CARD-00000164.
- 2026-11-15 — Implémenté : `add-card`, clôture et jalon sur toutes les Cards de la phase, section Phase de `deliver-card.md`, `AGENTS.md` à jour. Tests `test-module-delivery.py` et `test-kanban-board.py` OK. Limite connue : rien n’empêche techniquement de créer une Card sur `main` ; la règle est écrite, pas verrouillée.

- 2026-11-15T22:21:49+01:00 — Stage moved from `development` to `completion`.
- 2026-11-15 — Approbation explicite de l’utilisateur (« Oui, fusionne ») pour le candidat vérifié `97d6577` de la phase `claude/phase-cards-165-164` (CARD-00000165 et CARD-00000164), sans déploiement automatique ; tests `test-module-delivery.py` et `test-kanban-board.py` et `validate` OK. Publication à vérifier au jalon du journal.
