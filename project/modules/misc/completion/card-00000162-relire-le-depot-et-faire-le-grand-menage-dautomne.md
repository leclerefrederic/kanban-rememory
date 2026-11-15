---
type: card
id: "CARD-00000162"
module: "misc"
---

# CARD-00000162 — Relire le dépôt et faire le grand ménage d’automne

- Owner: Orchestrator
- Dependencies: Aucune.

## Expected outcome

Relire le dépôt après la migration pour retirer les fichiers, instructions et outillages obsolètes, et disposer d’un dépôt cohérent avec le workflow actuel.

## Scope and authorization

Inventorier les éléments devenus inutiles depuis la migration. Prévoir la suppression du répertoire local `Archives/`, y compris de ses fichiers ignorés par Git. L’utilisateur a demandé la mise au backlog. Le démarrage et les suppressions relèvent de l’exécution de cette Card.

Le 15 novembre 2026, après l’audit du dépôt (hors `project/` et `graphify-out/`), l’utilisateur a décidé de retirer entièrement le support legacy : Batches, Specifications, rôles séparés (Writer, Developer, Tester), skills de rôle, hook de rôle Claude, garde et hook de publication Batch, migration du journal déjà appliquée et anciennes mises en page (`project.json`, `project/kanban/`). L’historique Git reste la seule référence historique. Fusionner l’amorçage de l’Orchestrateur en une source unique et corriger les incohérences relevées.

## Acceptance criteria

- [x] Les éléments conservés ou supprimés sont justifiés par ce que le dépôt utilise encore.
- [x] Le dossier local `Archives/` a été supprimé et les instructions actives renvoient vers les bons emplacements pour les références historiques.
- [x] Les instructions, la documentation et les outils ne décrivent plus que le workflow Card unique.
- [x] La validation du Kanban et les contrôles applicables aux éléments touchés passent.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur.

- 2026-11-15T21:43:42+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Audit présenté ; l’utilisateur a autorisé le retrait complet du legacy dans le chat d’origine. Branche `claude/card-00000162-cleanup`, worktree `/private/tmp/kr-card00000162`, base `60222a6`.
- 2026-11-15 — Candidat `c4fc31fb3da7741836a0a86d2c9b2dc173ffee9c` vérifié dans un worktree d’intégration sur la base de `60222a6` (avance rapide). Revue du diff (100 fichiers, +971/−7904), validation Kanban et 39 tests automatisés réussis (`test-kanban-board`, `test-module-delivery`, `test-telegram-setup`). Le push sur main déclenche les tests GitHub Telegram (macOS, Windows), sans déploiement de production.
- 2026-11-15 — L’utilisateur a approuvé la fusion et la publication du candidat vérifié `c4fc31fb3da7741836a0a86d2c9b2dc173ffee9c` dans le chat d’origine.

- 2026-11-15T21:55:52+01:00 — Stage moved from `development` to `completion`.
