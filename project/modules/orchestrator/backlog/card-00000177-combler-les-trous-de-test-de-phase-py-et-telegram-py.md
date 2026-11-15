---
id: "CARD-00000177"
module: "orchestrator"
---

# CARD-00000177 — Combler les trous de test de phase.py et telegram.py

- Dependencies: Aucune.

## Expected outcome

Les comportements de `phase.py` et `telegram.py` qui peuvent casser une livraison et qu’aucun test ne couvre sont identifiés par une mesure de couverture, puis couverts.

## Scope and authorization

Demande de l’utilisateur du 2026-11-16 (voir la Card du lanceur `kr`). Règle des tests du workflow : ajouter un test seulement pour un comportement qui peut casser quelque chose et que rien ne couvre. Pas de test pour atteindre un pourcentage.

## Acceptance criteria

- [ ] La mesure de couverture (module standard `trace`, sans dépendance ajoutée) liste les branches non couvertes de `phase.py` et `telegram.py`.
- [ ] Chaque branche à risque (refus, erreur de publication, perte de données) a un test ; les autres sont écartées avec leur raison dans l’Execution and evidence.
- [ ] `test-kr.py` et `test-telegram.py` passent ; `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.
