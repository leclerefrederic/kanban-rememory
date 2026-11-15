---
id: "CARD-00000168"
module: "misc"
affected_modules: ["notifications", "orchestrator"]
---

# CARD-00000168 — Auditer et refondre le dépôt pour une livraison rapide et rigoureuse

- Dependencies: Aucune.

## Expected outcome

L’Orchestrator trouve vite ce qu’il doit savoir, livre une Card en peu d’appels, applique les règles à la lettre parce que l’outil les contrôle, et ne teste que ce qui doit l’être. Le dépôt ne contient plus de superflu, de doublon ni d’élément inutile.

## Scope and authorization

Demande de l’utilisateur du 2026-11-15 : « audite toi et refactorise l’ensemble du repo » (optimisation, performance, précision, intelligence, refactoring, efficience). La demande autorise l’exécution. Audit présenté dans le chat. Décisions de l’utilisateur le même jour : refondre le flux de livraison, fusionner les guides humains, supprimer les modules `acceptance` et `configuration` (jamais utilisés), supprimer l’état local périmé de `.git/kanban-rememory` après publication.

1. **Flux de livraison.** Un seul outil `orchestrator/tools/kr.py` : `show`, `validate`, `path`, `new`, `move`, `start`, `check`, `close`, `publish`, `init`. Cards et journal lus et écrits dans le checkout courant et commités sur la branche de phase ; plus de worktree d’intégration ni d’écriture dans le checkout de `main`. Une seule phase à la fois, enregistrée dans `.git/kanban-rememory/phase.json`. Pendant une phase, `new` et `move` ne s’exécutent que dans son worktree. `check` lance `validate` puis les commandes données sur un checkout propre qui contient `origin/main`, enregistre la révision vérifiée et liste les workflows CI. `close` exige la révision vérifiée, passe les Cards en completion, inscrit l’accord et le jalon du journal (durée, tokens). `publish` n’accepte qu’un commit de clôture limité aux Cards et au journal, pousse vers `origin/main`, met `main` local à jour et termine la phase.
2. **Superflu retiré.** Options `--owner`, `--base`, `--scope` en double, `--wip-limit`, `--timezone`, aperçu de `new` ; `checkpoint`, jalon `--evidence`, réécriture des liens au déplacement, verrous multi-modules, jetons d’intégration et répertoires runtime ; réglages `execution`, `shared`, `board_layout`, `project.id` et chemins de module (disposition fixe `project/modules/<module>/`, journal `project/rememory/`, schéma 2) ; champs de Card `type`, `Owner`, `Actual start`, `Actual finish` et section Resources par défaut (l’âge se lit dans l’historique) ; liste d’exceptions de liens (les liens des Cards terminées ne sont plus vérifiés) ; modèle de journal.
3. **Telegram.** Un seul script `orchestrator/tools/telegram.py` (`setup`, `status`, `test`, `attention`, `completed`). Module et projet déduits de la Card et des réglages. Retrait de `--task`, `--module`, `--project`, des libellés sur mesure, de `--send-to`, des filtres d’événements et de `run`. Conservés : même message, anti-doublon, confirmation des envois incertains, protection du jeton, macOS et Windows.
4. **Instructions agent.** Une seule procédure `orchestrator/workflow.md` (remplace `actions/`, `guidelines/` et `index.md`), `orchestrator/notify.md` et `orchestrator/install.md` (remplace `setup/`). `AGENTS.md` réduit à la politique du projet.
5. **Guides humains.** README, `documentation/guide.md` (fusion des guides), `lean-specifications.md` et `telegram-setup.md`.
6. **Tests.** `test-kr.py` et `test-telegram.py`, limités aux comportements à risque : attribution des IDs, déplacements, validation, phase de bout en bout et ses refus, rapport de performance, alertes et protection du secret Telegram.

Après publication, hors critères : suppression de l’état local périmé de `.git/kanban-rememory`, registre Telegram anti-doublon conservé.

## Acceptance criteria

- [ ] Une phase complète (`start`, `check`, `close`, commit, `publish`) se déroule avec `kr.py` dans le seul worktree de phase, sans écriture dans le checkout de `main` ; un test de bout en bout le vérifie.
- [ ] L’outil refuse une seconde phase, `new` hors du worktree de phase pendant une phase, `close` sur une autre révision que celle vérifiée et `publish` d’un commit de clôture qui touche autre chose que les Cards et le journal ; chaque refus est testé.
- [ ] La séquence documentée d’une phase à une Card compte au plus 8 commandes.
- [ ] Les éléments listés comme superflus ne figurent plus dans le code ni dans la doc ; les réglages sont au schéma 2 avec les modules `misc`, `notifications` et `orchestrator`.
- [ ] Les alertes Remy gardent le même message, l’anti-doublon et la confirmation des envois incertains ; `telegram.py` les envoie avec `--card`, sans `--module`, `--task` ni `--project` ; testé sans réseau.
- [ ] Les règles de l’agent tiennent dans `AGENTS.md` et `orchestrator/workflow.md`, sans règle dupliquée, en moins de 8 Ko à eux deux (18 Ko auparavant pour une livraison).
- [ ] Les guides humains se limitent à README, `documentation/guide.md`, `lean-specifications.md` et `telegram-setup.md`, cohérents avec le nouveau flux.
- [ ] `validate`, `test-kr.py` et `test-telegram.py` passent sur le candidat vérifié.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur, avec ses décisions sur le flux, les guides, les modules et l’état local.

- 2026-11-15T23:11:07+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Phase `claude/phase-168` ouverte (claim enregistré). Passage en development fait sur la branche et non dans le checkout de `main` : l’hôte interdit d’écrire dans le checkout principal depuis le worktree, et la refonte approuvée garde les Cards sur la branche de phase.
