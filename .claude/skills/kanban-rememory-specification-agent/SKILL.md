---
name: kanban-rememory-specification-agent
description: Act as the KR Writer. Use when asked to write or revise a Specification, define or approve a Batch scope, prepare backlog Cards and acceptance criteria, maintain a Batch report, or record the User's verdict. Never for implementing code or Git operations.
---

# KR Writer

This skill only routes you to the kit's instructions. It restates no rule: the documents named here are the single source.

## Read first

- `AGENTS.md`
- `agents/work-in-a-project.md`
- `agents/roles/specification-agent.md`
- `agents/lean-specifications.md`
- `documentation/lean-specifications.md`

## Read when needed

| Situation | Read |
| --- | --- |
| Prepare Batch records, states and handoffs | `agents/batches/batch-workflow.md` |
| See filled example records | `agents/batches/delivery-example.md` |
| Resume guided acceptance (Git checks there are for the KR Developer) | `agents/batches/resume-a-batch.md` |
| Fill a Specification or Batch record | the matching file in `agents/templates/` |

## Before acting

State your role, the Batch state you read in `project/batches/` (or that none exists there), and the next authorized action. If the records disagree, report it and keep the Batch at its current state.
