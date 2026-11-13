"""Check scope, acceptance artifact integrity, and publication evidence."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def revision(ref):
    return subprocess.check_output(
        ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"], text=True
    ).strip()


def artifact_digest(path):
    digest = hashlib.sha256()
    entries = sorted(path.rglob("*")) if path.is_dir() else [path]
    for entry in entries:
        if entry.is_symlink():
            raise ValueError("Acceptance artifacts must not contain symbolic links.")
        if entry.is_file():
            digest.update(str(entry.relative_to(path.parent)).encode() + b"\0")
            with entry.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["change", "freeze", "verify", "publish"])
    parser.add_argument("record", type=Path)
    parser.add_argument("--card")
    parser.add_argument("--artifact", type=Path)
    parser.add_argument("--restart", action="store_true")
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text())
        current = revision("HEAD")
        frozen = record.get("acceptance")
        if args.operation == "change":
            if not re.fullmatch(r"[A-Z][A-Z0-9]*-[0-9]{8}", args.card or ""):
                raise ValueError("An active Card ID is required.")
            active = Path("project/kanban/development").glob(args.card.lower() + "*.md")
            if args.card not in record["authorized_cards"] or not any(active):
                raise ValueError("Record out-of-scope work in Backlog and defer it.")
            if frozen:
                raise ValueError("Acceptance is active. Preserve the recorded build.")
        elif args.operation == "freeze":
            if frozen and not args.restart:
                raise ValueError("Explicitly restart affected tests before replacing the acceptance baseline.")
            path = args.artifact
            if path is None or not path.exists():
                raise ValueError("An existing acceptance artifact is required.")
            record["acceptance"] = {"revision": current, "path": str(path.resolve()),
                                    "sha256": artifact_digest(path.resolve())}
            record.pop("decision", None)
            args.record.write_text(json.dumps(record, indent=2) + "\n")
        else:
            if not frozen or not Path(frozen["path"]).exists():
                raise ValueError("The acceptance artifact is missing.")
            if artifact_digest(Path(frozen["path"])) != frozen["sha256"]:
                raise ValueError("The acceptance artifact changed.")
            if args.operation == "publish":
                checks = record.get("verification", {})
                if checks.get("revision") != frozen["revision"] or checks.get("technical_checks") != "passed":
                    raise ValueError("Record passing technical checks for the acceptance revision.")
                changed = subprocess.check_output(
                    ["git", "diff", "--name-only", revision(record["base_revision"]), frozen["revision"]],
                    text=True,
                ).splitlines()
                if any(Path(path).name == "build-app.sh" for path in changed) and checks.get("full_build") != "passed":
                    raise ValueError("Build-script changes require a successful full build.")
                if record.get("decision") != {"revision": frozen["revision"], "result": "accepted"}:
                    raise ValueError("Record the User's acceptance of the exact revision.")
                subprocess.run(["git", "merge-base", "--is-ancestor", frozen["revision"], current], check=True)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    print("Batch guard passed.")


if __name__ == "__main__":
    main()
