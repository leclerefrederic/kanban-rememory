# Installed project layout

This is the resulting layout, not a copy list. [Installation](install.md) owns copying/configuration and [workflow setup](configure-workflow.md) creates the approved stage folders. Keep existing product code/tests alongside it.

```text
repository/
  AGENTS.md, CLAUDE.md             Project permissions and shared startup
  documentation/                  Human guides and examples
  agents/
    index.md, VERSION
    guidelines/, actions/, setup/
    roles/                        orchestrator, writer, developer, tester
    templates/                    card, rememory-day, specification, batch-*
    tools/                        manage-kanban-board.py, kanban/
    skills/                       Optional distributed role routers
    hosts/claude/agents/           Optional distributed native adapters
  .agents/skills/                  Optional Codex discovery copies
  .claude/skills/, agents/         Optional Claude discovery copies
  project/
    kanban/
      workflow.json
      backlog/, development/, code-review/, completion/, cancellation/
    rememory/
```

The example is Standard; the actual configured workflow owns stage names/order and active WIP. Cards live in their stage folders, journals by date/owner in Rememory. Kit templates remain under agents, never as a dated project journal.

With modules, root `project.json` declares their workspace locations. The project board and journal stay above the module workspaces. Each workspace has its own `rememory/` and, when enabled, `specifications/` and `batches/`. A project's Cards carry a module or project scope and use one shared sequence of IDs.

With the Batch module:

```text
project/
  specifications/
    draft/, ready/, approved/, retired/
    resources/active/, resources/archived/
  batches/
    batch-001/
      description.md
      tests.md
      report.md
      evidence/                   Create with the first attachment
```

A ready Batch pins the approved Specifications by their stable IDs and paths. Specs travel from draft to ready to approved, then retire when their Batch closes. Existing workspaces using `specs/` retain that name and their frozen paths. IDs are `SPEC-001`, `Batch-001`; paths remain lowercase. Cards reference Batch/Spec IDs, never the reverse. Local guards belong in the shared Git directory. Each adopting project starts with its own workflow, Cards, Specs, Batches and dated records.
