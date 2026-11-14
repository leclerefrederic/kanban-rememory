# Project directory template

Copy the reusable files from the kit and create or merge the root AGENTS.md as described in the installation guide. Add this structure alongside the project's existing code and tests.

```text
repository/
├── AGENTS.md
├── documentation/
│   ├── index.md
│   ├── lean-specifications.md
│   └── ...
├── agents/
│   ├── lean-specifications.md
│   ├── maintain-rememory.md
│   ├── kanban/
│   ├── roles/
│   ├── templates/
│   │   ├── kanban-card.md
│   │   ├── daily-template.md
│   │   └── project-layout.md
│   └── tools/
│       ├── manage-kanban-board.py
│       └── kanban/
└── project/
    ├── kanban/
    │   ├── workflow.json
    │   ├── backlog/
    │   ├── development/
    │   ├── code-review/
    │   ├── completion/
    │   └── cancellation/
    └── rememory/
```

The tree shows the Standard workflow. Run `init` after approval to create `project/kanban/workflow.json` and one directory per approved stage. The workflow file lists the actual stages. Keep Cards in their stage directories and daily execution notes in `project/rememory/`.

## With the Batch module

Copy all operating references under `agents/batches/`, `agents/run-scheduled-batch-job.md`, the Specification and three Batch templates under `agents/templates/`, and `agents/tools/guard-batch-work.py` as listed in the installation procedure. Add the project paths below when adopting Batches. Create a Batch directory when preparing a specific Batch; keep local guard records in the shared Git directory as described in the Batch operations guide.

```text
project/
├── specs/
│   ├── draft/
│   ├── ready/
│   ├── approved/
│   └── resources/
│       ├── active/
│       └── archived/
└── batches/
    └── batch-001/
        ├── description.md
        ├── tests.md
        ├── report.md
        └── evidence/
```

The Specification directory determines its state. A ready Batch pins approved Specifications in `project/specs/approved/`. Its report and handoff are in `report.md`. Cards stay in `project/kanban/` and can reference a Batch or Specifications by ID. A Batch's ID is `Batch-001`; its directory is `batch-001/`.

Use lowercase names for workflow directories. The project template describes the layout. The installation guide lists the files to copy. Each project starts with its own workflow configuration, Cards, Specifications, Batches, and dated journals.

Create the Batch evidence directory when adding the first attachment.
