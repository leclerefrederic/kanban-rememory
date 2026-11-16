---
id: "CARD-00000196"
module: "orchestrator"
---

# CARD-00000196 — Corriger les lacunes de la procédure d'installation

- Dependencies: Aucune.

## Expected outcome

`orchestrator/install.md` mène à une installation qui fonctionne de bout en bout : fichiers copiés explicitement, `GUARDRAILS.md` inclus, prérequis Git posés, mise à jour possible.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, après audit et test dans un dépôt jetable. Travail sur `main`. Seul `orchestrator/install.md` change.

- Liste de copie explicite, avec `GUARDRAILS.md` copié seulement s'il est absent.
- Permissions Git écrites dans la section `Overrides` de `GUARDRAILS.md`, plus dans `AGENTS.md`.
- Prérequis Git : branche `main`, commit initial, remote `origin` avec `main` poussée.
- Upgrade : fichiers du kit et fichiers de l'utilisateur distingués ; commit du kit consigné dans le journal à l'installation et à la mise à jour.
- Verify : contrôle de `GUARDRAILS.md` et du remote ; ligne vide avant le titre.
- Hors périmètre : code de `kr`, test de `publish` et d'Upgrade.

## Acceptance criteria

- Suivre `install.md` dans un dépôt vide permet `kr start --main` et `kr check`.
- `install.md` ne cite plus les permissions Git dans `AGENTS.md`.
- `validate` passe.

## History

- 2026-11-16T11:56:47+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T11:57:17+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T11:57:17+01:00 — Merge approved for the verified candidate `05167570670d72bcba4864e9051039ed0b42f91b`: “Approuvé”.
