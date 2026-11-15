---
id: "CARD-00000171"
module: "orchestrator"
---

# CARD-00000171 — Réduire les appels par Card et accélérer test-kr.py

- Dependencies: Aucune.

## Expected outcome

Une petite Card se livre en environ 8 appels au lieu de 14, et `test-kr.py` tourne plus vite.

## Scope and authorization

Décision de l’utilisateur du 2026-11-15 (« Oui, 2 à 4 »), points 2 et 4 présentés dans le chat. La demande autorise l’exécution.

- `kr new --body` lit le contenu de la Card, sous son titre, sur l’entrée standard.
- `kr publish --summary --approval` clôt les Cards, inscrit l’accord et le jalon, commite et publie ; `close` disparaît. Le commit de clôture reprend les trailers `Co-Authored-By` du candidat vérifié. Relancé sur un commit de clôture existant, `publish` publie sans reclore.
- `kr publish --notify "CHAT"` envoie l’alerte Remy « Travail terminé » après la publication.
- Les Cards ne recopient plus ce que gardent git, le journal ou le registre Telegram ; `State` ne sert qu’à `waiting` ou `blocked`.
- `test-kr.py` appelle `kr.py` dans le même processus. Objectif mesuré : environ 6 s au lieu de 11 s.

## Acceptance criteria

- [x] `kr new --body` crée la Card avec le contenu fourni ; c’est testé.
- [x] Sur la révision vérifiée, `kr publish --summary --approval` clôt, commite et publie en un appel ; relancé sur un commit de clôture, il publie sans reclore ; c’est testé.
- [x] `--notify` lance l’alerte de livraison, et un Telegram absent ne fait pas échouer la publication ; c’est testé sans configuration réelle.
- [x] La séquence documentée d’une phase à une Card compte au plus 6 commandes, et `workflow.md` ne demande plus de recopier dans la Card ce que gardent git, le journal ou le registre Telegram.
- [x] `test-kr.py` passe en moins de 11 s ; la durée mesurée est notée.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur.

- 2026-11-15T23:46:24+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15 — `test-kr.py` : 11 s → 8,2 s (6 tests, même processus). Objectif de 6 s non atteint : les appels `git` dominent.

- 2026-11-15T23:54:45+01:00 — Stage moved from `development` to `completion`.
