---
id: "CARD-00000209"
module: "orchestrator"
---

# CARD-00000209 — Générer le kit d'installation en archive ZIP

- Dependencies: None. Fait suite à la Card 208.

## Expected outcome

Un script produit `dist/kanban-rememory-kit-<version>.zip`, le kit décrit par `install.md` : le dossier `kanban-rememory/`, `kanban-rememory.json`, `AGENTS.md`, `CLAUDE.md` et `GUARDRAILS.md`, tels qu'ils sont dans `HEAD`, sous un dossier racine `kanban-rememory-kit-<version>/`. L'archive décompressée est un KIT valide pour `install.md`.

## Scope and authorization

Script `kanban-rememory/orchestrator/tools/build-kit.py`, son test dans `test-kr.py`, `dist/` dans `.gitignore`, et une mention dans `install.md` qu'un KIT peut être l'archive décompressée. Demande de l'utilisateur : « il faut un script qui va générer le kit d'installation sous la forme d'une archive ZIP ».

## Acceptance criteria

- Le contenu vient de `HEAD` (`git archive`) : ni `__pycache__/`, ni fichier non suivi.
- La version vient de `kanban-rememory.json` dans `HEAD`.
- Le test vérifie les noms contenus dans l'archive.
- `kr validate` passe.

## History

- 2026-11-16T14:04:03+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T14:05:45+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T14:05:45+01:00 — Merge approved for the verified candidate `8ca7d2d5be0adb04fd467d93554105e9c8574318`: “Oui, commit”.
