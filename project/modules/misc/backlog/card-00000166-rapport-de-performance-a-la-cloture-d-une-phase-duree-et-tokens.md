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

- [ ] Le jalon de publication contient la durée de la phase et par Card, calculée à partir d’horodatages enregistrés par l’outil.
- [ ] Il contient les totaux de tokens pour Claude Code et pour Codex sur la période, ou la mention explicite qu’ils sont indisponibles.
- [ ] Aucune étape manuelle n’est ajoutée à la séquence de commandes de livraison.
- [ ] Aucun contenu de conversation ni chemin personnel n’est écrit dans le journal.
- [ ] Les tests de l’outil de livraison couvrent le calcul des durées et la lecture des deux formats avec des journaux de test, et les contrôles applicables passent.

## Resources

Aucune.

## Execution and evidence

- State: waiting
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur. Constat préalable : une session Claude Code d’environ 150 messages totalisait 16,7 M de tokens lus en cache pour 0,1 M en sortie.
