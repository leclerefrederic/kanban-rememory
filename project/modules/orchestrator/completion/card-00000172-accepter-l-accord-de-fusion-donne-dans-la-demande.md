---
id: "CARD-00000172"
module: "orchestrator"
---

# CARD-00000172 — Accepter l'accord de fusion donné dans la demande

- Dependencies: Aucune. Modifie la règle d’accord de CARD-00000160.

## Expected outcome

Quand la demande de l’utilisateur contient déjà l’accord de fusion, l’Orchestrator publie le candidat vérifié sans le redemander.

## Scope and authorization

Décision de l’utilisateur du 2026-11-15 (« Oui, 2 à 4 »), point 3 présenté dans le chat. La demande autorise l’exécution. Un accord donné dans la demande, par exemple « fais-le et fusionne », vaut pour le candidat dès que `check` le vérifie dans le périmètre demandé, sans alerte de fusion. L’Orchestrator redemande si la vérification échoue ou si le changement dépasse la demande.

## Acceptance criteria

- [x] `workflow.md` décrit l’accord donné dans la demande et les cas où il faut redemander ; `AGENTS.md` y renvoie sans le répéter.
- [x] `guide.md` l’explique à l’utilisateur.
- [x] `validate` passe.

## Execution and evidence

- State:
- Blocker:

## History

- 2026-11-15 — Créée à la demande de l’utilisateur.

- 2026-11-15T23:54:46+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-15T23:55:03+01:00 — Stage moved from `development` to `completion`.
