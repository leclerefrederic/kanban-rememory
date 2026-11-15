"""One phase at a time: a branch and a worktree that deliver Cards of one module with one approval."""

from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile

from .board import add_history, find_card, local, move
from .markdown import unchecked
from .project import JOURNAL, MODULES, common_directory, git, linked_worktree
from .report import report
from .validation import validate

RECORDS = (f"{MODULES.as_posix()}/", f"{JOURNAL.as_posix()}/")


def is_ancestor(root, ancestor, revision):
    result = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, revision], cwd=root)
    if result.returncode not in (0, 1):
        result.check_returncode()
    return result.returncode == 0


def require_clean(root):
    if git(root, "status", "--porcelain", "--untracked-files=normal"):
        raise ValueError("Commit or remove the local changes first: only a committed revision counts.")


def origin_main(root):
    try:
        git(root, "fetch", "--quiet", "origin", "main")
    except subprocess.CalledProcessError:
        raise ValueError("Could not fetch origin/main: check and publish compare with it.") from None
    return git(root, "rev-parse", "refs/remotes/origin/main")


class Phase:
    def __init__(self, project):
        self.project = project
        self.root = project.root
        self.common = common_directory(self.root)
        self.file = self.common / "kanban-rememory/phase.json"

    def state(self):
        return json.loads(self.file.read_text(encoding="utf-8")) if self.file.exists() else None

    def save(self, state, create=False):
        self.file.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(state, indent=2) + "\n"
        if create:
            try:
                with self.file.open("x", encoding="utf-8") as stream:  # one phase at a time
                    stream.write(text)
            except FileExistsError:
                raise ValueError("Another phase is active: run show.") from None
            return
        descriptor, pending = tempfile.mkstemp(dir=self.file.parent, prefix=".phase-")
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(text)
        os.replace(pending, self.file)

    def branch(self):
        try:
            return git(self.root, "symbolic-ref", "--quiet", "--short", "HEAD")
        except subprocess.CalledProcessError:
            raise ValueError("Check out the phase branch: HEAD is detached.") from None

    def here(self):
        """The active phase, provided this command runs in its worktree and branch."""
        state = self.state()
        if state is None:
            raise ValueError("No active phase: run start CARD-ID in a dedicated worktree.")
        if state["worktree"] != str(self.root) or state["branch"] != self.branch():
            raise ValueError(f"The active phase runs in {state['worktree']} on {state['branch']}: "
                             "work on the records there.")
        return state

    def guard_write(self):
        """During a phase, the records change only in its worktree."""
        if self.state() is not None:
            self.here()

    def guard_move(self, task_id, stage, destination):
        active = self.project.workflow["active"]
        if destination in active and stage not in active:
            raise ValueError(f"Begin a Card with: start {task_id}.")
        self.guard_write()
        state = self.state()
        if (stage in active or destination in active) and (state is None or task_id not in state["cards"]):
            raise ValueError(f"{task_id} is not in the active phase.")

    def start(self, task_id):
        """Open the phase with its first Card, or add the next Card, and move it to the first active stage."""
        module, _, _ = find_card(self.project, task_id)
        previous = self.state()
        if previous is None:
            branch = self.branch()
            if branch == "main" or not linked_worktree(self.root):
                raise ValueError("Start a phase in a dedicated worktree and branch, never on main.")
            state = {"module": module, "cards": [task_id], "branch": branch, "worktree": str(self.root),
                     "started": self.project.now().isoformat(timespec="seconds"), "verified": None}
        else:
            self.here()
            if module != previous["module"]:
                raise ValueError(f"The phase delivers {previous['module']} Cards; {task_id} belongs to {module}.")
            state = {**previous, "cards": [*previous["cards"], task_id]} if task_id not in previous["cards"] else previous
        self.save(state, create=previous is None)
        try:
            move(self.project, task_id, self.project.workflow["active"][0], lambda *_: None)
        except (OSError, ValueError):
            if previous is None:
                self.file.unlink()
            else:
                self.save(previous)
            raise
        return 0

    def check(self, commands):
        """Validate, then run each command, on the clean phase worktree; record the verified revision."""
        state = self.here()
        state["verified"] = None
        self.save(state)
        require_clean(self.root)
        head = git(self.root, "rev-parse", "HEAD")
        if not is_ancestor(self.root, origin_main(self.root), head):
            raise ValueError("Merge origin/main into the phase branch, then check again.")
        if validate(self.project):
            return 1
        workflows = sorted(path.name for path in (self.root / ".github/workflows").glob("*.y*ml"))
        print(f"CI workflows: {', '.join(workflows) or 'none'}", flush=True)
        for command in commands:
            print(f"$ {' '.join(command)}", flush=True)
            code = subprocess.call(command, cwd=self.root)
            if code:
                return code
        require_clean(self.root)
        if git(self.root, "rev-parse", "HEAD") != head:
            raise ValueError("HEAD changed during the check.")
        state["verified"] = head
        self.save(state)
        print(f"Verified revision: {head}")
        return 0

    def close(self, summary, approval):
        """After the approval of the verified revision: complete the Cards, record the approval and the journal."""
        if any(not text.strip() or "\n" in text or "\r" in text for text in (summary, approval)):
            raise ValueError("Give --summary and --approval as nonempty single lines.")
        state = self.here()
        require_clean(self.root)
        head = git(self.root, "rev-parse", "HEAD")
        if state["verified"] != head:
            raise ValueError(f"HEAD {head} is not verified: run check, then ask for approval of that revision.")
        workflow = self.project.workflow
        completed = workflow["completed"]
        found = [find_card(self.project, card) for card in state["cards"]]
        for card, (_, stage, path) in zip(state["cards"], found):
            if stage != completed and (completed not in workflow["transitions"].get(stage, [])
                                       or unchecked(path.read_text(encoding="utf-8"))):
                raise ValueError(f"Check every acceptance criterion of {card} before close.")
        now = self.project.now()
        paths = []
        for card, (_, stage, path) in zip(state["cards"], found):
            if stage != completed:
                path = move(self.project, card, completed, lambda *_: None)
            add_history(path, f"{now.isoformat(timespec='seconds')} — Merge approved for the verified "
                              f"candidate `{head}`: “{approval}”.")
            paths.append(path)
        texts = [(card, path.read_text(encoding="utf-8")) for card, path in zip(state["cards"], paths)]
        performance = report(datetime.fromisoformat(state["started"]), now, texts, workflow["active"], completed,
                             {self.root, self.common.parent})
        journal = local(self.project.journal)
        listed = f"Phase Cards: {', '.join(state['cards'])}.\n\n" if len(state["cards"]) > 1 else ""
        link = Path(os.path.relpath(paths[0], journal)).as_posix()
        entry = (f"## {state['module']}/{state['cards'][0]}\n\n{summary}\n\n{listed}{performance}\n\n"
                 f"Verified revision: `{head}`. [Card](<{link}>).")
        day = journal / f"{now.date().isoformat()}.md"
        current = day.read_text(encoding="utf-8") if day.exists() else f"# {now.date()} ({workflow['timezone']})\n"
        title, _, rest = current.partition("\n")
        day.write_text(f"{title}\n\n{entry}\n\n{rest.strip()}".rstrip() + "\n", encoding="utf-8")
        print("Commit the closing records, then run publish.")
        return 0

    def publish(self):
        """Push the closing commit to origin/main and end the phase."""
        state = self.here()
        require_clean(self.root)
        head, verified = git(self.root, "rev-parse", "HEAD"), state["verified"]
        if not verified or head == verified or not is_ancestor(self.root, verified, head):
            raise ValueError("Publish the closing commit made on the verified revision: run close, then commit.")
        outside = [path for path in git(self.root, "diff", "--name-only", verified, head).splitlines()
                   if not path.startswith(RECORDS)]
        if outside:
            raise ValueError(f"The closing commit may change only Cards and the journal: {', '.join(outside)}.")
        marker = f"candidate `{verified}`"
        for card in state["cards"]:
            _, stage, path = find_card(self.project, card)
            if stage != self.project.workflow["completed"] or marker not in path.read_text(encoding="utf-8"):
                raise ValueError(f"Close {card} before publishing.")
        if not any(f"Verified revision: `{verified}`" in day.read_text(encoding="utf-8")
                   for day in self.project.journal.glob("*.md")):
            raise ValueError("The closing commit lacks the journal milestone: run close.")
        if validate(self.project):
            raise ValueError("Fix the findings in the closing commit before publishing.")
        upstream = origin_main(self.root)
        if upstream != head:
            if not is_ancestor(self.root, upstream, head):
                raise ValueError("origin/main moved: merge it, check again and ask for a new approval.")
            git(self.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
            if origin_main(self.root) != head:
                raise ValueError("Could not confirm the publication on origin/main.")
        self.file.unlink()
        print(f"Published {head} on origin/main; the phase is over.")
        print(f"From the primary checkout: git merge --ff-only origin/main, "
              f"git worktree remove {self.root}, git branch -d {state['branch']}")
        return 0
