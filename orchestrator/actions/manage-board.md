# Operate the board

Run from the project root with Python 3.9+ and Git. The CLI grants no execution or publication authority. Card records live in the primary checkout; the tool writes there from any worktree. `--scope MODULE` selects a module; Card IDs are project-wide.

## Inspect and validate

```sh
python3 orchestrator/tools/manage-kanban-board.py show [--scope MODULE]
python3 orchestrator/tools/manage-kanban-board.py validate
python3 orchestrator/tools/manage-kanban-board.py path CARD-ID
```

`show` uses the stage order, WIP limit, dates and blockers; `--wip-limit` and `--timezone` override one display only. `validate` is read-only and exits 1 on invalid filenames, duplicate IDs, missing relative Markdown targets or anchors, and unchecked criteria on completed Cards. External URLs, reference-style links and HTML anchors are not checked. `path` resolves a stable ID to its current file.

## Create

```sh
python3 orchestrator/tools/manage-kanban-board.py new "Verify retries" --scope misc --owner Orchestrator
```

Preview first; add `--apply` to create the backlog Card. Complete the [Card content](write-card.md) before pickup. The next ID follows the highest Card number on all boards and `last_card_id` in project settings. IDs have eight digits (`CARD-00000001`); never reuse one. Recheck before integrating concurrent work: the preview ID can change.

## Move

```sh
python3 orchestrator/tools/manage-kanban-board.py move CARD-00000019 development --owner-token OWNER
```

`transitions` lists permitted destinations. Moves into, within or out of active stages require the delivery owner from [coordination](coordinate-modules.md). The tool checks capacity on entry and requires nonempty, fully checked criteria before completion. It keeps ID, filename and start date and updates inline relative links to and from the Card; it refuses when a link outside the module board and the journal would change. Inspect a refusal before retrying.

To read a Card's published history:

```sh
git log origin/main --full-history --name-status -- ':(glob)project/modules/**/card-00000029-*.md'
```

A commit date does not prove push time. A publishing commit cannot contain its own hash; record the tested revision separately.
