"""Copy the kit skills from orchestrator/skills/ into the discovery folders of Claude Code and Codex."""

import argparse
from hashlib import sha256
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
TARGETS = {"claude": ".claude/skills", "codex": ".agents/skills"}

# Only remove byte-identical shipped copies from before a rename or retirement. Customized or
# augmented directories may belong to the project and need a manual migration.
LEGACY_SKILLS = {
    "kanban-rememory-standalone": (None, {
        "10d63b3701dadec02c3554d7873a864f835727e31aaf912e9e22f8e0a9016da4",
        "79ce96491439cdd8e360a5a722a4f8bb766c34ab594462be18cabbf8ff294293",
        "aaa9904f3a3629eed9278331cb0aa5e68f1cf13b06ba080fd76b699e02bdec6d",
        "b191a6c2d6cac951fd68e8dff683c8abfdfd55eed2b616ff0d0a527207fe21db",
    }),
    "kanban-rememory-development-agent": ("kr-developer", {
        "57335865f11f12c6744fcaf83a47eb8217fb79237132cd41e68e5dc1a34225cb",
        "d2d8a595fecdcedb19cd8aebd9e0889dde193b887d2f70fa1921612617d9a948",
    }),
    "kanban-rememory-specification-agent": ("kr-writer", {
        "2c0d1701817b9f5babcae1ddc8f65a13d8ffa17e182709fc1bfd0c249d0f443e",
        "bbdc7ecaabe44b850ca57f9542c83ee11a1c1a99cf89f3e61cc1f07b75eaa7f1",
        "e069e7f3b06e04a7298d042f5cb9112ec5d64f2bc68721f7a0ce1b01042d6ce8",
        "ed30811379a10381f3ef2fe8a8ee2f73ed045106e6d6a18121ddf9eb0cd38032",
    }),
    "kanban-rememory-orchestrator": ("kr-orchestrator", {
        "694fd10e50d7c1af19ad332d6b7b84dd70123903222836c2f894891ce676caf5",
        "baad70b8656ec904e200e29271cb8b993341e7595f9eb6223c55d9dbb46ffb0f",
    }),
    "kanban-rememory-tester": ("kr-tester", {
        "63ee09873068f27e612dcdd9a12ab0d8678d32091db5f9dc2844ec4981fe826f",
    }),
}


# Exact kr-* copies shipped before the documentation migration (fa2f2ba).
# Keep earlier distributed digests when changing a skill, so upgrades can distinguish edits.
SHIPPED_SKILLS = {
    "kr-developer": {"d0793d674da6b9c3425cf276440a8297a0911b2309974ac4444c0a0f467c6a5c", "68e11dbf8a50dada644c60baf473fd1390193b10c39ecba601474158ac775f09", "16ba9f093446f3a74affaa1bc8f46a4619e5d85720207a8e1a6d764fb54d4364"},
    "kr-writer": {"e37407c1acad15da1e1ce94a432a4a88a846a381894165b47b1c3f06ac3aa5cc", "a74f109638e0e7bd37b087a4b7d1f2eb4eda13196d67ca92e6be404f72a6511f", "bc34cd619f7c0158729e02458ca3e4ff334b009be61089ce3f0d9693e7c33f03"},
    "kr-orchestrator": {"fc8d90535e21a1fa42e0aba93bae585f2e3c0055b0dd81d1edb7f6d8ed81cc8a", "194988ee15067b2880eb4a9708ea2bf779bf47d2ffd5ed8eeb6a5ee5c1342615", "6e7fb6466ac4e17da4bb6f55e25dd740988d9a6d53a06fee68c32bc93736b3c5"},
    "kr-tester": {"64ab5f96b5cc7524e302799d169963d74acf05c2a7eea1595c0ff1a97dccc210", "8b4b3f77c021d84a076ff00b4efbf958029b76b491ac77dd883f9e91d4812dfd", "897d12fe541bc88b79aaa04f595402ebd580530632723a490a767f949b8cd281"},
}


def local_path(path):
    if path.is_symlink():
        return False
    for parent in path.parents:
        if parent == ROOT:
            return True
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            return False
    return False


def files(folder):
    if not local_path(folder) or not folder.is_dir():
        return None
    result = {}
    for path in folder.rglob("*"):
        if path.is_symlink() or not (path.is_file() or path.is_dir()):
            return None
        result[path.relative_to(folder)] = path.read_bytes() if path.is_file() else None
    return result


def is_shipped_legacy_copy(folder, digests):
    skill = folder / "SKILL.md"
    return (
        local_path(skill) and folder.is_dir() and skill.is_file()
        and set(folder.iterdir()) == {skill}
        and sha256(skill.read_bytes()).hexdigest() in digests
    )


def kept(folder, kind):
    print(f"Kept customized {kind} skill {folder.relative_to(ROOT)}. Review it before replacing or removing.",
          file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--check", action="store_true", help="Report differences without writing.")
    args = parser.parse_args()
    source_root = ROOT / "orchestrator/skills"
    if not local_path(source_root) or not source_root.is_dir():
        sys.exit("Missing or linked orchestrator/skills/. Nothing was changed.")
    if not local_path(ROOT / "orchestrator/VERSION"):
        sys.exit("Linked orchestrator/VERSION. Nothing was changed.")
    try:
        version = (ROOT / "orchestrator/VERSION").read_text().strip()
    except OSError:
        sys.exit("orchestrator/VERSION is missing or unreadable. Nothing was changed.")
    sources = []
    legacy_sources = []
    for source in sorted(source_root.iterdir()):
        if source.name in LEGACY_SKILLS:
            legacy_sources.append(source)
            continue
        if source.is_symlink():
            sys.exit(f"Linked skill source {source.relative_to(ROOT)}. Nothing was changed.")
        if not (source / "SKILL.md").is_file():
            continue
        if files(source) is None:
            sys.exit(f"Linked or unsupported source {source.relative_to(ROOT)}. Nothing was changed.")
        sources.append(source)
    if not sources:
        sys.exit("No skill found in orchestrator/skills/. Nothing was changed.")
    source_names = {source.name for source in sources}
    copies, retire, conflicts = [], [], []
    for key, relative in TARGETS.items():
        if args.target not in (key, "both"):
            continue
        ready = set()
        for source in sources:
            destination = ROOT / relative / source.name
            if files(source) == files(destination):
                ready.add(source.name)
            elif (local_path(destination) and not destination.exists()) or is_shipped_legacy_copy(
                    destination, SHIPPED_SKILLS.get(source.name, set())):
                copies.append((source, destination))
                ready.add(source.name)
            else:
                conflicts.append(destination)
                kept(destination, "current")
        for old_name, (new_name, digests) in LEGACY_SKILLS.items():
            old = ROOT / relative / old_name
            if not local_path(old):
                kept(old, "legacy")
            elif old.exists():
                if not is_shipped_legacy_copy(old, digests):
                    kept(old, "legacy")
                elif new_name is None or new_name in ready:
                    retire.append(old)
                else:
                    print(f"Kept {old.relative_to(ROOT)} until its replacement is reconciled.", file=sys.stderr)
    for old in legacy_sources:
        new_name, digests = LEGACY_SKILLS[old.name]
        if not is_shipped_legacy_copy(old, digests):
            kept(old, "legacy source")
        elif new_name is None or new_name in source_names:
            retire.append(old)
        else:
            print(f"Kept {old.relative_to(ROOT)} until its replacement source is available.", file=sys.stderr)
    differences = [str(target.relative_to(ROOT)) for _, target in copies]
    differences += [f"{old.relative_to(ROOT)} (retire legacy copy)" for old in retire]
    differences += [f"{path.relative_to(ROOT)} (customized; review required)" for path in conflicts]
    if args.check:
        if differences:
            sys.exit("Out of date (kit " + version + "): " + ", ".join(differences))
        print(f"Skills match kit {version}.")
        return
    for source, destination in copies:
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    for old in retire:
        (old / "SKILL.md").unlink()
        old.rmdir()
    print(f"Kit {version}: updated {len(copies) + len(retire)} skill folder(s)" +
          (": " + ", ".join(differences) if differences else "."))
    if conflicts:
        sys.exit("Synchronization is incomplete: reconcile the preserved customized current skills.")


if __name__ == "__main__":
    main()
