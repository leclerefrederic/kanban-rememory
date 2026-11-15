"""Copy the kit skills from agents/skills/ into the discovery folders of Claude Code and Codex."""

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


def files(folder):
    return {path.relative_to(folder): path.read_bytes() for path in folder.rglob("*") if path.is_file()}


def is_shipped_legacy_copy(folder, digests):
    skill = folder / "SKILL.md"
    return (
        not folder.is_symlink() and folder.is_dir()
        and not skill.is_symlink() and skill.is_file()
        and set(folder.iterdir()) == {skill}
        and sha256(skill.read_bytes()).hexdigest() in digests
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["claude", "codex", "both"], default="both")
    parser.add_argument("--check", action="store_true", help="Report differences without writing.")
    args = parser.parse_args()
    sources = []
    for source in sorted((ROOT / "agents/skills").iterdir()):
        if not (source / "SKILL.md").is_file():
            continue
        migration = LEGACY_SKILLS.get(source.name)
        if migration is not None and migration[0] is None and is_shipped_legacy_copy(source, migration[1]):
            continue  # A file-copy upgrade may leave a bundled retired source behind.
        sources.append(source)
    if not sources:
        sys.exit("No skill found in agents/skills/.")
    differences = []
    source_names = {source.name for source in sources}
    for key, relative in TARGETS.items():
        if args.target not in (key, "both"):
            continue
        for source in sources:
            destination = ROOT / relative / source.name
            if not destination.is_dir() or files(source) != files(destination):
                differences.append(f"{relative}/{source.name}")
                if not args.check:
                    shutil.rmtree(destination, ignore_errors=True)
                    shutil.copytree(source, destination)
        for old_name, (new_name, digests) in LEGACY_SKILLS.items():
            if new_name is not None and new_name not in source_names:
                continue
            old = ROOT / relative / old_name
            if not old.exists() and not old.is_symlink():
                continue
            if not is_shipped_legacy_copy(old, digests):
                print(f"Kept customized legacy skill {old.relative_to(ROOT)}. Review it before removing.",
                      file=sys.stderr)
                continue
            differences.append(f"{old.relative_to(ROOT)} (retire legacy copy)")
            if not args.check:
                (old / "SKILL.md").unlink()
                old.rmdir()
    version = (ROOT / "agents/VERSION").read_text().strip()
    if args.check:
        if differences:
            sys.exit("Out of date (kit " + version + "): " + ", ".join(differences))
        print(f"Skills match kit {version}.")
    else:
        print(f"Kit {version}: updated {len(differences)} skill folder(s)" + (": " + ", ".join(differences) if differences else "."))


if __name__ == "__main__":
    main()
