---
id: "CARD-00000176"
module: "orchestrator"
---

# CARD-00000176 — Lister les versions publiees avec kr versions

- Dependencies: Aucune.

## Expected outcome

`kr versions` liste les tags `vX.Y.Z`, du plus récent au plus ancien, avec la date et le sujet du commit de clôture, et indique la version courante de `settings.json`.

## Scope and authorization

Demande de l’utilisateur du 2026-11-16 (voir la Card du lanceur `kr`). Lecture seule, tags locaux uniquement. Pas de génération de notes de version : le journal les contient déjà.

## Acceptance criteria

- [ ] `kr versions` affiche une ligne par tag `vX.Y.Z` : tag, date, sujet.
- [ ] La version courante de `settings.json` est affichée ; sans tag, un message l’indique.
- [ ] Un test de `test-kr.py` le couvre ; `workflow.md` ou `guide.md` mentionne la commande ; `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-16 — Créée à la demande de l’utilisateur.
