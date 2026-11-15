---
id: "CARD-00000173"
module: "orchestrator"
---

# CARD-00000173 — Choisir main ou une release au démarrage d'une Card, et tagger la release

- Dependencies: Aucune. Modifie CARD-00000165 (phase) et la règle « jamais sur `main` » de `workflow.md`.

## Expected outcome

Au démarrage d'une Card, l'Orchestrator demande à l'utilisateur de travailler sur `main` ou dans une release. Une release est une phase (CARD-00000165) : une branche qui livre une ou plusieurs Cards avec une seule fusion. À la fusion d'une release, un tag git `vX.Y.Z` est posé avec une montée de version automatique.

## Scope and authorization

Demande de l’utilisateur du 2026-11-16, release = phase. La demande autorise la création de la Card ; le démarrage reste à autoriser.

- **Choix au démarrage.** `kr start` n'ouvre rien sans réponse : `main` ou release (nouvelle ou existante).
- **Mode `main`.** L'Orchestrator commite chaque étape sur `main` (autocommit). `check` reste obligatoire avant la poussée : l'autocommit ne dispense pas de vérifier. Un accord donné dans la demande (CARD-00000172) permet de publier sans redemander.
- **Mode release.** Les Cards se commitent sur la branche de la release. L'utilisateur décide de la fusion ; `publish` la fait comme aujourd'hui.
- **Version.** Aucun fichier version (CARD-00000169) : le dernier tag `vX.Y.Z` est la source. L'utilisateur choisit patch, minor ou major à la création de la release, patch par défaut. `publish` calcule le tag suivant et le pose sur le commit publié, puis le pousse.
- **Points à confirmer avant le démarrage** : le tag en mode `main` (proposition : aucun, seules les releases sont taguées) ; si `check` reste exigé en mode `main` (proposition : oui).
- Modifier `kr.py`, `kanban/`, `test-kr.py`, `workflow.md`, `guide.md`, `install.md` et `AGENTS.md` relève de cette Card.

## Acceptance criteria

- [ ] `kr start` demande `main` ou release et refuse sans réponse.
- [ ] Le mode `main` commite sur `main`, exige `check`, puis pousse.
- [ ] Une release fusionnée reçoit le tag `vX.Y.Z` suivant selon patch, minor ou major, poussé avec `main`.
- [ ] Les points à confirmer sont tranchés par l'utilisateur et consignés dans la Card.
- [ ] `workflow.md`, `guide.md`, `install.md` et `AGENTS.md` décrivent le choix et le tag sans se répéter.
- [ ] `test-kr.py` couvre les deux modes et le calcul du tag ; `validate` passe.
