# Project directory template

Copy the reusable files from the kit and create or merge the root AGENTS.md as described in the installation guide. Add this structure alongside the project's existing code and tests.

```text
repository/
├── AGENTS.md
├── README.md
├── docs/
│   ├── agents/
│   └── templates/
├── tools/
└── project/
    ├── kanban/
    │   ├── workflow.json
    │   ├── backlog/
    │   ├── development/
    │   ├── code-review/
    │   ├── completion/
    │   └── archive/
    └── rememory/
```

The tree shows the Standard workflow. Run `init` after approval to create `project/kanban/workflow.json` and one directory per approved stage. The workflow file lists the actual stages. Keep Cards in their stage directories and daily execution notes in `project/rememory/`.

## With the Batch module

Add these paths when the project adopts Batches. Create a Batch directory when preparing a specific Batch.

```text
project/
├── specs/
│   ├── draft/
│   ├── ready/
│   └── frozen/
└── batches/
    └── batch-001/
        ├── description.md
        ├── tests.md
        └── report.md
```

The Specification directory determines its state. A Batch pins the approved Specifications in `project/specs/frozen/`. Its Journal is `report.md`. Cards stay in `project/kanban/` and can reference a Batch or Specifications by ID.

Use lowercase names for workflow directories. The project template describes the layout. The installation guide lists the files to copy. Each project starts with its own workflow configuration, Cards, Specifications, Batches, and dated journals.
