---
id: "CARD-00000217"
module: "orchestrator"
---

# CARD-00000217 — Le kit embarque tous les scripts d'installation

- Dependencies: None. Fait suite à la Card 216.

## Expected outcome

`dist/build-kit.py` met dans le ZIP tous les fichiers de `dist/installer/` (version de HEAD), sauf les tests (`test-*`), sous `<dossier du kit>/installer/`. Plus aucun nom de script en dur dans le builder : un script ajouté dans `dist/installer/` part dans le kit sans toucher au builder.

## Scope and authorization

`dist/build-kit.py`, `dist/test-build-kit.py`, ZIP reconstruit. Demande de l'utilisateur : « il faut revoir le kit builder car il doit embarquer les scripts d'installation dans le zip ».

## Acceptance criteria

- Le test du builder prouve qu'un second script de `dist/installer/` est dans le ZIP et qu'un `test-*` n'y est pas.
- Le ZIP reconstruit contient `installer/init.py` et pas `installer/test-init.py`.
- `kr validate` passe.

## History

- 2026-11-16T16:24:36+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T16:34:01+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T16:34:01+01:00 — Merge approved for the verified candidate `def446171aeac77aca04b9b152227510a606067c`: “Oui, commit”.
