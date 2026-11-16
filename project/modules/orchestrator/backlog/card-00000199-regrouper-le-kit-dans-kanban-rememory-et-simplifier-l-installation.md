---
id: "CARD-00000199"
module: "orchestrator"
---

# CARD-00000199 — Regrouper le kit dans kanban-rememory/ et simplifier l'installation

- Dependencies: Aucune.

## Expected outcome

`orchestrator/` et `documentation/` vivent dans un seul dossier `kanban-rememory/`. L'installation se réduit à : le dossier existe ou non, et une mise à jour remplace le dossier entier avec l'accord de l'utilisateur.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, qui remplace CARD-00000198 (annulée). Travail sur `main`. Module orchestrator ; touche aussi la documentation et le README.

- Déplacer `orchestrator/` et `documentation/` sous `kanban-rememory/` ; `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md` et `project/` restent à la racine.
- Mettre à jour tous les chemins : outils (`telegram.py`, `phase.py`, `project.py`, `validation.py`), tests, `workflow.md`, `notify.md`, `install.md`, `guide.md`, `telegram-setup.md`, `README.md`, `AGENTS.md`, `GUARDRAILS.md`. Les Cards terminées gardent leurs anciens chemins.
- Réécrire `install.md` pour un LLM : dossier absent = installation vierge, présent = remplacement après accord, sans `diff` ni comparaison fichier par fichier ; ajouts à `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md` (permissions Git sous `Overrides`), `.gitignore` (`__pycache__/`), `.gitattributes` (`* text=auto`), puis `project/` généré en dernier par `kr init`, sans push.
- Reprendre le texte de `install.md` du commit `b4720a1` comme base.
- Hors périmètre : test de `publish` en dépôt cible.

## Acceptance criteria

- `kanban-rememory/` contient `orchestrator/` et `documentation/` ; la racine garde `AGENTS.md`, `CLAUDE.md`, `GUARDRAILS.md`, `project/`.
- Aucune référence à un ancien chemin dans les outils, les tests et les documents vivants.
- `kr validate`, `test-kr.py` et `test-telegram.py` passent depuis le nouvel emplacement.
- Suivre `install.md` dans un dépôt vierge donne un `kr show` valide.
