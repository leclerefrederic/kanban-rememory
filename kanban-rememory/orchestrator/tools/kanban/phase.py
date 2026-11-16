"""One phase at a time: a branch of the checkout that delivers Cards of one module with one approval."""

from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from .board import add_history, find_card, local, move
from .project import JOURNAL, MODULES, SETTINGS, bump, common_directory, git, load_project
from .report import report
from .validation import validate

RECORDS = (f"{MODULES.as_posix()}/", f"{JOURNAL.as_posix()}/")
NO_ACTION = {"en": "No action required.", "fr": "Aucune action requise."}


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

    @property
    def cancelled(self):
        """Terminal stages besides completion: their phase Cards are skipped at closure."""
        return self.project.frozen - {self.project.workflow["completed"]}

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
        """The active phase, provided HEAD is on its branch."""
        state = self.state()
        if state is None:
            raise ValueError("No active phase: run start CARD-ID on a dedicated branch.")
        if state["branch"] != self.branch():
            raise ValueError(f"The active phase runs on {state['branch']}: switch to it to change the records.")
        return state

    def next_action(self):
        """What the active phase waits for, or None without a phase."""
        state = self.state()
        if state is None:
            return None
        if state["branch"] != self.branch():
            return f"switch to {state['branch']}"
        if git(self.root, "status", "--porcelain", "--untracked-files=normal"):
            return "commit the changes"
        return ("ask for approval, then publish" if state["verified"] == git(self.root, "rev-parse", "HEAD")
                else "run check")

    def guard_write(self):
        """During a phase, the records change only on its branch."""
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

    def start(self, task_id, mode=None, part="patch"):
        """Open the phase with its first Card, or add the next Card, and move it to the first active stage.

        The first Card chooses where the phase works: on main, or on a release branch that is tagged when published.
        """
        module, _, _ = find_card(self.project, task_id)
        previous = self.state()
        if previous is None:
            if mode is None:
                raise ValueError("Choose where to work: --main, or --release on a dedicated branch.")
            branch = self.branch()
            if (branch == "main") != (mode == "main"):
                raise ValueError("Work on main with --main from main; start a release on a dedicated branch.")
            state = {"module": module, "cards": [task_id], "branch": branch, "mode": mode,
                     **({"bump": part} if mode == "release" else {}),
                     "started": self.project.now().isoformat(timespec="seconds"), "verified": None}
        else:
            if mode is not None:
                raise ValueError("The phase is already open: --main and --release only start a phase.")
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
        """Validate, then run each command, on the clean phase branch; record the verified revision."""
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

    def close(self, state, head, summary, approval):
        """Complete the phase Cards, write the approval on each and the journal milestone; return the closed IDs."""
        workflow = self.project.workflow
        completed = workflow["completed"]
        found = [(card, *find_card(self.project, card)[1:]) for card in state["cards"]]
        live = [(card, stage, path) for card, stage, path in found if stage not in self.cancelled]
        for card, stage, path in live:
            if stage != completed and completed not in workflow["transitions"].get(stage, []):
                raise ValueError(f"{card} cannot move from {stage} to {completed}.")
        now = self.project.now()
        paths = []
        for card, stage, path in live:
            if stage != completed:
                path = move(self.project, card, completed, lambda *_: None)
            add_history(path, f"{now.isoformat(timespec='seconds')} — Merge approved for the verified "
                              f"candidate `{head}`: “{approval}”.")
            paths.append((card, path))
        paths = paths or [(card, path) for card, _, path in found]  # every Card cancelled: link the first
        texts = [(card, path.read_text(encoding="utf-8")) for card, path in paths]
        performance = report(datetime.fromisoformat(state["started"]), now, texts, workflow["active"], completed,
                             {self.root, self.common.parent})
        journal = local(self.project.journal)
        listed = f"Phase Cards: {', '.join(state['cards'])}.\n\n" if len(state["cards"]) > 1 else ""
        link = Path(os.path.relpath(paths[0][1], journal)).as_posix()
        entry = (f"## {state['module']}/{state['cards'][0]}\n\n{summary}\n\n{listed}{performance}\n\n"
                 f"Verified revision: `{head}`. [Card](<{link}>).")
        day = journal / f"{now.date().isoformat()}.md"
        current = day.read_text(encoding="utf-8") if day.exists() else f"# {now.date()} ({workflow['timezone']})\n"
        title, _, rest = current.partition("\n")
        day.write_text(f"{title}\n\n{entry}\n\n{rest.strip()}".rstrip() + "\n", encoding="utf-8")
        return [card for card, _ in paths]

    def write_version(self, version):
        path = self.root / SETTINGS
        data = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps({**data, "version": version}, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    def publish(self, summary=None, approval=None, notify=None, language="en"):
        """Close the verified Cards, commit, push to origin/main, return to an up-to-date main and end the phase."""
        if any(text is not None and (not text.strip() or "\n" in text or "\r" in text) for text in (summary, approval)):
            raise ValueError("Give --summary and --approval as nonempty single lines.")
        from telegram import config_path
        alerting = bool(notify) or config_path().exists()  # a configured Telegram always gets the delivery alert
        if alerting and not summary:
            raise ValueError("The delivery alert needs --summary: it is the text of the alert.")
        state = self.here()
        release = state.get("mode", "release") == "release"
        require_clean(self.root)
        head, verified = git(self.root, "rev-parse", "HEAD"), state["verified"]
        if not verified or not is_ancestor(self.root, verified, head):
            raise ValueError(f"HEAD {head} is not verified: run check, then ask for approval of that revision.")
        upstream = origin_main(self.root)
        if not is_ancestor(self.root, upstream, head):
            raise ValueError("origin/main moved: merge it, check again and ask for a new approval.")
        if head == verified:
            if not summary or not approval:
                raise ValueError("Give --summary and --approval to close the verified revision.")
            closed = self.close(state, head, summary, approval)
            if release:
                self.write_version(bump(self.project.version, state.get("bump", "patch")))
            git(self.root, "add", "--all", "--", *RECORDS, SETTINGS.as_posix())
            # The closing commit keeps the authorship trailers of the verified candidate.
            trailers = git(self.root, "log", "-1", "--format=%(trailers:key=Co-Authored-By)")
            git(self.root, "commit", "--quiet", "-m",
                f"Close {', '.join(closed)} with recorded merge approval" + (f"\n\n{trailers}" if trailers else ""))
            head = git(self.root, "rev-parse", "HEAD")
        allowed = RECORDS + ((SETTINGS.as_posix(),) if release else ())
        outside = [path for path in git(self.root, "diff", "--name-only", verified, head).splitlines()
                   if not path.startswith(allowed)]
        if outside:
            raise ValueError(f"The closing commit may change only Cards and the journal: {', '.join(outside)}.")
        marker = f"candidate `{verified}`"
        for card in state["cards"]:
            _, stage, path = find_card(self.project, card)
            if stage not in self.cancelled and (stage != self.project.workflow["completed"]
                                                or marker not in path.read_text(encoding="utf-8")):
                raise ValueError(f"{card} lacks its closure: reset to the verified revision and publish again.")
        if not any(f"Verified revision: `{verified}`" in day.read_text(encoding="utf-8")
                   for day in self.project.journal.glob("*.md")):
            raise ValueError("The closing commit lacks the journal milestone.")
        if validate(self.project):
            raise ValueError("Fix the findings, amend the closing commit, then publish again.")
        tag = f"v{load_project(self.root).version}"
        if release:  # the version of the closing commit names the release
            known = subprocess.run(["git", "rev-parse", "--quiet", "--verify", f"refs/tags/{tag}^{{commit}}"], cwd=self.root,
                                   capture_output=True, text=True).stdout.strip()
            if known and known != head:
                raise ValueError(f"Tag {tag} already marks another revision: fix version in settings.json.")
        if upstream != head:
            git(self.root, "push", "--quiet", "origin", "HEAD:refs/heads/main")
            if origin_main(self.root) != head:
                raise ValueError("Could not confirm the publication on origin/main.")
        if release:
            git(self.root, "tag", "--force", tag, head)
            git(self.root, "push", "--quiet", "origin", f"refs/tags/{tag}")
        self.file.unlink()
        if state["branch"] != "main":
            git(self.root, "switch", "--quiet", "main")
            try:
                git(self.root, "merge", "--quiet", "--ff-only", head)
            except subprocess.CalledProcessError:
                raise ValueError(f"Published {head}, but main does not fast-forward to it: reconcile main, "
                                 f"then delete {state['branch']}.") from None
            git(self.root, "branch", "--quiet", "--delete", state["branch"])
        print(f"Published {head} on origin/main" + (f" as {tag}" if release else "")
              + "; main is up to date and the phase is over.")
        if alerting:
            alert = subprocess.run(
                [sys.executable, str(self.root / "kanban-rememory/orchestrator/tools/telegram.py"), "completed", "--card",
                 state["cards"][0], "--id", "delivery", "--text", summary, "--next-action", NO_ACTION[language],
                 "--chat-name", notify or self.project.name, "--language", language, "--send"],
                cwd=self.root, capture_output=True, text=True)
            print((alert.stdout + alert.stderr).strip())
        return 0
