# Project directory template

Copy the reusable files from the kit and create or merge the root AGENTS.md as described in the installation guide. Add this structure alongside the project's existing code and tests.

```text
project/
├── AGENTS.md
├── agents/
├── docs/
│   └── lot-templates/
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

## With the Lot module

Add these paths when the project adopts Lots. Create a Lot directory when preparing a specific Lot.

```text
project/
├── specs/
│   ├── draft/
│   ├── ready/
│   └── frozen/
└── lots/
    └── Lot-001/
        ├── Description.md
        ├── Tests.md
        └── Report.md
```

The Fiche directory determines its state. A Lot pins the approved Fiches in `specs/frozen/`. Its Journal is `Report.md`. Cards stay in `kanban/` and can reference a Lot or Fiches by ID.

Use lowercase names for workflow directories. Keep the established Rememory path for journals. The project template describes the layout. The installation guide lists the files to copy. Each project starts with its own workflow configuration, Cards, Fiches, Lots, and dated journals.
