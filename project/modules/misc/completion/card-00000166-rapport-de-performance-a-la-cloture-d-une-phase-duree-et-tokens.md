---
type: card
id: "CARD-00000166"
module: "misc"
---

# CARD-00000166 — Rapport de performance à la clôture d’une phase : durée et tokens

- Owner: Orchestrator
- Dependencies: Aucune. S’appuie sur la phase multi-Cards (CARD-00000165).

## Expected outcome

À la clôture d’une phase, le jalon du journal indique sans étape supplémentaire pour l’Orchestrator : la durée totale de la phase, la durée par Card, et les tokens consommés (entrée, entrée en cache, sortie) pour Claude Code et Codex.

## Scope and authorization

- Horodater automatiquement `claim`, `add-card`, `checkpoint` et `finish` dans l’état de la livraison, et les Cards au passage en `completion`.
- Au `finish`, lire les journaux de session de l’hôte pour la période de la phase et ajouter une ligne de synthèse au jalon : Claude Code (`~/.claude/projects/<projet>/*.jsonl`, champ `usage` par message avec horodatage) et Codex (`~/.codex/sessions/AAAA/MM/JJ/rollout-*.jsonl`, événements `token_count` cumulés). Ces emplacements ont été constatés le 2026-11-15 sur le poste de l’utilisateur ; ils ne sont pas une interface documentée.
- Retenir les sessions dont le répertoire de travail est le dépôt ou ses worktrees de phase. Lecture seule, aucune donnée de conversation copiée, uniquement des totaux.
- Si les journaux sont absents ou ambigus, écrire « tokens : non disponibles » sans bloquer la livraison.
- Hors périmètre : coûts en argent, suivi par tâche fine, changement des réglages de l’hôte.

Mise au backlog à la demande de l’utilisateur ; le démarrage reste à autoriser.

## Acceptance criteria

- [x] Le jalon de publication contient la durée de la phase et par Card, calculée à partir d’horodatages enregistrés par l’outil.
- [x] Il contient les totaux de tokens pour Claude Code et pour Codex sur la période, ou la mention explicite qu’ils sont indisponibles.
- [x] Aucune étape manuelle n’est ajoutée à la séquence de commandes de livraison.
- [x] Aucun contenu de conversation ni chemin personnel n’est écrit dans le journal.
- [x] Les tests de l’outil de livraison couvrent le calcul des durées et la lecture des deux formats avec des journaux de test, et les contrôles applicables passent.

## Resources

Aucune.

## Execution and evidence

- State: done
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur. Constat préalable : une session Claude Code d’environ 150 messages totalisait 16,7 M de tokens lus en cache pour 0,1 M en sortie.

- 2026-11-15T22:33:12+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Démarrage autorisé par l’utilisateur (« fais la 166 »), phase `claude/phase-card-166`.
- 2026-11-15 — Implémenté dans `kanban/report.py` et `coordination.py` : heure du `claim` enregistrée dans l’état ; durée par Card lue dans l’historique de la Card (déjà horodaté par les déplacements) plutôt que par de nouveaux horodatages à `add-card`, `checkpoint` et `finish`, ce qui évite du code redondant ; ligne de performance ajoutée au jalon de publication. Essai sur de vraies données : phase 165/164, Claude Code 4,2 M tokens lus en cache pour 25 k en sortie ; Codex indisponible (aucune session Codex dans ce répertoire sur la période). Tests `test-module-delivery.py` (6) et `test-kanban-board.py` OK.

- 2026-11-15T22:35:28+01:00 — Stage moved from `development` to `completion`.
- 2026-11-15 — Approbation explicite de l’utilisateur (« Oui, fusionne ») pour le candidat vérifié `40ad7ed` de la phase `claude/phase-card-166`, sans déploiement automatique ; tests de livraison, tests du Kanban et `validate` OK.
