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
- **Version.** La version courante est stockée dans `project/settings.json` (clé `version`, `"X.Y.Z"`, initialisée à `0.0.0`), à côté de `last_card_id`. Le tag git n'en est que le reflet : la valeur de `settings.json` fait foi. L'utilisateur choisit patch, minor ou major à la création de la release, patch par défaut. `publish` calcule la version suivante, l'écrit dans `settings.json` dans le commit de clôture, pose le tag `vX.Y.Z` sur ce commit et le pousse avec `main`. `validate` vérifie le format de `version` (`kanban/project.py`) ; `publish` refuse un tag existant qui marque une autre révision.
- **Décisions de l'utilisateur du 2026-11-16** (« Oui, les deux »). Aucun tag en mode `main`, seules les releases sont taguées. `check` reste exigé en mode `main`.
- Modifier `kr.py`, `kanban/`, `test-kr.py`, `workflow.md`, `guide.md`, `install.md` relève de cette Card.

## Acceptance criteria

- [x] `kr start` demande `main` ou release et refuse sans réponse.
- [x] Le mode `main` commite sur `main`, exige `check`, puis pousse.
- [x] Une release fusionnée met à jour `version` dans `settings.json` et reçoit le tag `vX.Y.Z` suivant selon patch, minor ou major, poussé avec `main`.
- [x] Les points à confirmer sont tranchés par l'utilisateur et consignés dans la Card.
- [x] `workflow.md`, `guide.md` et `install.md` décrivent le choix et le tag sans se répéter.
- [x] `test-kr.py` couvre les deux modes et le calcul du tag ; `validate` passe.

## History

- 2026-11-16T00:15:45+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:19:20+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T00:19:20+01:00 — Merge approved for the verified candidate `2104776ffc3736ca64b0e19afd4bd0947277a81f`: “Oui, fusionne”.
