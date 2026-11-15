"""Resolve the Specification record layout for one workspace."""

SPECIFICATION_NAMES = ("specifications", "specs")


def specification_root(workspace):
    canonical, legacy = (workspace / name for name in SPECIFICATION_NAMES)
    existing = []
    for path in (canonical, legacy):
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Specification path must be a local directory: {path}.")
        if path.is_dir():
            existing.append(path)
    if len(existing) > 1:
        raise ValueError(f"Ambiguous Specification directories in {workspace}: specifications/ and specs/.")
    return existing[0] if existing else canonical


def specification_directories(workspace):
    specs = specification_root(workspace)
    paths = tuple(specs / subpath for subpath in (
        "draft", "ready", "approved", "retired", "resources/active", "resources/archived",
    )) + (workspace / "batches",)
    for path in (*paths, specs / "resources", workspace):
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Batch records path must be a local directory: {path}.")
    return paths
