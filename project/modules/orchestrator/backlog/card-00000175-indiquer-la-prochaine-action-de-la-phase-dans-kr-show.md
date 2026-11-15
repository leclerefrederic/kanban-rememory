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

- [ ] Checkout sale : `Next: commit the changes`.
- [ ] Checkout propre sans vérification, ou HEAD plus récent que la révision vérifiée : `Next: run check`.
- [ ] HEAD égal à la révision vérifiée : `Next: ask for approval, then publish`.
- [ ] Sans phase, aucune ligne `Next:`.
- [ ] Un test de `test-kr.py` couvre ces cas ; `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.
