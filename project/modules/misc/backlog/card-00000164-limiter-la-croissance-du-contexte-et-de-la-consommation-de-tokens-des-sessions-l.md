---
type: card
id: "CARD-00000164"
module: "misc"
---

# CARD-00000164 — Limiter la croissance du contexte et de la consommation de tokens des sessions longues

- Owner: Orchestrator
- Dependencies: Aucune.

## Expected outcome

Éviter que le coût par demande augmente au fil d’une session longue (constaté jusqu’à 35M de tokens pour une demande simple lors de l’audit de Codex, chiffre non revérifié), sans relancer une session par Card. La règle vaut pour Codex et pour Claude Code.

## Scope and authorization

Ajouter aux instructions de travail partagées (`orchestrator/guidelines/working-rules.md`, et `orchestrator/actions/deliver-card.md` si utile) des règles de maîtrise du contexte :

- compacter (ou repartir d’un contexte propre, l’état étant dans la Card et le journal) à chaque clôture de Card, et dès qu’un seuil de contexte à fixer est dépassé ;
- déléguer les audits, lectures larges et exécutions de tests bruyants à des agents séparés dont seule la conclusion revient ;
- borner les sorties d’outils (lectures partielles, recherche ciblée, fin de sortie des tests) ;
- grouper les appels d’outils indépendants ;
- garder légers les fichiers chargés à chaque tour (`AGENTS.md`, `CLAUDE.md`, règles partagées, skills) ;
- noter dans la Card les éléments de reprise utiles avant de compacter.

Vérifier le réglage de compaction automatique propre à chaque hôte avant de le documenter (par exemple le seuil d’auto-compaction de Codex). Ne pas modifier les réglages personnels de l’utilisateur sans son accord.

Mise au backlog à la demande de l’utilisateur. Le démarrage reste à autoriser ; une seule Card est en développement dans `misc` (CARD-00000162).

## Acceptance criteria

- [ ] Les règles de maîtrise du contexte figurent dans une seule source partagée, sans doublon dans les instructions des hôtes.
- [ ] Les seuils et réglages cités ont été vérifiés dans la documentation de l’hôte concerné.
- [ ] Les instructions restent courtes et n’alourdissent pas sensiblement le contexte chargé à chaque tour.
- [ ] La validation du Kanban et les contrôles applicables aux fichiers touchés passent.

## Resources

Aucune.

## Execution and evidence

- State: waiting
- Actual start:
- Actual finish:
- Blocker:

## History

- 2026-11-15 — Mise au backlog à la demande de l’utilisateur, à la suite de l’analyse de la consommation de tokens des sessions longues.
