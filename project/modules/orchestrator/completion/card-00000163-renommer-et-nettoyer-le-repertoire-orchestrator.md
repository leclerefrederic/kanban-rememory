---
type: card
id: "CARD-00000163"
module: "orchestrator"
---

# CARD-00000163 — Renommer et nettoyer le répertoire orchestrator

- Owner: Orchestrator
- Dependencies: CARD-00000160 (workflow de livraison autonome).

## Expected outcome

Le répertoire `orchestrator/` contient les instructions et outils du workflow courant. L’Orchestrateur prend en charge le cadrage, l’exécution, la vérification et la livraison autorisée dans le même chat.

## Scope and authorization

Le 15 novembre 2026, l’utilisateur a demandé le renommage de `agents/`, le retrait des éléments obsolètes et les adaptations nécessaires au cumul des rôles. Mettre à jour les références actives, les outils et les contrôles touchés. Conserver les données historiques et la compatibilité des installations qui utilisent explicitement des rôles séparés ou des Batches.

## Acceptance criteria

- [x] Le paquet et ses points d’entrée actifs utilisent `orchestrator/`.
- [x] Le parcours courant couvre toutes les étapes de livraison dans le même chat et réserve les décisions requises à l’utilisateur.
- [x] La validation du Kanban, les tests des outils et la synchronisation des instructions Codex et Claude Code passent.

## Resources

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15T21:23:13+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15 — Candidat `62f42649124fe23ca5858c5ade260905d3aabd42` vérifié dans un worktree d’intégration sur la base de `466dec1`. Revue du diff, validation Kanban, synchronisation des instructions, vérification du hook Git et 113 tests automatisés réussis. Le push sur main déclenche les tests Telegram GitHub, sans déploiement de production.
- 2026-11-15 — L’utilisateur a approuvé la fusion et la publication du candidat vérifié `62f42649124fe23ca5858c5ade260905d3aabd42` dans le chat d’origine.

- 2026-11-15T21:30:37+01:00 — Stage moved from `development` to `completion`.
