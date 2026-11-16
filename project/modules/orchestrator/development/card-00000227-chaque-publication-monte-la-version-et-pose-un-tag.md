---
id: "CARD-00000227"
module: "orchestrator"
---

# CARD-00000227 — Chaque publication monte la version et pose un tag

- Dependencies: None. Fait suite à la Card 226 ; décision de l'utilisateur sur la numérotation.

## Expected outcome

Chaque `kr publish` monte `version` dans le commit de clôture, pose le tag `vX.Y.Z` sur ce commit et le pousse, sur `main` comme en release. Une publication sur `main` monte le patch par défaut (`0.1.0` → `0.1.1`) ; une release sur branche monte le minor et remet le patch à zéro (`0.1.7` → `0.2.0`) ; `--bump patch|minor|major` force un autre cran. Le numéro du kit suit : `build-kit.py` prend `version` du commit de clôture, qui est le tag courant. `workflow.md`, `guide.md` et `INSTALL.md` le disent.

## Scope and authorization

`kr.py`, `kanban/phase.py`, `test-kr.py`, `workflow.md`, `guide.md`, `dist/INSTALL.md`, ZIP reconstruit. Demandes de l'utilisateur : « une update sur main pourrait être un incrément … et mis à jour dans la version du kit quand on build », « pour moi … 0.0.X une branche 0.X.0 », « je mettrais 0.0.XX même ».

## Acceptance criteria

- Une publication sur `main` monte le patch, tague et pousse le tag ; une release sans `--bump` monte le minor.
- `kr versions` liste ces publications.
- `test-kr.py`, `kr validate` passent ; le ZIP porte le nouveau numéro.

## History

- 2026-11-16T20:16:21+01:00 — Stage moved from `backlog` to `development`.
