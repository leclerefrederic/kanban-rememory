"""Durable local coordination shared by a clone's worktrees."""

from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import subprocess
import tempfile
from time import monotonic, sleep
from zoneinfo import ZoneInfo

from .batches import batch_descriptions, verify_approval
from .files import CARD_ID, cards, check_module_records, header_value
from .workflow import load_workflow
from .project import coordination_root, load_project, primary_worktree


class BusyError(ValueError):
    pass


@contextmanager
def exclusive(directory, name):
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / f"{name}.lock"
    deadline = monotonic() + 2
    while True:
        try:
            lock.mkdir()
            break
        except FileExistsError:
            if monotonic() >= deadline:
                raise BusyError(
                    f"Coordination lock is held: {lock}. Reconcile its owner before retry or recovery."
                ) from None
            sleep(0.025)
    try:
        yield
    finally:
        lock.rmdir()


def replace_text(path, value):
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=".pending-", delete=False,
    ) as stream:
        pending = Path(stream.name)
        stream.write(value)
    try:
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)



def replace_json(path, value):
    replace_text(path, json.dumps(value, indent=2) + "\n")


def add_milestone(directory, day, timezone, identity, entry):
    if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
        raise ValueError(f"Not a local journal directory: {directory}.")
    directory.mkdir(parents=True, exist_ok=True)
    marker = f"<!-- kr-event: {identity} -->"
    for file in directory.glob("????-??-??.md"):
        if file.is_symlink():
            raise ValueError(f"Not a local journal file: {file}.")
        if marker in file.read_text(encoding="utf-8").splitlines():
            return
    file = directory / f"{day}.md"
    current = file.read_text(encoding="utf-8") if file.exists() else f"# {day} ({timezone})\n"
    title, _, previous = current.partition("\n")
    replace_text(file, f"{title}\n\n{marker}\n{entry}\n\n{previous.lstrip()}")


class Coordination:
    def __init__(self, root, module):
        self.root = Path(root).resolve()
        self.primary = primary_worktree(self.root)
        self.project = load_project(self.primary)
        self.module = self.project.select_module(module)
        if self.module is None:
            raise ValueError("Module delivery coordination requires an active project.json.")
        self.directory = coordination_root(self.root) / "projects" / self.project.id
        self.module_file = self.directory / f"module-{self.module}.json"

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True).strip()

    def branch(self):
        branch = self.git("symbolic-ref", "--quiet", "--short", "HEAD")
        if self.root == self.primary or branch == "main":
            raise ValueError("Delivery operations require a dedicated worktree and branch.")
        return branch

    def status(self):
        if not self.module_file.exists():
            return None
        return json.loads(self.module_file.read_text(encoding="utf-8"))

    def require_owner(self, owner, delivery):
        state = self.status()
        if state is None or state["owner"] != owner or state["delivery"] != delivery:
            raise ValueError(f"No matching ownership for module {self.module}.")
        if state["worktree"] != str(self.root) or state["branch"] != self.branch():
            raise ValueError("Resume in the recorded delivery branch and worktree.")
        return state

    @property
    def workspace(self):
        return self.project.workspace(self.module)

    def description(self, delivery):
        matches = [path for path in batch_descriptions(self.workspace)
                   if header_value(path.read_text(encoding="utf-8"), "id") == delivery]
        if len(matches) != 1:
            raise ValueError(f"Expected one description for {self.module}/{delivery}.")
        return matches[0]

    def check_intake(self, delivery, approval):
        check_module_records(self.workspace)
        workflow = load_workflow(self.workspace)
        if any(cards(stage, self.workspace) for stage in workflow["active"]):
            raise ValueError("Reconcile active Cards before claiming a new delivery.")
        open_batches = [path for path in batch_descriptions(self.workspace)
                        if header_value(path.read_text(encoding="utf-8"), "status") != "closed"]
        if len(open_batches) > 1:
            raise ValueError("Reconcile multiple open Batches before claiming a delivery.")
        if delivery.startswith("Batch-"):
            description = self.description(delivery)
            if header_value(description.read_text(encoding="utf-8"), "status") != "ready":
                raise ValueError("Only a ready Batch can be claimed.")
            if not approval:
                raise ValueError("Supply the trusted full Batch approval commit.")
            verify_approval(delivery, approval, self.workspace, self.primary)
        else:
            if any(header_value(p.read_text(encoding="utf-8"), "status") not in {"draft", "ready"}
                   for p in open_batches):
                raise ValueError("Reconcile the active Batch before claiming a Card.")
            intake = workflow.get("intake", workflow["stages"][0])
            matches = [path for path in cards(intake, self.workspace)
                       if CARD_ID.match(path.stem)[1].upper() == delivery]
            if len(matches) != 1 or header_value(matches[0].read_text(encoding="utf-8"), "batch"):
                raise ValueError("Claim a standalone Card in intake or its approved Batch.")

    def claim(self, owner, delivery, base, approval=None):
        branch = self.branch()
        base_revision = self.git("rev-parse", "--verify", f"{base}^{{commit}}")
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", base_revision, "HEAD"],
            cwd=self.root, check=True,
        )
        with exclusive(self.directory, "pickup"), exclusive(self.directory, f"module-{self.module}"):
            current = self.status()
            if current:
                self.require_owner(owner, delivery)
                if current["base_revision"] != base_revision:
                    raise ValueError("Resume with the recorded base revision.")
                return current
            for path in self.directory.glob("module-*.json"):
                other = json.loads(path.read_text(encoding="utf-8"))
                if str(self.root) == other["worktree"] or branch == other["branch"]:
                    raise ValueError("Use a separate branch and worktree for each active delivery.")
            self.check_intake(delivery, approval)
            state = {
                "project": self.project.id,
                "module": self.module,
                "delivery": delivery,
                "owner": owner,
                "branch": branch,
                "worktree": str(self.root),
                "base_revision": base_revision,
                "checkpoint": "picked up",
            }
            replace_json(self.module_file, state)
            return state

    def checkpoint(self, owner, delivery, checkpoint):
        with exclusive(self.directory, f"module-{self.module}"):
            state = self.require_owner(owner, delivery)
            state["checkpoint"] = checkpoint
            replace_json(self.module_file, state)
            return state

    def integration(self, action, owner, delivery):
        with exclusive(self.directory, f"module-{self.module}"):
            self.require_owner(owner, delivery)
            with exclusive(self.directory, "integration-update"):
                return self.update_integration(action, owner, delivery)

    def update_integration(self, action, owner, delivery):
        path = self.directory / "integration.json"
        current = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
        identity = {"module": self.module, "owner": owner, "delivery": delivery,
                    "worktree": str(self.root)}
        if current and any(current.get(field) != value for field, value in identity.items()):
            raise BusyError(f"Integration is held by {current['module']}/{current['delivery']}.")
        if action == "release":
            if current:
                path.unlink()
            return None
        actual_main = self.git("rev-parse", "--verify", "refs/heads/main")
        if current:
            if current["main_revision"] != actual_main:
                raise ValueError("Main advanced; record evidence, release integration and reverify on the new main.")
            return current
        if action != "begin":
            raise ValueError("Begin integration before verifying it.")
        state = {**identity, "main_revision": actual_main}
        replace_json(path, state)
        return state

    def finish(self, owner, delivery, revision):
        with exclusive(self.directory, f"module-{self.module}"):
            self.require_owner(owner, delivery)
            with exclusive(self.directory, "integration-update"):
                integration = self.directory / "integration.json"
                if integration.exists() and json.loads(integration.read_text())["module"] == self.module:
                    raise ValueError("Release integration ownership after verified publication.")
                if self.git("rev-parse", "--verify", f"{revision}^{{commit}}") != revision:
                    raise ValueError("Supply the full verified closing revision.")
                output = self.git("ls-remote", "--exit-code", "origin", "refs/heads/main").split()
                if len(output) != 2 or output[1] != "refs/heads/main":
                    raise ValueError("Could not verify the published main revision.")
                subprocess.run(
                    ["git", "merge-base", "--is-ancestor", revision, output[0]],
                    cwd=self.root, check=True,
                )
                self.check_closure(delivery, revision)
                self.module_file.unlink()

    def check_closure(self, delivery, revision):
        from .files import acceptance_checks

        check_module_records(self.workspace)
        if delivery.startswith("Batch-"):
            description = self.description(delivery)
            relative = description.relative_to(self.primary)
            published = self.git("show", f"{revision}:{relative}")
            if header_value(published, "status") != "closed":
                raise ValueError("Published Batch record must be closed.")
            if header_value(published, "id") != delivery:
                raise ValueError("Published closure belongs to another Batch.")
        else:
            completed = load_workflow(self.workspace)["completed"]
            matches = [path for path in cards(completed, self.workspace)
                       if CARD_ID.match(path.stem)[1].upper() == delivery]
            if len(matches) != 1:
                raise ValueError("Complete the matching Card before releasing capacity.")
            relative = matches[0].relative_to(self.primary)
            published = self.git("show", f"{revision}:{relative}")
            checks = list(acceptance_checks(published))
            if not checks or any("[ ]" in check for check in checks):
                raise ValueError("Published Card closure is missing verified criteria.")

    def milestone(self, owner, delivery, event, summary, revision, evidence, shared=False):
        if not summary.strip() or "\n" in summary or "\r" in summary:
            raise ValueError("Supply a short single-line milestone.")
        check_module_records(self.workspace)
        target = (self.primary / evidence).resolve()
        if not target.is_relative_to(self.workspace) or not target.is_file():
            raise ValueError("Link a local evidence file within this module.")
        if self.git("rev-parse", "--verify", f"{revision}^{{commit}}") != revision:
            raise ValueError("Supply the full milestone commit.")
        timezone = load_workflow(self.workspace)["timezone"]
        day = datetime.now(ZoneInfo(timezone)).date()
        event_identity = f"{self.project.id}/{self.module}/{delivery}/{event}"
        reference = f"{self.module}/{delivery}"
        with exclusive(self.directory, f"module-{self.module}"):
            self.require_owner(owner, delivery)
            with exclusive(self.directory, "journal-update"):
                local = self.workspace / "rememory"
                for directory in (local, self.project.memory) if shared else (local,):
                    relative = Path(os.path.relpath(target, directory)).as_posix()
                    entry = (f"## {reference}\n\n{summary}\n\n"
                             f"Revision: `{revision}`. [Local evidence](<{relative}>).")
                    add_milestone(directory, day, timezone, event_identity, entry)
