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

- [ ] Une phase complète se déroule sur une branche du checkout principal ; après `publish`, ce checkout est sur `main` au commit publié et la branche n’existe plus ; un test de bout en bout le vérifie.
- [ ] `start` sur `main` et l’écriture de Cards depuis une autre branche pendant une phase sont refusés ; c’est testé.
- [ ] Le code et la doc ne mentionnent plus de worktree, hors historique.
- [ ] `validate` et `test-kr.py` passent sur le candidat vérifié.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur.
