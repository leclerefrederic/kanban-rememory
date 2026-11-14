"""Pre-push check: run the Batch publish guard when a push to main closes a Batch."""

from pathlib import Path
import re
import subprocess
import sys

ZERO = "0" * 40


def git(*args, check=True):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and result.returncode:
        raise ValueError(result.stderr.strip() or "git failed")
    return result.stdout if result.returncode == 0 else None


def statuses(sha):
    """Return {batch directory name: status} from the Batch descriptions in a commit."""
    found = {}
    for path in (git("ls-tree", "-r", "--name-only", sha, "project/batches/") or "").splitlines():
        parts = path.split("/")
        if len(parts) == 4 and parts[3] == "description.md":
            match = re.search(r"^status:\s*(\S+)", git("show", f"{sha}:{path}") or "", re.MULTILINE)
            found[parts[2]] = match.group(1) if match else None
    return found


def main():
    root = Path(git("rev-parse", "--show-toplevel").strip())
    common = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip())
    guard = Path(__file__).with_name("guard-batch-work.py")
    for line in sys.stdin.read().splitlines():
        _, local_sha, remote_ref, remote_sha = line.split()
        if remote_ref != "refs/heads/main" or local_sha == ZERO or remote_sha == ZERO:
            continue
        if git("cat-file", "-e", remote_sha, check=False) is None:
            continue  # Unknown remote commit: the remote rejects this push anyway.
        before = statuses(remote_sha)
        for batch, status in statuses(local_sha).items():
            record = common / "kanban-rememory" / batch / "guard.json"
            if status != "closed" or before.get(batch) == "closed" or not record.exists():
                continue
            result = subprocess.run([sys.executable, str(guard), "publish", str(record)],
                                    cwd=root, capture_output=True, text=True)
            if result.returncode:
                sys.exit(f"Push refused: {batch} cannot be closed. {result.stderr.strip()}")


if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        sys.exit(f"Push refused: {error}")
