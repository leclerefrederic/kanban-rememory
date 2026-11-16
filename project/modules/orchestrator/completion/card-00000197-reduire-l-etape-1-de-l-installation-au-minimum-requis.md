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
- Portée élargie le 2026-11-16 : relecture complète de `install.md` en une seule livraison (sections Check, Agree, Close the gaps, Verify ; comparaison fichier par fichier du kit, sans empreinte ni manifeste ; le kit = `orchestrator/`, `documentation/`, `CLAUDE.md`, `AGENTS.md`, `GUARDRAILS.md`).
- Retrait de la ligne d'autorisation permanente de push dans `AGENTS.md`, à la demande de l'utilisateur : chaque push reste soumis à son approbation.

## Acceptance criteria

- `install.md` suit Check, Agree, Close the gaps, Verify, sans contradiction interne.
- `AGENTS.md` ne contient plus d'autorisation permanente de push.
- `validate` passe.

## History

- 2026-11-16T12:02:13+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T12:57:06+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T12:57:06+01:00 — Merge approved for the verified candidate `4b1c07e91d8d206b18235bc9ba6e6f18b1526f9a`: “Approuvé”.
