---
type: card
id: "CARD-00000160"
module: "orchestrator"
---

# CARD-00000160 — Automatiser la livraison des Cards avec accord avant fusion

- Owner: Orchestrator
- Dependencies: Aucune.

## Expected outcome

Une fois le développement autorisé, l’orchestrateur mène la Card jusqu’à la livraison. Il rend la main à l’utilisateur quand une intervention est nécessaire ou quand le travail est terminé. La fusion vers `main` fait partie des décisions qui exigent l’accord explicite de l’utilisateur.

## Scope and authorization

Aligner les instructions de démarrage, de développement et de livraison sur le parcours ci-dessous. L’utilisateur a demandé la mise au backlog. Le démarrage fera l’objet d’une autorisation distincte.

## Acceptance criteria

- [x] À la demande initiale, l’orchestrateur cadre le résultat et les critères dans une Card. Il réutilise l’autorisation déjà donnée ou demande la décision manquante.
- [x] Après autorisation, il passe la Card en `development`, travaille sur une branche dédiée, relit le diff, lance les contrôles applicables et corrige les échecs récupérables avant de les relancer.
- [x] Quand une intervention est indispensable, il indique précisément l’action ou la décision attendue et ce qui en dépend. Il poursuit le travail autorisé qui reste possible.
- [x] Avant la fusion vers `main`, il vérifie le candidat avec `main` à jour et présente la révision, les contrôles effectués et tout déploiement automatique de production déclenché par la fusion ou le push. Il consigne l’accord explicite de l’utilisateur pour ce candidat. La Card reste en `development` tant que l’accord manque. Si le candidat change, il le revérifie et soumet la nouvelle révision.
- [x] Après accord, il termine la livraison autorisée, vérifie la publication et le déploiement s’il fait partie de la livraison, clôture la Card et consigne le jalon dans Rememory. Il indique à l’utilisateur ce qui a été livré et où le consulter.

## Resources

- [Workflow de livraison](../../../../agents/actions/deliver-card.md) — procédure à aligner avec le parcours validé.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur.

- 2026-11-15T21:00:52+01:00 — Stage moved from `backlog` to `development`.

- Développement autorisé par l’utilisateur. Exécuter CARD-00000161 après la livraison de CARD-00000160.
- Candidat `9f7ad233f99a8a4c565ab8e533955d2be50501e6` sur la base de `main` à `f0d021dd3126ccb345c578a871578b591c4910c7`. Revue du diff, contrôle du diff et validation Kanban réussis dans le checkout d’intégration.
- Le dépôt ne déclare aucun déploiement automatique de production pour ce candidat. Accord de fusion demandé dans le chat d’origine.

- 2026-11-15 — L’utilisateur a explicitement autorisé la fusion et la publication du candidat `9f7ad23` dans le chat. Ce record accompagne la publication.

- 2026-11-15T21:14:01+01:00 — Stage moved from `development` to `completion`.
