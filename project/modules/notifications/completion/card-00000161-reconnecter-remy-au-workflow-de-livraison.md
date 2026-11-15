---
type: card
id: "CARD-00000161"
module: "notifications"
---

# CARD-00000161 — Reconnecter Remy au workflow de livraison

- Owner: Orchestrator
- Dependencies: CARD-00000160 (définit les passages de main du workflow).

## Expected outcome

Remy envoie sur Telegram les alertes du workflow de livraison lorsque les notifications sont configurées. L’utilisateur retrouve le chat d’origine pour agir ou consulter le résultat.

## Scope and authorization

Réutiliser Remy et les deux types d’alerte existants, `attention` (Intervention requise) et `completed` (Travail terminé). Le type `attention` couvre deux moments distincts. L’utilisateur a demandé la mise au backlog. Le démarrage fera l’objet d’une autorisation distincte.

## Acceptance criteria

- [x] **Intervention requise — décision ou action indispensable.** Quand un travail s’arrête sur une décision, un accès ou une action que seul l’utilisateur peut fournir, Remy identifie la Card, indique ce qui est attendu et renvoie au chat où agir.
- [x] **Intervention requise — accord de fusion vers `main`.** Quand le candidat vérifié est prêt, Remy demande l’accord pour la révision présentée et renvoie au chat. Le message signale tout déploiement automatique de production que la fusion ou le push déclenchera. L’accord est donné dans le chat d’origine.
- [x] **Travail terminé — livraison vérifiée.** Une fois la livraison convenue vérifiée, Remy indique le résultat et où le consulter. Le message précise qu’aucune action n’est attendue.
- [x] Une même demande ou livraison ne produit qu’une alerte. Les étapes intermédiaires et les erreurs que l’orchestrateur peut corriger seul ne déclenchent pas d’alerte.

## Resources

- [Règles de notification](../../../../agents/actions/notify-user.md) — types d’alerte et comportement existant.
- [Workflow de livraison](../../../../agents/actions/deliver-card.md) — passages de main à raccorder.

## Execution and evidence

- State: completed
- Actual start: 2026-11-15
- Actual finish: 2026-11-15
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur.

- 2026-11-15T21:16:56+01:00 — Stage moved from `backlog` to `development`.

- L’utilisateur a autorisé la fusion et la publication directes de cette Card dans le chat, sans nouvelle demande d’accord.
- Les 23 contrôles Telegram sont passés. Les trois scénarios ont été vérifiés avec des aperçus en français utilisant un destinataire fictif.

- 2026-11-15T21:18:10+01:00 — Stage moved from `development` to `completion`.
