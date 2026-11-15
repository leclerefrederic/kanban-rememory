"""Delivery batch references and approval checks."""

from hashlib import sha256
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

from .files import CARD_ID, PROJECT, ROOT, field, header_value, markdown_lines, resource_links
from .specifications import SPECIFICATION_NAMES, specification_root


def relationship(source, key):
    missing = object()
    value = header_value(source, key, missing)
    if value is not missing:
        return value
    aliases = {"batch": ("lot", "lot_id"), "specifications": ("fiches", "fiche_ids")}
    for legacy in aliases.get(key, (f"{key}_id",)):
        value = header_value(source, legacy, missing)
        if value is not missing:
            return value
    return None


def fiche_entries(source):
    if header_value(source, "type") in ("batch", "lot"):
        entries = relationship(source, "specifications")
        if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
            raise ValueError("Batch front matter requires a specifications list of mappings.")
        for entry in entries:
            yield [entry.get(key) for key in ("id", "revision", "path", "sha256")]
        return
    for line in markdown_lines(source):
        if line.startswith("- Fiche:"):
            yield [part.strip() for part in line.partition(":")[2].split("|")]


def project_reference(path, project=PROJECT, root=ROOT):
    relative = Path(path)
    specifications = specification_root(project)
    if project != root / "project":
        root_relative = (root / relative).resolve()
        if not root_relative.is_relative_to(specifications):
            raise ValueError("A Batch must pin a repository-relative Specification path in its own module.")
        if relative.is_absolute() or ".." in relative.parts or root / relative != root_relative:
            raise ValueError("A Batch Specification path must be local and cannot contain aliases.")
        return root_relative
    if relative.parts and relative.parts[0] in SPECIFICATION_NAMES:
        relative = Path("project") / path.lower()
    if relative.parts[:3] == ("project", "specs", "frozen"):
        migrated = specifications / "approved" / relative.name
        if relative.name == "fiche-001-r1.md" and not migrated.is_file():
            migrated = migrated.with_name("spec-001-r1.md")
        if migrated.is_file():
            return migrated
    return root / relative


def retired_pin(reference, revision, status):
    """Resolve a closed, unnumbered Batch pin without editing its recorded path."""
    if revision is None and status == "closed" and reference.parent.name == "approved":
        return reference.parent.parent / "retired" / reference.name
    return reference


def batch_slug(identifier):
    return re.sub(r"^lot-", "batch-", identifier.lower())


def batch_descriptions(project=PROJECT):
    for directory in project.iterdir() if project.exists() else ():
        if directory.name in ("batches", "lots", "Lots") and directory.is_dir():
            yield from sorted(p for p in directory.glob("*/*.md") if p.name.lower() == "description.md")


def validate_lot_mapping(card_paths, project=PROJECT, root=ROOT, *, standalone=False):
    findings = []

    def report(path, message):
        findings.append(f"{path.relative_to(root)}: {message}")

    fiches = set()
    approved = {}
    eligible = {}
    retired = {}
    seen_ids = {}
    try:
        specifications = specification_root(project)
    except ValueError as error:
        return [str(error)]
    for state in ("ready", "approved", "frozen", "retired"):
        for path in (specifications / state).glob("*.md"):
            content = path.read_bytes()
            source = content.decode("utf-8")
            fiche_id = header_value(source, "id") or field(source, "Fiche ID")
            revision = header_value(source, "revision") or field(source, "Revision") or None
            revision = str(revision) if revision is not None else None
            if not isinstance(fiche_id, str) or not fiche_id:
                continue
            fiches.add(fiche_id)
            record = (fiche_id, revision, sha256(content).hexdigest())
            relative = path.relative_to(root).as_posix()
            if state == "retired":
                retired[relative] = record
            else:
                eligible[relative] = record
            if fiche_id in seen_ids and (revision is None or seen_ids[fiche_id] is None):
                report(path, f"Duplicate Specification ID: {fiche_id}")
            seen_ids[fiche_id] = revision
            if revision is None and (
                header_value(source, "type") != "specification"
                or not re.fullmatch(r"SPEC-[0-9]{3,}", fiche_id)
                or path.name != f"{fiche_id.lower()}.md"
            ):
                report(path, "Unnumbered Specification filename must match its stable SPEC ID.")
            if state in ("approved", "frozen"):
                approved[relative] = record

    lots = {}
    owners = {}
    for path in batch_descriptions(project):
        lot_id = header_value(path.read_text(encoding="utf-8"), "id") or header_value(path.read_text(encoding="utf-8"), "lot") or path.parent.name
        if not isinstance(lot_id, str) or batch_slug(lot_id) != path.parent.name.lower() and lot_id.lower() != path.parent.name.lower():
            report(path, "Batch ID must match the directory name.")
            continue
        selected = set()
        if lot_id in lots:
            report(path, f"Duplicate batch ID: {lot_id}")
        lots[lot_id] = selected
        source = path.read_text(encoding="utf-8")
        status = header_value(source, "status")
        draft = header_value(source, "type") == "batch" and status == "draft"
        if header_value(source, "type") in ("batch", "lot"):
            if status not in ("draft", "ready", "in-progress", "delivered", "validated", "rejected", "closed"):
                report(path, "Unknown Batch status.")
            if header_value(source, "id") != lot_id:
                report(path, "Batch ID must match the directory name.")
            companion_ids = []
            for name, kind, other in (("tests.md", "tests", "report"), ("report.md", "report", "tests")):
                record = path.with_name(name)
                if not record.is_file():
                    record = path.with_name(name.capitalize())
                if draft and not record.is_file():
                    continue
                record_source = record.read_text(encoding="utf-8") if record.is_file() else ""
                record_id = header_value(record_source, "id")
                expected_id = relationship(source, kind)
                sibling_id = relationship(record_source, other)
                if (not isinstance(record_id, str) or not record_id
                        or header_value(record_source, "type") != kind
                        or relationship(record_source, "batch") != lot_id
                        or (expected_id is not None and record_id != expected_id)
                        or (sibling_id is not None and sibling_id != relationship(source, other))):
                    report(path, f"Inconsistent YAML references for {name}.")
                companion_ids.append(record_id)
            if len(companion_ids) == 2 and companion_ids[0] and companion_ids[0] == companion_ids[1]:
                report(path, "Tests and Report must have distinct IDs.")
        for parts in fiche_entries(source):
            if len(parts) == 3:
                parts = [*parts, None]
            if (len(parts) != 4 or any(not isinstance(parts[i], str) or not parts[i] for i in (0, 2))
                    or (parts[1] is not None and (not isinstance(parts[1], str) or not parts[1]))
                    or (parts[3] is not None and
                        (not isinstance(parts[3], str) or not re.fullmatch(r"[0-9a-f]{64}", parts[3])))):
                report(path, "Specification entry requires an ID, revision, and path. Legacy digests must be valid.")
                continue
            try:
                path_ref = project_reference(parts[2], project, root)
                if parts[1] is None:
                    required_state = "ready" if draft else "approved"
                    if (path_ref.parent != specifications / required_state
                            or path_ref.name != f"{parts[0].lower()}.md"
                            or path_ref != root / parts[2] or path_ref.resolve() != path_ref
                            or Path(parts[2]).is_absolute() or parts[3] is not None):
                        report(path, f"An unnumbered Specification must pin its own {required_state} path.")
                        continue
                    owner = owners.setdefault(parts[0], lot_id)
                    if owner != lot_id:
                        report(path, f"Specification {parts[0]} already belongs to Batch {owner}.")
                reference = retired_pin(path_ref, parts[1], status).relative_to(root).as_posix()
            except ValueError as error:
                report(path, str(error))
                continue
            records = retired if parts[1] is None and status == "closed" else eligible if draft else approved
            pinned = records.get(reference)
            if not pinned or pinned[:2] != tuple(parts[:2]):
                state = "retired" if records is retired else "ready or approved" if draft else "approved"
                identity = "ID and path" if parts[1] is None else "ID, revision, and path"
                report(path, f"Specification entry must pin a matching {state} {identity}.")
                continue
            if parts[3] is not None and pinned[2] != parts[3]:
                report(path, f"Approved specification content changed: {parts[2]}")
            if parts[0] in selected:
                report(path, f"Duplicate specification in batch: {parts[0]}")
            selected.add(parts[0])
        if not selected and not draft:
            report(path, "A batch requires at least one approved specification.")

    for path in card_paths:
        source = path.read_text(encoding="utf-8")
        if header_value(source, "type") == "card":
            if header_value(source, "id") != CARD_ID.match(path.stem)[1].upper():
                report(path, "Card ID must match the filename.")
            lot_id = relationship(source, "batch")
            fiche_ids = relationship(source, "specifications")
            if standalone:
                if lot_id is not None or fiche_ids not in (None, []):
                    report(path, "Module Cards do not use Batch or Specification fields.")
                continue
            if ((lot_id is not None and not isinstance(lot_id, str))
                    or not isinstance(fiche_ids, list)
                    or any(not isinstance(item, str) or not item for item in fiche_ids)):
                report(path, "Card references require a batch ID or null and a list of specification IDs.")
                continue
        else:
            lot_id = field(source, "Lot ID")
            fiche_ids = [item.strip() for item in field(source, "Fiche IDs").split(",")]
        if lot_id and lot_id not in lots:
            report(path, f"Unknown batch: {lot_id}")
        for fiche_id in fiche_ids:
            if not isinstance(fiche_id, str) or not fiche_id:
                continue
            if fiche_id not in fiches:
                report(path, f"Specification is not ready or approved: {fiche_id}")
            elif lot_id in lots and fiche_id not in lots[lot_id]:
                report(path, f"Specification {fiche_id} is outside batch {lot_id}")
    return findings


def is_closed_lot_report(document, project=PROJECT):
    if not document.is_relative_to(project):
        return False
    relative = document.relative_to(project)
    if len(relative.parts) != 3 or relative.parts[0] not in ("batches", "lots", "Lots") or document.name.lower() != "report.md":
        return False
    description = document.with_name("description.md")
    if not description.is_file():
        description = document.with_name("Description.md")
    if not description.is_file():
        return False
    lines = description.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        return False
    front_matter = lines[1:lines.index("---", 1)]
    return any(re.fullmatch(r"""status:[ 	]*(?:closed|'closed'|"closed")[ 	]*""", line)
               for line in front_matter)


def verify_approval(lot_id, revision, project=PROJECT, root=ROOT):
    if not re.fullmatch(r"(?:Batch|Lot)-[0-9]+", lot_id, re.IGNORECASE):
        raise ValueError("Expected a batch ID such as Batch-001.")
    prefix, number = lot_id.split("-", 1)
    lot_id = f"{prefix.title()}-{number}"
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", revision):
        raise ValueError("Supply the full trusted approval commit ID.")
    kind = subprocess.run(["git", "cat-file", "-t", revision], cwd=root, capture_output=True)
    if kind.returncode or kind.stdout.strip() != b"commit":
        raise ValueError("The trusted approval commit is unavailable.")

    matches = [path for path in batch_descriptions(project) if path.parent.name.lower() in (lot_id.lower(), batch_slug(lot_id))]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one description for {lot_id}.")
    description = matches[0]

    def approved_bytes(path):
        relative = path.relative_to(root).as_posix()
        recorded = subprocess.run(
            ["git", "show", f"{revision}:{relative}"], cwd=root, capture_output=True,
        )
        if recorded.returncode and path == description and project == root / "project":
            for directory in ("batches", "lots", "Lots"):
                historical = f"{directory}/{lot_id}/Description.md"
                recorded = subprocess.run(
                    ["git", "show", f"{revision}:{historical}"], cwd=root, capture_output=True,
                )
                if not recorded.returncode:
                    break
        if recorded.returncode:
            raise ValueError(f"Approval mismatch: {relative}")
        return recorded.stdout

    approved = approved_bytes(description).decode("utf-8")
    current = description.read_bytes().decode("utf-8")
    status = header_value(current, "status")
    if header_value(approved, "status") != "ready" or status not in ("ready", "in-progress", "delivered", "validated", "rejected", "closed"):
        raise ValueError("Approval verification requires a ready approval and a Batch past draft.")
    if status != "ready":
        header, end, body = current[4:].partition("\n---\n") if current.startswith("---\n") else ("", "", "")
        if end:
            header = re.sub(r"(?m)^status:[^\n]*$", "status: ready", header, count=1)
            current = "---\n" + header + end + body
    if current != approved:
        raise ValueError(f"Approval mismatch: {description.relative_to(root)}")
    findings = validate_lot_mapping((), project, root)
    if findings:
        raise ValueError("\n".join(findings))
    resources = specification_root(project) / "resources"

    def check_resources(fiche, source):
        for link in resource_links(source):
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (fiche.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(resources):
                continue  # Other linked files are references to living documents, not frozen resources.
            recorded = approved_bytes(target)
            active = resources / "active"
            candidates = [target]
            if target.is_relative_to(active):
                candidates.append(resources / "archived" / target.relative_to(active))
            if not any(path.is_file() and path.read_bytes() == recorded for path in candidates):
                raise ValueError(f"Approval mismatch: {target.relative_to(root)}")

    for entry in fiche_entries(approved):
        fiche = retired_pin(project_reference(entry[2], project, root), entry[1], status)
        original = root / entry[2]
        recorded_fiche = approved_bytes(original)
        if fiche.read_bytes() != recorded_fiche:
            raise ValueError(f"Approval mismatch: {fiche.relative_to(root)}")
        check_resources(fiche, recorded_fiche.decode("utf-8"))
    print(f"Approval verified for {lot_id}.")
    return 0
