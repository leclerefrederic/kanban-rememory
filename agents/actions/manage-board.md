# Operate the board

Prerequisites: approved action, [Kanban rules](../guidelines/kanban.md), Python 3.9+ and Git. Run from the project root. This CLI does not grant execution or publication authority.

In multi-module projects use the shared board. Select `--scope MODULE` or `--scope @project` when creating a Card. `--module` is an alias. Card IDs are project-wide. Module Spec and Batch references stay qualified. Active Card moves require the recorded `--owner-token` from [delivery coordination](coordinate-modules.md).

## Inspect and validate

```sh
python3 agents/tools/manage-kanban-board.py show
python3 agents/tools/manage-kanban-board.py validate
```

`show` uses configured stage order, active/WIP settings, dates and blockers. `--wip-limit` or `--timezone` overrides one display run, not the approved policy. `validate` is read-only: invalid filenames, duplicate numeric IDs, missing inline relative Markdown targets/ATX anchors and unchecked completed acceptance criteria return exit 1. Historical Cards without checklists remain accepted. External URLs, reference-style links and HTML anchors are not checked.

Use `show --scope MODULE` for the module view or an unassigned project session for the complete view. Use `history MODULE/CARD-ID` to locate a frozen Card from a previous module board. After an approved scope reassignment, a project-scoped Writer can use `reassign CARD-ID --to-scope MODULE --scope @project` on an unclaimed backlog Card whose Batch/Spec references have been resolved. Scope stays fixed after pickup.

## Create

```sh
python3 agents/tools/manage-kanban-board.py new "Verify retries" --owner "Billing team"
```

Preview first; add `--apply` when project intake permits creating the proposed backlog record. This is not permission to execute. Complete the [Card content](write-card.md) before pickup.

The next numeric ID follows the highest CARD or legacy TASK number across every stage, including Cancellation. Use eight digits (`CARD-00000001` through `CARD-99999999`); never reuse a retired number. Recheck before integrating concurrent contributions: the preview ID can change. Agree a migration before exhausting the range. The first stage is intake unless `intake` selects another non-active, non-completed stage.

## Move

```sh
python3 agents/tools/manage-kanban-board.py move CARD-00000019 development
python3 agents/tools/manage-kanban-board.py validate
```

Substitute the approved stage. `transitions` maps source stages to permitted destinations; starter workflows include rework and Cancellation. The tool checks capacity when entering active work and requires nonempty fully checked acceptance criteria before completion. It preserves ID/filename/start date and updates inline relative links to/from the moved Card, including anchors. Review other formats and outside-repository references separately. Record authorization, state, dates and evidence on the Card; inspect any refusal before retrying.

## Legacy lookup

Left-pad old numeric suffixes and replace TASK with CARD: `TASK-0015` identifies `CARD-00000015`; eight-digit legacy IDs retain their number and slug. The tool still reads unmigrated projects. To inspect published Card history, use a role allowed Git and the fetched published branch, for example:

```sh
git log origin/main --full-history --name-status -- ':(glob)project/kanban/**/card-00000029-*.md' ':(glob)project/kanban/**/task-00000029-*.md'
```

Git shows committed transitions; a commit date does not prove push time. Record tested revision separately from the publishing commit, which cannot contain its own hash.
