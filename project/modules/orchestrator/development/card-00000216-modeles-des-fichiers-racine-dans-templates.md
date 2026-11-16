---
id: "CARD-00000216"
module: "orchestrator"
---

# CARD-00000216 — Modèles des fichiers racine dans templates/

- Dependencies: None. Fait suite à la Card 215.

## Expected outcome

`kanban-rememory/orchestrator/templates/` contient, suivis par Git, les modèles des cinq fichiers que l'installation écrit à la racine d'un projet : `GUARDRAILS.md` (copie de celui de ce dépôt), `AGENTS.md`, `CLAUDE.md`, `.gitignore` et `.gitattributes`. `INSTALL.md` les lit : fichier absent, copie du modèle ; fichier présent, ajout des lignes du modèle qui n'y sont pas (`GUARDRAILS.md` présent reste intact, hors permissions). `build-kit.py` ne génère plus le modèle `GUARDRAILS.md` : il est dans le kit comme les autres.

## Scope and authorization

Les cinq modèles, `dist/INSTALL.md`, `dist/build-kit.py` et son test, ZIP reconstruit. `.gitignore` et `.gitattributes` ne contiennent que les lignes que l'installation ajoute, pas le contenu du `.gitignore` de ce dépôt. Demande de l'utilisateur : « tu vas mettre dans templates une copie de GUARDRAILS, CLAUDE et AGENTS, .gitignore et .gitattributes ».

## Acceptance criteria

- Les cinq modèles existent dans `templates/` et sont dans le ZIP.
- `INSTALL.md` ne contient plus de ligne en dur pour `AGENTS.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`.
- `kr validate` passe.

## History

- 2026-11-16T15:26:27+01:00 — Stage moved from `backlog` to `development`.
