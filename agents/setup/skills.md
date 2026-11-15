# Install or update host skills

Optional. The shared instructions work without discovery copies. Copy the four canonical `agents/skills/kr-*` source directories and `agents/tools/sync-skills.py`, plus core `agents/VERSION`, into the approved target. Keep skills as routers to shared rules, not independent policies.

```sh
python3 agents/tools/sync-skills.py
python3 agents/tools/sync-skills.py --check
```

Sources remain under `agents/skills/`. Destinations are native `.agents/skills/` for Codex and `.claude/skills/` for Claude Code. `--target codex` or `--target claude` limits the operation. Other skills remain untouched.

The synchronizer updates recognized distributed copies and preserves customized current/legacy folders, extra files and symlinks for review. A reported unresolved current copy is not a successful complete synchronization. Inspect its differences, preserve the project customization and agree the merge; do not delete it to make the check pass. A copy upgrade may leave old source folders: known unchanged retired sources are skipped; custom ones require reconciliation.

Known unchanged legacy long KR names are retired only after replacements exist. Keep the migration fingerprints; renamed paths in new sources are not the historical bytes. An old standalone skill has no replacement. Rerun after updating the kit, then open a fresh host chat to verify all four current names and an explicit role. `--check` proves copy consistency, not native host discovery or delegation availability.
