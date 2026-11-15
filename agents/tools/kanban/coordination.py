"""Durable local coordination shared by a clone's worktrees."""

from contextlib import contextmanager
from datetime import datetime
from errno import EACCES, EAGAIN, EDEADLK
import json
import os
from pathlib import Path
import subprocess
import tempfile
from time import monotonic, sleep
from uuid import uuid4
from zoneinfo import ZoneInfo

from .batches import batch_descriptions, verify_approval
from .files import CARD_ID, cards, check_module_records, header_value
from .workflow import load_workflow
from .project import PROJECT_SCOPE, coordination_root, load_project, primary_worktree


class BusyError(ValueError):
    pass


@contextmanager
def exclusive(directory, name):
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / f"{name}.lock"
    if lock.is_symlink():
        raise ValueError(f"Coordination lock must be local: {lock}.")
    deadline = monotonic() + 2
    with lock.open("a+b") as handle:
        while True:
            try:
                take_lock(handle)
                break
            except OSError as error:
                if error.errno not in {EACCES, EAGAIN, EDEADLK}:
                    raise
                if monotonic() >= deadline:
                    raise BusyError(f"Coordination lock is held: {lock}.") from error
                sleep(0.025)
        # Closing the descriptor releases the lock even if its process stops.
        yield


def take_lock(handle):
    if os.name == "nt":
        import msvcrt

        handle.seek(0)
        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
    else:
        import fcntl

        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)


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


def recorded_milestone(directory, identity):
    marker = f"<!-- kr-event: {identity} -->"
    for file in directory.glob("????-??-??.md"):
        if file.is_symlink():
            raise ValueError(f"Not a local journal file: {file}.")
        if marker in file.read_text(encoding="utf-8").splitlines():
            return True
    return False


def add_milestone(directory, day, timezone, identity, entry):
    if directory.is_symlink() or (directory.exists() and not directory.is_dir()):
        raise ValueError(f"Not a local journal directory: {directory}.")
    directory.mkdir(parents=True, exist_ok=True)
    if recorded_milestone(directory, identity):
        return
    marker = f"<!-- kr-event: {identity} -->"
    file = directory / f"{day}.md"
    current = file.read_text(encoding="utf-8") if file.exists() else f"# {day} ({timezone})\n"
    title, _, previous = current.partition("\n")
    replace_text(file, f"{title}\n\n{marker}\n{entry}\n\n{previous.lstrip()}")


class Coordination:
    def __init__(self, root, module):
        self.root = Path(root).resolve()
        self.primary = primary_worktree(self.root)
        self.project = load_project(self.primary)
        if not self.project.modules:
            raise ValueError("Module delivery coordination requires an active project.json.")
        self.module = (self.project.validate_scope(module) if module is not None
                       else self.project.select_module())
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
        return self.project.scope_workspace(self.module)

    def description(self, delivery):
        if self.module == PROJECT_SCOPE:
            raise ValueError("Batches in a module-aware project require a module scope.")
        matches = [path for path in batch_descriptions(self.workspace)
                   if header_value(path.read_text(encoding="utf-8"), "id") == delivery]
        if len(matches) != 1:
            raise ValueError(f"Expected one description for {self.module}/{delivery}.")
        return matches[0]

    def check_intake(self, delivery, approval):
        check_module_records(self.workspace)
        check_module_records(self.project.board)
        self.project.check_legacy_boards()
        workflow = load_workflow(self.project.board)
        if any(self.scope_cards(stage) for stage in workflow["active"]):
            raise ValueError("Reconcile active Cards before claiming a new delivery.")
        open_batches = [path for path in batch_descriptions(self.workspace)
                        if header_value(path.read_text(encoding="utf-8"), "status") != "closed"]
        if self.module == PROJECT_SCOPE:
            open_batches = []
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
            matches = [path for stage in workflow["stages"] for path in cards(stage, self.project.board)
                       if CARD_ID.match(path.stem)[1].upper() == delivery]
            if (len(matches) != 1 or matches[0].parent.name != intake
                    or self.project.card_scope(matches[0]) != self.module
                    or header_value(matches[0].read_text(encoding="utf-8"), "batch")):
                raise ValueError("Claim a standalone Card in intake or its approved Batch.")

    def scope_cards(self, stage):
        workflow = load_workflow(self.project.board)
        archived = stage in {workflow["completed"], "cancellation"}
        return [path for path in cards(stage, self.project.board)
                if self.project.card_scope(path, allow_legacy=archived) == self.module]

    def claim(self, owner, delivery, base, approval=None):
        branch = self.branch()
        base_revision = self.git("rev-parse", "--verify", f"{base}^{{commit}}")
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", base_revision, "HEAD"],
            cwd=self.root, check=True,
        )
        with (exclusive(self.directory, "pickup"),
              exclusive(self.directory, f"module-{self.module}"),
              exclusive(self.directory, "board-write")):
            current = self.status()
            if current:
                self.require_owner(owner, delivery)
                if current["base_revision"] != base_revision:
                    raise ValueError("Resume with the recorded base revision.")
                if approval is not None and current.get("approval") != approval:
                    raise ValueError("Resume with the recorded Batch approval commit.")
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
            if approval is not None:
                state["approval"] = approval
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

    def integration_check(self, owner, delivery, revision=None, token=None):
        with exclusive(self.directory, f"module-{self.module}"):
            self.require_owner(owner, delivery)
            with exclusive(self.directory, "integration-update"):
                state = self.update_integration("verify", owner, delivery)
                if token is None:
                    state.pop("verified_revision", None)
                    state["check_token"] = uuid4().hex
                else:
                    if state.pop("check_token", None) != token:
                        raise ValueError("Integration changed while verification was running.")
                    state["verified_revision"] = revision
                replace_json(self.directory / "integration.json", state)
                return state

    def publish_card(self, owner, delivery, closing):
        if not delivery.startswith("CARD-"):
            raise ValueError("Use qualified Batch closure for a Batch.")
        with exclusive(self.directory, f"module-{self.module}"):
            claim = self.require_owner(owner, delivery)
            with exclusive(self.directory, "integration-update"):
                state = self.update_integration("verify", owner, delivery)
                if state.get("verified_revision") != closing:
                    raise ValueError("Verify the exact combined Card closing revision.")
                self.check_closure(delivery, closing)
                remote_main = self.remote_main()
                previous = claim.get("closing_revision")
                if previous and previous != closing and self.is_ancestor(previous, remote_main):
                    raise ValueError("The Card was already published at a different closing revision.")
                if self.is_ancestor(closing, remote_main):
                    self.require_card_publication(claim, delivery, closing)
                    return remote_main
                if remote_main != state["main_revision"]:
                    raise ValueError("Remote main advanced. Reconcile and verify again before publishing.")
                if not self.is_ancestor(remote_main, closing) or not self.is_ancestor(self.git("rev-parse", "HEAD"), closing):
                    raise ValueError("Closing revision must preserve main and the delivery branch.")
                claim["closing_revision"] = closing
                replace_json(self.module_file, claim)
                self.git("push", f"--force-with-lease=refs/heads/main:{remote_main}", "origin",
                         f"{closing}:refs/heads/main")
                published = self.remote_main()
                if not self.is_ancestor(closing, published):
                    raise ValueError("Card closure is not reachable from published main.")
                return published

    def remote_main(self):
        output = self.git("ls-remote", "--exit-code", "origin", "refs/heads/main").split()
        if len(output) != 2 or output[1] != "refs/heads/main":
            raise ValueError("Could not verify the published main revision.")
        return output[0]

    def is_ancestor(self, ancestor, revision):
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, revision],
            cwd=self.root,
        )
        if result.returncode != 1:
            result.check_returncode()
        return result.returncode == 0

    def finish(self, owner, delivery, revision):
        with exclusive(self.directory, f"module-{self.module}"):
            claim = self.require_owner(owner, delivery)
            with exclusive(self.directory, "integration-update"):
                integration = self.directory / "integration.json"
                if integration.exists() and json.loads(integration.read_text())["module"] == self.module:
                    raise ValueError("Release integration ownership after verified publication.")
                if self.git("rev-parse", "--verify", f"{revision}^{{commit}}") != revision:
                    raise ValueError("Supply the full verified closing revision.")
                published = self.remote_main()
                if not self.is_ancestor(revision, published):
                    raise ValueError("The exact closing revision is not on published main.")
                self.require_card_publication(claim, delivery, revision)
                self.check_closure(delivery, revision)
                if delivery.startswith("Batch-"):
                    from .closure import Closure

                    Closure(self, owner, delivery).verify_published(revision, published)
                if not recorded_milestone(self.project.memory, self.publication_identity(delivery, revision)):
                    raise ValueError("Record the verified project publication milestone before releasing capacity.")
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
            completed = load_workflow(self.project.board)["completed"]
            matches = [path for path in self.scope_cards(completed)
                       if CARD_ID.match(path.stem)[1].upper() == delivery]
            if len(matches) != 1:
                raise ValueError("Complete the matching Card before releasing capacity.")
            relative = matches[0].relative_to(self.primary)
            published = self.git("show", f"{revision}:{relative}")
            if header_value(published, "scope") != self.module or header_value(published, "id") != delivery:
                raise ValueError("Published Card closure belongs to another scope or Card.")
            checks = list(acceptance_checks(published))
            if not checks or any("[ ]" in check for check in checks):
                raise ValueError("Published Card closure is missing verified criteria.")
        return self.primary / relative

    def publication_identity(self, delivery, revision):
        return f"{self.project.id}/{self.module}/{delivery}/published/{revision}"

    def require_card_publication(self, claim, delivery, revision):
        if delivery.startswith("CARD-") and claim.get("closing_revision") != revision:
            raise ValueError("Use the Card's recorded publication revision.")

    def milestone(self, owner, delivery, event, summary, revision, evidence=None, published=False):
        if not summary.strip() or "\n" in summary or "\r" in summary:
            raise ValueError("Supply a short single-line milestone.")
        check_module_records(self.workspace)
        if self.git("rev-parse", "--verify", f"{revision}^{{commit}}") != revision:
            raise ValueError("Supply the full milestone commit.")
        timezone = load_workflow(self.project.board)["timezone"]
        day = datetime.now(ZoneInfo(timezone)).date()
        event_identity = f"{self.project.id}/{self.module}/{delivery}/{event}"
        reference = f"{self.module}/{delivery}"
        with exclusive(self.directory, f"module-{self.module}"):
            claim = self.require_owner(owner, delivery)
            if published:
                remote_main = self.remote_main()
                if not self.is_ancestor(revision, remote_main):
                    raise ValueError("The milestone revision is not on published main.")
                self.require_card_publication(claim, delivery, revision)
                target = self.check_closure(delivery, revision)
                if delivery.startswith("Batch-"):
                    from .closure import Closure

                    Closure(self, owner, delivery).verify_published(revision, remote_main)
                event_identity = self.publication_identity(delivery, revision)
                directory = self.project.memory
            else:
                if not evidence:
                    raise ValueError("Link to existing evidence for a work note.")
                target = (self.primary / evidence).resolve()
                in_board = target.is_relative_to(self.project.board / "kanban")
                same_scope = (in_board and target.is_file()
                              and self.project.card_scope(target, allow_legacy=True) == self.module)
                if not target.is_file() or (not same_scope and
                        (in_board or not target.is_relative_to(self.workspace))):
                    raise ValueError("Link a local evidence file within the current scope.")
                directory = self.project.scope_memory(self.module)
            with exclusive(self.directory, "journal-update"):
                relative = Path(os.path.relpath(target, directory)).as_posix()
                verb = "Published revision" if published else "Revision"
                entry = (f"## {reference}\n\n{summary}\n\n"
                         f"{verb}: `{revision}`. [Reference record](<{relative}>).")
                add_milestone(directory, day, timezone, event_identity, entry)
