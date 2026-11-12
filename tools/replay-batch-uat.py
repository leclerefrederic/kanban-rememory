"""Create a disposable Git repository with delivered and closed delivery batch snapshots."""

import argparse
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="New directory for the fixture")
    root = parser.parse_args().directory.resolve()
    root.mkdir()

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

    git("init", "-q", "-b", "main")
    git("config", "user.name", "Batch acceptance fixture")
    git("config", "user.email", "fixture@example.invalid")
    git("commit", "--allow-empty", "-qm", "Baseline")
    git("switch", "-qc", "delivery")
    (root / "product.txt").write_text("Tested change\n", encoding="utf-8")
    git("add", "product.txt")
    git("commit", "-qm", "Implement sample change")
    tested = git("rev-parse", "HEAD")
    git("switch", "-q", "main")
    lot = root / "batches/Batch-001"
    lot.mkdir(parents=True)
    fiche = root / "specs/frozen/SPEC-001-r1.md"
    fiche.parent.mkdir(parents=True)
    fiche.write_text('---\ntype: specification\nid: "SPEC-001"\nrevision: "1"\n---\n', encoding="utf-8")

    def record(name, body):
        (lot / name).write_text(body, encoding="utf-8")

    def description(status):
        record("Description.md", f'---\ntype: batch\nid: "Batch-001"\nstatus: {status}\n'
               'specifications: [{"id":"SPEC-001","revision":"1",'
               '"path":"specs/frozen/SPEC-001-r1.md"}]\n---\n')

    def report(decision, evidence=""):
        record("Report.md", '---\ntype: report\nid: "Batch-001-Report"\nbatch: "Batch-001"\n'
               f'---\n\nUser decision: {decision}.\n{evidence}')

    description("delivered")
    report("pending")
    record("Tests.md", '---\ntype: tests\nid: "Batch-001-Tests"\nbatch: "Batch-001"\n'
           f'---\n\nTested commit: `{tested}`\n\nAcceptance result: OK.\n')
    git("add", "batches", "specs")
    git("commit", "-qm", "Record delivered fixture")
    git("branch", "uat-delivered")
    git("merge", "--no-ff", "-qm", "Merge accepted fixture", "delivery")
    git("tag", "batch-001", tested)
    description("closed")
    report("accepted", "\nClosing trailer: Batch-Closure: Batch-001\nDelivery tag: refs/tags/batch-001\n")
    git("add", "batches")
    git("commit", "-qm", "Close fixture", "-m", "Batch-Closure: Batch-001")
    print(f"Fixture: {root}\nDelivered snapshot: uat-delivered\nClosed snapshot: main")
    print(f"Tested commit: {tested}\nClosing commit: {git('rev-parse', 'HEAD')}")


if __name__ == "__main__":
    main()
