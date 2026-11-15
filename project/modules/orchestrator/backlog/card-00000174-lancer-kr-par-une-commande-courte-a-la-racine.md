---
id: "CARD-00000174"
module: "orchestrator"
---

# CARD-00000174 — Lancer kr par une commande courte a la racine

- Dependencies: Aucune.

## Expected outcome

`./kr <commande>` à la racine du dépôt lance `python3 orchestrator/tools/kr.py <commande>`, depuis n’importe quel répertoire courant.

## Scope and authorization

Demande de l’utilisateur du 2026-11-16 : couvrir les cinq pistes d’amélioration proposées, dans une nouvelle release, puis fusionner dans `main` (accord donné dans la demande). Un script shell exécutable, sans option ni installation globale.

## Acceptance criteria

- [ ] `./kr show` affiche le même résultat que `python3 orchestrator/tools/kr.py show`, y compris lancé depuis un autre répertoire.
- [ ] `workflow.md` et `guide.md` nomment `./kr` comme lanceur.
- [ ] `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.
