---
id: "CARD-00000218"
module: "orchestrator"
---

# CARD-00000218 — Lever les ambiguïtés d'INSTALL.md relevées par l'essai en bac à sable

- Dependencies: None. Fait suite à la Card 217 et à l'essai d'installation en bac à sable.

## Expected outcome

`dist/INSTALL.md` ne laisse plus de décision implicite à l'agent sur : la place de `misc` dans `modules`, la forme des clés de `workflow` et des `transitions` (stages sans sortie), la valeur de `KIT` dans les commandes, le format d'une ligne de permission dans `GUARDRAILS.md`, et le sort des dossiers temporaires.

## Scope and authorization

`dist/INSTALL.md` seulement ; le ZIP ne change pas. Demande de l'utilisateur : « lève ces ambiguïtés dans une Card ».

## Acceptance criteria

- `misc` est ajouté en dernier dans `modules`.
- `INSTALL.md` donne les clés exactes de `workflow` et dit que `completion` et `cancellation` n'ont pas de clé dans `transitions`.
- `KIT` est défini une fois comme chemin absolu à substituer dans les commandes.
- Le format d'une ligne de permission est donné.
- Les dossiers temporaires sont supprimés à la fin.
- `kr validate` passe.

## History

- 2026-11-16T17:01:39+01:00 — Stage moved from `backlog` to `development`.
