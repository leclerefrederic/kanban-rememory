"""Run a check with its own temporary files and artifact directory."""

import os
from pathlib import Path
import subprocess
import tempfile

from .project import coordination_root


def run_check(coordination, owner, delivery, command, integration_checkout=None):
    state = coordination.require_owner(owner, delivery)
    if not command:
        raise ValueError("Supply the check command after --.")
    checkout = coordination.root
    check_token = candidate = None
    if integration_checkout is not None:
        checkout = Path(integration_checkout).resolve()
        if coordination_root(checkout) != coordination_root(coordination.root):
            raise ValueError("Integration checks require a worktree of this clone.")
        state = coordination.integration_check(owner, delivery)
        integration_base = state["main_revision"]
        check_token = state["check_token"]
        candidate = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip()
        subprocess.run(["git", "merge-base", "--is-ancestor", integration_base, candidate],
                       cwd=checkout, check=True)
        require_clean(checkout)
    base = coordination.directory / "runtime" / state["module"] / delivery.lower()
    base.mkdir(parents=True, exist_ok=True)
    runtime = Path(tempfile.mkdtemp(prefix="check-", dir=base))
    for name in ("tmp", "artifacts"):
        (runtime / name).mkdir()
    environment = os.environ.copy()
    for name in ("TMPDIR", "TEMP", "TMP"):
        environment[name] = str(runtime / "tmp")
    environment.update(KR_MODULE=state["module"], KR_RUNTIME_DIR=str(runtime),
                       KR_ARTIFACT_DIR=str(runtime / "artifacts"))
    print(f"Runtime directory: {runtime}", flush=True)
    result = subprocess.call(command, cwd=checkout, env=environment)
    if candidate is not None and result == 0:
        require_clean(checkout)
        if candidate != subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=checkout, text=True).strip():
            raise ValueError("The checkout changed during verification.")
        coordination.integration_check(owner, delivery, candidate, check_token)
    return result


def require_clean(checkout):
    changes = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=checkout)
    if changes:
        raise ValueError("Verify the exact integration revision in a clean checkout.")
