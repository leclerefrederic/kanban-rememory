---
id: "CARD-00000178"
module: "orchestrator"
---

# CARD-00000178 — Retirer les cases à cocher des critères et limiter la trace de la Card à l'utile

- Dependencies: Aucune.

## Expected outcome

`kr` n'exige plus de cocher les critères d'acceptation, et la Card ne garde que ce qu'un outil ou l'utilisateur relit : les critères, les décisions de l'utilisateur, les déplacements de stage et l'approbation.

## Scope and authorization

Demande de l'utilisateur du 2026-11-16 : cocher les critères et ajouter des lignes d'historique à la main est du travail sans effet ; garder l'essentiel et la trace de ce qui est pertinent. Conserver les lignes de déplacement de stage et d'approbation écrites par `kr` : `markdown.py` et `report.py` en tirent les durées. Les Cards existantes restent inchangées. Hors périmètre : les durées, le journal, le ledger Telegram.

## Acceptance criteria

- `publish` et `validate` n'échouent plus sur un critère non coché ; une Card avec des cases cochées ou sans case reste valide.
- Le workflow et le modèle de Card décrivent les critères comme une liste simple et limitent les lignes d'historique manuelles aux décisions de l'utilisateur.
- Les champs du modèle qu'aucun outil ne lit et qui restent vides sont retirés, sans casser `validate`.
- `test-kr.py` et `validate` passent.

## Execution and evidence

## History

- 2026-11-16T00:36:57+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T00:40:45+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T00:40:45+01:00 — Merge approved for the verified candidate `280eb218fdb770e8136589e59c8c8b710bf89e15`: “Approuvé”.
