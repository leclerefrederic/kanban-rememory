---
id: "CARD-00000197"
module: "orchestrator"
---

# CARD-00000197 — Réduire l'étape 1 de l'installation au minimum requis

- Dependencies: Aucune.

## Expected outcome

La première étape de `orchestrator/install.md` ne vérifie que le minimum requis : les outils sont disponibles et le répertoire de travail est un dépôt Git.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16, première étape de la relecture pas à pas de `install.md`, successeur de CARD-00000196. Travail sur `main`.

- Étape 1 : Python 3.9+ et Git disponibles, le répertoire de travail est un dépôt Git (sinon, demander l'accord pour en créer un).
- Retirer de l'étape 1 le prérequis du remote `origin` ; la lecture des instructions et des réglages existants passe au début de l'étape 2.
- Hors périmètre : les étapes suivantes, relues ensuite une par une.

## Acceptance criteria

- L'étape 1 tient en une phrase et ne cite que les outils et le dépôt Git.
- `validate` passe.

## History

- 2026-11-16T12:02:13+01:00 — Stage moved from `backlog` to `development`.
