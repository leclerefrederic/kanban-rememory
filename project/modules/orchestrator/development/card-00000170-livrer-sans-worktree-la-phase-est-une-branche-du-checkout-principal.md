---
id: "CARD-00000170"
module: "orchestrator"
---

# CARD-00000170 — Livrer sans worktree : la phase est une branche du checkout principal

- Dependencies: Aucune. Modifie le flux de CARD-00000168.

## Expected outcome

Un seul agent livre les Cards dans le checkout principal, sur la branche de phase, sans créer ni retirer de worktree.

## Scope and authorization

Décision de l’utilisateur du 2026-11-15 : « Je ne veux plus de worktrees pour le moment, KR sera mono agent ». La demande autorise l’exécution. La branche de phase, l’interdiction de travailler sur `main`, la phase unique et l’accord sur la révision vérifiée restent inchangés.

- `start` n’exige plus de worktree, seulement une branche autre que `main` ; l’état de phase ne retient plus de worktree.
- Pendant une phase, les Cards ne s’écrivent que sur sa branche.
- `publish` revient sur `main`, l’avance sur le commit publié et supprime la branche de phase.
- `workflow.md`, `install.md`, `.gitignore` et `test-kr.py` ne parlent plus de worktree.

## Acceptance criteria

- [x] Une phase complète se déroule sur une branche du checkout principal ; après `publish`, ce checkout est sur `main` au commit publié et la branche n’existe plus ; un test de bout en bout le vérifie.
- [x] `start` sur `main` et l’écriture de Cards depuis une autre branche pendant une phase sont refusés ; c’est testé.
- [x] Le code et la doc ne mentionnent plus de worktree, hors historique.
- [x] `validate` et `test-kr.py` passent sur le candidat vérifié.

## Execution and evidence

- State: in-progress — vérification du candidat
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur.

- 2026-11-15T23:36:19+01:00 — Stage moved from `backlog` to `development`.
- 2026-11-15 — Phase ouverte sur `claude/phase-170` dans le checkout principal. L’outil publié exigeait encore un worktree : `start` a été lancé avec son propre code, ce seul contrôle neutralisé pour cette exécution.
- 2026-11-15 — Implémenté : contrôle de worktree et champ `worktree` de l’état retirés, `publish` revient sur `main` à jour et supprime la branche, test de bout en bout sur une branche, `workflow.md` (7 commandes), `install.md` et `.gitignore` à jour. `test-kr.py` (6 tests) passe ; `telegram.py` inchangé, sa suite n’est pas relancée.
