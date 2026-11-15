# Batch-012 technical verification

Candidate `1d70a04e39b39492bfac502045095cede7cc5317`, verified on `origin/codex/batch-012`. The product diff is limited to `agents/`. The published main tip at verification was `d1c711b96637fc0845c41568c158a8ba78df7f87`. The live repository remains single-project.

## Reproduction

Use a clean checkout of the candidate in `/private/tmp/kr-batch012-development` or an isolated clone. The scripts create disposable fixtures and local-only Git remotes. Run with Python 3.9+ and Git:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-kanban-board.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-module-delivery.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-module-publication.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-role-migration.py
PYTHONDONTWRITEBYTECODE=1 python3 agents/tools/test-telegram-setup.py
python3 -B agents/tools/manage-kanban-board.py validate
python3 -B agents/tools/sync-skills.py --check
```

Results: 42 Kanban, 6 module delivery, 4 publication guard, 17 role, and 23 Telegram tests passed. One supplemental runtime repeat with `KR_TEST_LOOPBACK=1` opened dynamically assigned loopback ports in the sandbox-approved fixture and passed. Diff checks, board validation, skill synchronization and the trusted SPEC-021 r1 approval snapshot passed.

| Case | Technical evidence |
| --- | --- |
| MM-01 | Board suite preserved single-project behavior. Setup preview/apply used independent A/B workspaces and shared source fixture. |
| MM-02 | Malformed and duplicate JSON, unsupported schema/policy, escape, overlap and symlink alias were refused before activation. |
| MM-03 | Same Card/Batch/Spec IDs validated in A/B. Ambiguous writes and wrong-module pins were refused. |
| MM-04 | Four native role invocations per host. Claude 2.1.323 enforced three named-role refusals and allowed the corresponding approved writes. Codex 0.169.0 and unnamed Orchestrator scope remain advisory. Two final parser replays (Claude Developer and Codex Orchestrator) passed. |
| MM-05 | A/B journal writes executed concurrently and one replay was deduplicated. Native fresh startup loaded manifest, global memory and only the selected module. Publication and journal probes were isolated fixtures. |
| MM-06 | Concurrent claims produced one A owner and one B owner. Board writes from stale branches resolved to the control worktree. |
| MM-07 | Claims remained exclusive through wait, delivered, validated and rejected. Closure held the slot until remote evidence and release. |
| MM-08 | Ready A Batch coexisted with an A Card and B Card. A Batch claimed after published Card closure. Active Card moves require owning claim; local Card WIP and helper rules retained. |
| MM-09 | A new process resumed the known owner and checkpoint. Wrong-owner takeover and pickup from a separate primary clone were refused. Coordination is scoped to one shared Git directory. |
| MM-10 | Concurrent checks used same-named DBs/artifacts in distinct directories; supplemental loopback check passed. Fixed shared resources require serial checks. |
| MM-11 | Concurrent integration ownership was refused; an advanced main invalidated prior verification. The next owner resumed against the new base. |
| MM-12 | Two independently passing candidates failed the combined shared-format check. Closure preparation was refused. A different module could acquire integration, while the original module retained its slot. |
| MM-13 | Real local Git remotes and pre-push hook verified accepted recovery ref and rejected archive interruptions. Repeated publication was idempotent, both retained refs exact, rejected code excluded, and slots released only at verified closure. |
| MM-14 | A/B same-ID alerts were distinct; replay was suppressed. Transport was simulated. |
| MM-15 | Preview made no changes; active legacy work blocked activation. Approved activation retained frozen bytes, paths and IDs. |

Native checks used synthetic project instructions and local source files/records. Earlier eight probes used the same hook and the previous manifest parser. Two replay probes used the delivered parser with the same hook. These observations verify module scope, memory loading and the covered Claude hook decisions. They do not verify installed-skill discovery or new host-level enforcement. No Tester/User verdicts are assigned here.
