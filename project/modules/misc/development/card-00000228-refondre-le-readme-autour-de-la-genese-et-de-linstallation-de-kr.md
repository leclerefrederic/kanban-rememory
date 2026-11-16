---
id: "CARD-00000228"
module: "misc"
---

# CARD-00000228 — Refondre le README autour de la genèse et de l’installation de KR

- Dependencies: Aucune.

## Expected outcome

Un README en anglais, vivant et incisif, qui présente la genèse, l’intention, l’objectif et le résultat de Kanban Rememory, et permet de l’installer dans un dépôt Git.

## Scope and authorization

Réécriture de README.md demandée par l’utilisateur. Conserver l’anglais établi pour le README et son public de créateurs utilisant des agents IA. Installation fondée sur dist/INSTALL.md et le kit 0.1.49. Documentation uniquement ; ne pas modifier le kit ni la procédure d’installation.

Décision explicite : « sur main en fast forward car je ne veux pas de montée de version. » Travailler sur main ; conserver version 0.1.49, sans nouveau tag. Faire vérifier le candidat avant le push. Cette décision remplace la montée de version automatique du workflow pour cette livraison documentaire.

## Acceptance criteria

- La genèse expose le problème de perte de contexte sans inventer d’histoire personnelle.
- L’intention, le public, le fonctionnement et le résultat réel sont compréhensibles sans connaître KR.
- Le ton anglais est énergique et accessible.
- L’installation nomme les prérequis, les deux fichiers à récupérer, leur emplacement et la consigne à donner à l’agent.
- Les effets de l’installation et le parcours d’une première tâche correspondent à INSTALL.md et au guide.
- Les liens locaux et validate passent ; la version reste 0.1.49 et aucun nouveau tag n’est créé.

## Execution and evidence

README réécrit en anglais selon les conventions établies. Genèse fondée sur le problème de contexte ; résultat des cinq Cards étayé par CARD-00000179. Installation comparée à dist/INSTALL.md ; liens locaux et ancre vérifiés ; VERSION du ZIP et version du projet égales à 0.1.49. Aucun code ni kit modifié.

## History

- 2026-11-16T20:41:34+01:00 — Stage moved from `backlog` to `development`.
