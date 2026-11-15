---
id: "CARD-00000175"
module: "orchestrator"
---

# CARD-00000175 — Indiquer la prochaine action de la phase dans kr show

- Dependencies: Aucune.

## Expected outcome

`kr show` ajoute à la ligne de phase la prochaine action à faire : commit à faire, `check` à lancer, approbation à demander ou `publish` à lancer.

## Scope and authorization

Demande de l’utilisateur du 2026-11-16 (voir la Card du lanceur `kr`). Pas de nouvelle commande : une ligne `Next:` sous `Phase:`, calculée depuis l’état de la phase et de Git.

## Acceptance criteria

- [x] Checkout sale : `Next: commit the changes`.
- [x] Checkout propre sans vérification, ou HEAD plus récent que la révision vérifiée : `Next: run check`.
- [x] HEAD égal à la révision vérifiée : `Next: ask for approval, then publish`.
- [x] Sans phase, aucune ligne `Next:`.
- [x] Un test de `test-kr.py` couvre ces cas ; `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.

- 2026-11-16T00:25:18+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:25:51+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T00:28:42+01:00 — Merge approved for the verified candidate `61119223197a33e848369f56f8ac1402a9821851`: “Une fois celles ci couvertes, tu fusionnes dans le main tu as mon accord.”.
