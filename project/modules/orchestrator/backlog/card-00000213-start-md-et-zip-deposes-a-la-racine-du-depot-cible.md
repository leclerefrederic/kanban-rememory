---
id: "CARD-00000213"
module: "orchestrator"
---

# CARD-00000213 — START.md et ZIP déposés à la racine du dépôt cible

- Dependencies: None. Fait suite à la Card 212.

## Expected outcome

L'utilisateur dépose `START.md` et le ZIP à la racine de son dépôt et dit à son agent « Follow START.md ». `START.md` s'adresse à l'agent : décompresser le ZIP dans un dossier hors du dépôt (`mktemp -d`), suivre `install.md`, puis demander s'il faut supprimer `START.md` et le ZIP. `install.md` ignore ces deux fichiers dans le contrôle « checkout propre » et ne les ajoute jamais au commit.

## Scope and authorization

Modèle `start.md`, `install.md` (prérequis et vérification « checkout propre »), test de `build-kit.py`. Exécution de `START.md` dans un dépôt de test jetable, hors de ce dépôt. Demande de l'utilisateur : « mets START et le ZIP à la racine de ton repo » et « fais exécuter les instructions de START.md ».

## Acceptance criteria

- `START.md` généré contient le nom du ZIP, `mktemp -d` et l'ordre de suivre `install.md`.
- L'installation de test dans un dépôt jetable aboutit : `kr validate` passe, `START.md` et le ZIP ne sont pas commités.
- `kr validate` passe ici.

## History
