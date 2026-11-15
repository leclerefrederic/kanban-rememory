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

- [x] `./kr show` affiche le même résultat que `python3 orchestrator/tools/kr.py show`, y compris lancé depuis un autre répertoire.
- [x] `workflow.md` et `guide.md` nomment `./kr` comme lanceur.
- [x] `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.

- 2026-11-16T00:25:04+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:25:17+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T00:28:42+01:00 — Merge approved for the verified candidate `61119223197a33e848369f56f8ac1402a9821851`: “Une fois celles ci couvertes, tu fusionnes dans le main tu as mon accord.”.
