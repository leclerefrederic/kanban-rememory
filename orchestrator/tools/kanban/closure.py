"""Resume an explicitly decided module Batch closure from exact Git objects."""

from contextlib import contextmanager
import json
from pathlib import Path
import re
import subprocess

from .accepted_content import StaleAcceptance, verify_accepted_content
from .coordination import exclusive, replace_json
from .files import header_value
from .specification_retirement import retire_batch_specifications, verify_retirement


FULL_REVISION = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


class Closure:
    def __init__(self, coordination, owner, delivery):
        self.coordination = coordination
        self.owner = owner
        self.delivery = delivery
        if not delivery.startswith("Batch-"):
            raise ValueError("Qualified closure recovery is for a Batch.")
        self.identity = f"{coordination.module}/{delivery}"
        self.path = coordination.directory / f"closure-{coordination.module}-{delivery.lower()}.json"
        namespace = f"{coordination.project.id}/{self.identity.lower()}"
        self.recovery = f"refs/heads/batch-recovery/{namespace}"
        self.tag = f"refs/tags/{namespace}"
        self.archive = f"refs/heads/batch-archive/{namespace}"

    @contextmanager
    def while_integrating(self):
        control = self.coordination
        with exclusive(control.directory, f"module-{control.module}"):
            control.require_owner(self.owner, self.delivery)
            with exclusive(control.directory, "integration-update"):
                integration_file = control.directory / "integration.json"
                if not integration_file.is_file():
                    raise ValueError("Acquire solution integration before closing a delivery.")
                integration = json.loads(integration_file.read_text(encoding="utf-8"))
                scope = (integration["module"], integration["owner"], integration["delivery"])
                if scope != (control.module, self.owner, self.delivery):
                    raise ValueError("Another delivery owns solution integration.")
                yield integration

    def remote_revision(self, ref):
        result = subprocess.run(
            ["git", "ls-remote", "--exit-code", "origin", ref, f"{ref}^{{}}"],
            cwd=self.coordination.root, capture_output=True, text=True,
        )
        if result.returncode == 2:
            return None
        result.check_returncode()
        entries = dict(line.split("\t", 1)[::-1] for line in result.stdout.splitlines())
        return entries.get(f"{ref}^{{}}", entries.get(ref))

    def git(self, *args):
        return self.coordination.git(*args)

    def ancestor(self, ancestor, revision):
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, revision],
            cwd=self.coordination.root,
        )
        if result.returncode != 1:
            result.check_returncode()
        return result.returncode == 0

    def full_revision(self, value):
        if not FULL_REVISION.fullmatch(value) or self.git("rev-parse", "--verify", f"{value}^{{commit}}") != value:
            raise ValueError("Supply the full, available commit ID.")
        return value

    def validate(self, record):
        closing = self.full_revision(record["closing"])
        candidate = self.full_revision(record["candidate"])
        before = self.full_revision(record["main_revision"])
        if not self.ancestor(before, closing):
            raise ValueError("Closing commit must preserve the integration base.")
        identity = self.git("show", "-s", "--format=%(trailers:key=Batch-Closure,valueonly)", closing)
        if identity != self.identity:
            raise ValueError(f"Closing commit requires Batch-Closure: {self.identity}.")
        description = self.coordination.description(self.delivery)
        path = description.relative_to(self.coordination.primary).as_posix()
        published = self.git("show", f"{closing}:{path}")
        if header_value(published, "id") != self.delivery or header_value(published, "status") != "closed":
            raise ValueError("Closing commit is missing the qualified closed Batch record.")
        verify_retirement(
            self.coordination.root, self.coordination.workspace.relative_to(self.coordination.primary),
            Path(path), published, record.get("approval"), closing,
        )
        if self.ancestor(candidate, closing) != (record["result"] == "accepted"):
            raise ValueError("Closing history must include the accepted candidate or exclude the rejected candidate.")
        # A closing commit says what was decided; the published report remains the decision source.
        report = self.git("show", f"{closing}:{Path(path).with_name('report.md').as_posix()}")
        decision = re.search(r"(?ms)^## User decision\s*\n(.*?)(?=^## |\Z)", report)
        expected = f"- Decision: {record['result']} `{candidate}`."
        lines = decision[1].splitlines() if decision else []
        if [line for line in lines if line.startswith("- Decision:")] != [expected]:
            raise ValueError("Missing exact User decision in the closing Batch report.")
        if record["result"] == "accepted":
            verify_accepted_content(self.coordination.root, candidate, closing)

    def validate_for_publication(self, record):
        try:
            self.validate(record)
        except StaleAcceptance as error:
            # The caller holds both the integration update and module locks.
            (self.coordination.directory / "integration.json").unlink()
            raise StaleAcceptance(f"{error} Integration was released. This module remains occupied.") from error

    def retire(self, integration_checkout):
        with self.while_integrating() as integration:
            control = self.coordination
            checkout = Path(integration_checkout).resolve()
            if checkout in (control.root, control.primary):
                raise ValueError("Retire Specifications in the separate integration worktree.")
            checkout_root = subprocess.check_output(
                ["git", "rev-parse", "--show-toplevel"], cwd=checkout, text=True,
            ).strip()
            if Path(checkout_root).resolve() != checkout:
                raise ValueError("Supply the integration worktree root.")
            common = control.git("rev-parse", "--path-format=absolute", "--git-common-dir")
            actual = subprocess.check_output(
                ["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                cwd=checkout, text=True,
            ).strip()
            if Path(actual).resolve() != Path(common).resolve():
                raise ValueError("Use an integration worktree of this clone.")
            head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
            if not self.ancestor(integration["main_revision"], head):
                raise ValueError("The integration worktree must preserve the recorded main revision.")
            state = control.require_owner(self.owner, self.delivery)
            description = control.description(self.delivery).relative_to(control.primary)
            return retire_batch_specifications(
                checkout, control.workspace.relative_to(control.primary), description, state.get("approval"),
            )

    def prepare(self, closing, candidate, result):
        with self.while_integrating() as integration:
            record = {
                "project": self.coordination.project.id, "delivery": self.identity,
                "owner": self.owner, "closing": closing, "candidate": candidate, "result": result,
                "main_revision": integration["main_revision"],
            }
            approval = self.coordination.require_owner(self.owner, self.delivery).get("approval")
            if approval is not None:
                record["approval"] = approval
            if integration.get("verified_revision") != closing:
                raise ValueError("Verify the exact combined closing revision before preparing publication.")
            self.validate_for_publication(record)
            if self.path.exists():
                previous = json.loads(self.path.read_text(encoding="utf-8"))
                if previous == record:
                    return record
                if previous["main_revision"] == record["main_revision"]:
                    try:
                        self.validate(previous)
                    except StaleAcceptance:
                        pass
                    else:
                        raise ValueError("An interrupted closure already records different evidence.")
                if any(self.remote_revision(ref) for ref in (self.recovery, self.tag, self.archive)):
                    raise ValueError("A prior attempt already published recovery or archive evidence. Reconcile its refs.")
                attempt = self.path.with_name(f"{self.path.stem}-previous-{previous['closing']}.json")
                replace_json(attempt, previous)
            replace_json(self.path, record)
            return record

    def publish_ref(self, revision, ref):
        existing = self.remote_revision(ref)
        if existing is None:
            # Create the ref only while it still does not exist, or reconcile on retry.
            self.git("push", f"--force-with-lease={ref}:", "origin", f"{revision}:{ref}")
        elif existing != revision:
            raise ValueError(f"Remote ref differs from the recorded closure: {ref}.")
        if self.remote_revision(ref) != revision:
            raise ValueError(f"Could not verify publication: {ref}.")

    def publish(self):
        with self.while_integrating() as integration:
            if not self.path.exists():
                raise ValueError("Prepare exact closure evidence before publication.")
            record = json.loads(self.path.read_text(encoding="utf-8"))
            self.validate_for_publication(record)
            remote_main = self.remote_revision("refs/heads/main")
            if not remote_main:
                raise ValueError("Could not verify the remote main ref.")
            closing = record["closing"]
            already_closed = self.ancestor(closing, remote_main)
            if not already_closed and remote_main != record["main_revision"]:
                raise ValueError("Remote main advanced. Preserve recovery and reconcile before publishing.")
            if not already_closed and integration.get("verified_revision") != closing:
                raise ValueError("Verify the exact combined closing revision after reacquiring integration.")
            guard = self.coordination.directory / "modules" / self.coordination.module / self.delivery.lower() / "guard.json"
            if guard.is_file():
                import sys

                script = self.coordination.root / "orchestrator/tools/guard-batch-work.py"
                subprocess.run([sys.executable, str(script), "publish", str(guard), "--revision", closing],
                               cwd=self.coordination.root, check=True)
            self.publish_ref(closing, self.recovery)
            retained = self.tag if record["result"] == "accepted" else self.archive
            self.publish_ref(record["candidate"], retained)
            if not already_closed:
                self.git("push", f"--force-with-lease=refs/heads/main:{remote_main}",
                         "origin", f"{closing}:refs/heads/main")
            published = self.remote_revision("refs/heads/main")
            if not published or not self.ancestor(closing, published):
                raise ValueError("Closure is not reachable from published main.")
            if self.ancestor(record["candidate"], published) != (record["result"] == "accepted"):
                raise ValueError("Published candidate ancestry does not match the decision.")
            return {**record, "published_main": published, "recovery_ref": self.recovery,
                    "retained_ref": retained}

    def verify_published(self, closing, remote_main):
        if not self.path.exists():
            raise ValueError("Recover the exact Batch closure record before releasing module capacity.")
        record = json.loads(self.path.read_text(encoding="utf-8"))
        self.validate(record)
        if record["closing"] != closing:
            raise ValueError("Release module capacity against the exact recorded closing commit.")
        retained = self.tag if record["result"] == "accepted" else self.archive
        if self.remote_revision(retained) != record["candidate"]:
            raise ValueError(f"The retained candidate ref is missing or differs: {retained}.")
        if self.ancestor(record["candidate"], remote_main) != (record["result"] == "accepted"):
            raise ValueError("Published candidate ancestry does not match the decision.")
