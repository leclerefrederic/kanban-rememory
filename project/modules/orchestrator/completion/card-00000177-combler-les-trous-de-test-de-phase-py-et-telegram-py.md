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

- [x] La mesure de couverture (module standard `trace`, sans dépendance ajoutée) liste les branches non couvertes de `phase.py` et `telegram.py`.
- [x] Chaque branche à risque (refus, erreur de publication, perte de données) a un test ; les autres sont écartées avec leur raison dans l’Execution and evidence.
- [x] `test-kr.py` et `test-telegram.py` passent ; `validate` passe.

## Execution and evidence

- State:
- Blocker:
- Mesure : module `trace` de la bibliothèque standard, lancé par l'API pour écrire les résultats malgré `unittest.main`.
- `phase.py` : ajout de `test_check_and_publish_refuse_unsafe_states` (validation en échec dans `check`, résumé et approbation invalides ou absents, critère non coché, clôture absente, `origin/main` déplacé à `publish` et à `check`).
- Écarté : les `ValueError` d'état impossible en usage normal (HEAD détaché, échec de `fetch`, `check_returncode`, `HEAD changed during the check`, échec de push non confirmé) ; la collision de tag, couverte par la vérification de `publish`.
- `telegram.py` : le point d'entrée en ligne de commande est lancé en sous-processus par `test-telegram.py`, donc invisible à `trace` ; les autres lignes non couvertes sont la configuration Windows et les erreurs de saisie interactive de l'installation, sans risque pour une livraison.

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.

- 2026-11-16T00:26:14+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:28:18+01:00 — Stage moved from `development` to `completion`.
