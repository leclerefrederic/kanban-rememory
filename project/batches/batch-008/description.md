---
type: batch
id: "Batch-008"
specifications: [{"id":"SPEC-011","revision":"1","path":"project/specs/approved/spec-011-r1.md"},{"id":"SPEC-012","revision":"1","path":"project/specs/approved/spec-012-r1.md"}]
status: closed
---

# Telegram alerts and Claude Code role-limit hook

## Objective

Scope approved by the User on 2026-11-14: [SPEC-011 revision 1](../../specs/approved/spec-011-r1.md) (Telegram alerts for attention and task completion), then [SPEC-012 revision 1](../../specs/approved/spec-012-r1.md) (optional role-limit hook for Claude Code).

## Execution constraints

SPEC-011 first, then SPEC-012; adjust the order only for technical dependencies. For SPEC-012, Claude Code only and Codex stays advisory. Use an isolated project and a confirmed test Telegram destination for SPEC-011 delivery checks, and a scratch repository with the kit adopted for SPEC-012.
