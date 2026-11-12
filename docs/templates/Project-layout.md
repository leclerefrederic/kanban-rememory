# Project directory template

Copy the reusable files from the kit and create or merge the root AGENTS.md as described in the installation guide. Add this structure alongside the project's existing code and tests.

```text
project/
├── AGENTS.md
├── agents/
├── docs/
│   └── templates/
├── tools/
├── kanban/
│   ├── workflow.json
│   ├── backlog/
│   ├── development/
│   ├── code-review/
│   ├── completion/
│   └── archive/
└── Rememory/
```

The tree shows the Standard workflow. Run `init` after approval to create `kanban/workflow.json` and one directory per approved stage. The workflow file lists the actual stages. Keep Cards in their stage directories and daily execution notes in `Rememory/`.

## With the Batch module

Add these paths when the project adopts Batches. Create a Batch directory when preparing a specific Batch.

```text
project/
├── specs/
│   ├── draft/
│   ├── ready/
│   └── frozen/
└── batches/
    └── Batch-001/
        ├── Description.md
        ├── Tests.md
        └── Report.md
```

The Specification directory determines its state. A Batch pins the approved Specifications in `specs/frozen/`. Its Journal is `Report.md`. Cards stay in `kanban/` and can reference a Batch or Specifications by ID.

Use lowercase names for workflow directories. Keep the established Rememory path for journals. The project template describes the layout. The installation guide lists the files to copy. Each project starts with its own workflow configuration, Cards, Specifications, Batches, and dated journals.
