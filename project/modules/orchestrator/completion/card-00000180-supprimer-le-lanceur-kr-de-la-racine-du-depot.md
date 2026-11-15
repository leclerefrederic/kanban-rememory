---
id: "CARD-00000180"
module: "orchestrator"
---

# CARD-00000180 — Supprimer le lanceur kr de la racine du dépôt

- Dependencies: Aucune.

## Expected outcome

Le fichier `kr` n'existe plus à la racine ; les outils s'appellent par `python3 orchestrator/tools/kr.py`.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : il n'utilise pas le lanceur, seul l'Orchestrateur lance les outils. Remplacer `./kr` par `python3 orchestrator/tools/kr.py` dans `documentation/guide.md` et `orchestrator/workflow.md`, et retirer toute référence au lanceur ailleurs, tests compris. Les Cards existantes restent inchangées.

## Acceptance criteria

- `kr` à la racine est supprimé et aucune référence à `./kr` ne subsiste hors des Cards.
- Le workflow et le guide donnent la commande `python3 orchestrator/tools/kr.py`.
- `test-kr.py`, `test-telegram.py` et `validate` passent.

## Execution and evidence

## History

- 2026-11-16T00:50:27+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:52:59+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T00:52:59+01:00 — Merge approved for the verified candidate `4d5d483cb27d4fe77840fd88be7fc0f1ee392f36`: “Approuvé”.
