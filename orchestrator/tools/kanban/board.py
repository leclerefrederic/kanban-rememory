"""Cards on the module boards: list, show, create and move."""

import json
from pathlib import Path
import re
from unicodedata import normalize

from .markdown import card_id, field, header_value, moves, prose_lines, unchecked
from .project import MISC

TEMPLATE = Path(__file__).resolve().parents[2] / "templates/card.md"


def cards(project, stage, module=None):
    """Card files of one stage, on one board or all of them, ordered by ID."""
    paths = [path for name in (project.modules if module is None else (module,))
             for path in (project.board(name) / stage).glob("*.md") if card_id(path)]
    return sorted(paths, key=lambda path: (card_id(path), path.name))


def find_card(project, task_id):
    """Return (module, stage, path) of the only Card with this ID."""
    matches = [(stage, path) for stage in project.workflow["stages"] for path in cards(project, stage)
               if card_id(path) == task_id]
    if len(matches) != 1:
        raise ValueError(f"Expected one Card {task_id}, found {len(matches)}.")
    stage, path = matches[0]
    return path.parent.parent.name, stage, path


def local(directory):
    """A record directory, refused when reached through a symbolic link."""
    if directory.resolve() != directory:
        raise ValueError(f"Record path goes through a symbolic link: {directory}.")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def show(project, module=None, phase=None, action=None):
    workflow = project.workflow
    today = project.now().date()
    if phase:
        verified = phase["verified"] or "no"
        print(f"Phase: {', '.join(phase['cards'])} ({phase['module']}) on {phase['branch']}, "
              f"{phase.get('mode', 'release')}; verified: {verified}")
        print(f"Next: {action}")
    else:
        print("Phase: none")
    wip = {name: 0 for name in project.modules}
    for stage in workflow["stages"]:
        paths = cards(project, stage, module)
        if stage in project.frozen:
            print(f"{stage}: {len(paths)} Cards")
            continue
        print(stage)
        for path in paths:
            source = path.read_text(encoding="utf-8")
            name, task_id = path.parent.parent.name, card_id(path)
            heading = next((line[2:] for _, line in prose_lines(source.splitlines()) if line.startswith("# ")),
                           path.stem)
            print(f"  {task_id} | {name} | {heading.removeprefix(task_id).lstrip(' —-')} | "
                  f"{path.relative_to(project.root)}")
            if stage in workflow["active"]:
                wip[name] += 1
                started = next((at for at, to in moves(source) if to in workflow["active"]), None)
                details = [f"age {(today - started.date()).days} days" if started else "age unknown"]
                for label in ("State", "Blocker"):
                    if value := field(source, label):
                        details.append(f"{label.lower()}: {value}")
                print(f"    {'; '.join(details)}")
        if module not in (None, MISC):
            for path in cards(project, stage, MISC):
                affected = header_value(path.read_text(encoding="utf-8"), "affected_modules")
                if isinstance(affected, list) and module in affected:
                    print(f"  {card_id(path)} | linked from {MISC} | {path.relative_to(project.root)}")
    for name in (project.modules if module is None else (module,)):
        print(f"{name} WIP: {wip[name]}/{workflow['wip_limit']}")
    return 0


def new(project, title, module, body=None):
    title = title.strip()
    if not title or "\n" in title or "\r" in title:
        raise ValueError("The title must be a nonempty single line.")
    board = project.board(module)
    highest, seen = project.last_card_id, set()
    for stage in project.workflow["stages"]:
        for path in cards(project, stage):
            task_id = card_id(path)
            if task_id in seen:
                raise ValueError(f"Duplicate {task_id}. Resolve the collision before creating a Card.")
            seen.add(task_id)
            highest = max(highest, int(task_id[5:]))
    if highest >= 99999999:
        raise ValueError("The eight-digit Card range is exhausted.")
    task_id = f"CARD-{highest + 1:08d}"
    slug = normalize("NFKD", title).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")[:80].rstrip("-") or "card"
    content = (TEMPLATE.read_text(encoding="utf-8").replace('"MODULE"', json.dumps(module))
               .replace("CARD-NNNNNNNN", task_id).replace("TITLE", title, 1))
    heading = f"# {task_id} — {title}\n"
    if f'id: "{task_id}"' not in content or f"module: {json.dumps(module)}" not in content or heading not in content:
        raise ValueError("The Card template needs its id, module and heading placeholders.")
    if body is not None:
        if not body.strip():
            raise ValueError("--body read an empty Card body from stdin.")
        content = content[:content.index(heading) + len(heading)] + "\n" + body.strip() + "\n"
    target = local(board / project.workflow["stages"][0]) / f"{task_id.lower()}-{slug}.md"
    with target.open("x", encoding="utf-8") as stream:
        stream.write(content)
    print(f"Created {target.relative_to(project.root)}.")
    return target


def add_history(path, line):
    text = path.read_text(encoding="utf-8").rstrip()
    if not re.search(r"^## History$", text, re.MULTILINE):
        text += "\n\n## History"
    path.write_text(f"{text}\n\n- {line}\n", encoding="utf-8")


def move(project, task_id, destination, guard):
    """Move a Card along the workflow; guard(task_id, stage, destination) applies the phase rules."""
    workflow = project.workflow
    module, stage, card = find_card(project, task_id)
    if stage in project.frozen:
        raise ValueError(f"{task_id} is in {stage}: its record is history. Create a successor Card.")
    if destination not in workflow["transitions"].get(stage, []):
        raise ValueError(f"Transition from {stage} to {destination} is not allowed.")
    guard(task_id, stage, destination)
    active = workflow["active"]
    if destination in active and stage not in active and sum(
            len(cards(project, column, module)) for column in active) >= workflow["wip_limit"]:
        raise ValueError(f"WIP limit reached on {module}. Finish the active Card first.")
    text = card.read_text(encoding="utf-8")
    if destination == workflow["completed"] and unchecked(text):
        raise ValueError("Completion requires a nonempty acceptance checklist with every item checked.")
    target = local(project.board(module) / destination) / card.name
    with target.open("x", encoding="utf-8") as stream:
        stream.write(text)
    card.unlink()
    add_history(target, f"{project.now().isoformat(timespec='seconds')} — Stage moved from `{stage}` "
                        f"to `{destination}`.")
    print(f"Moved {task_id} from {stage} to {destination}.")
    return target
