"""Create a disposable Git repository with delivered and closed Lot snapshots."""

import argparse
from hashlib import sha256
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
    git("config", "user.name", "Lot acceptance fixture")
    git("config", "user.email", "fixture@example.invalid")
    git("commit", "--allow-empty", "-qm", "Baseline")
    git("switch", "-qc", "delivery")
    (root / "product.txt").write_text("Tested change\n", encoding="utf-8")
    git("add", "product.txt")
    git("commit", "-qm", "Implement sample change")
    tested = git("rev-parse", "HEAD")
    git("switch", "-q", "main")
    lot = root / "Lots/Lot-001"
    lot.mkdir(parents=True)
    fiche = root / "specs/frozen/FICHE-001-r1.md"
    fiche.parent.mkdir(parents=True)
    fiche.write_text('---\ntype: fiche\nid: "FICHE-001"\nrevision: "1"\n---\n', encoding="utf-8")
    digest = sha256(fiche.read_bytes()).hexdigest()

    def record(name, body):
        (lot / name).write_text(body, encoding="utf-8")

    def description(status):
        record("Description.md", f'---\ntype: lot\nid: "Lot-001"\nstatus: {status}\n'
               'fiches: [{"id":"FICHE-001","revision":"1",'
               f'"path":"specs/frozen/FICHE-001-r1.md","sha256":"{digest}"}}]\n---\n')

    def report(decision, evidence=""):
        record("Report.md", '---\ntype: report\nid: "Lot-001-Report"\nlot: "Lot-001"\n'
               f'---\n\nUser decision: {decision}.\n{evidence}')

    description("delivered")
    report("pending")
    record("Tests.md", '---\ntype: tests\nid: "Lot-001-Tests"\nlot: "Lot-001"\n'
           f'---\n\nTested commit: `{tested}`\n\nAcceptance result: OK.\n')
    git("add", "Lots", "specs")
    git("commit", "-qm", "Record delivered fixture")
    git("branch", "uat-delivered")
    git("merge", "--no-ff", "-qm", "Merge accepted fixture", "delivery")
    git("tag", "lot-001", tested)
    description("closed")
    report("accepted", "\nClosing trailer: Lot-Closure: Lot-001\nDelivery tag: refs/tags/lot-001\n")
    git("add", "Lots")
    git("commit", "-qm", "Close fixture", "-m", "Lot-Closure: Lot-001")
    print(f"Fixture: {root}\nDelivered snapshot: uat-delivered\nClosed snapshot: main")
    print(f"Tested commit: {tested}\nClosing commit: {git('rev-parse', 'HEAD')}")


if __name__ == "__main__":
    main()
