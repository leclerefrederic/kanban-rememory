# CARD-00000141 — Native Claude verification passed

2026-11-15. Exact candidate: `98ac495347b3da93b71aa449c45f43656e131b30`. CLI: **Claude Code 2.1.323**, `/Users/fleclere/.local/bin/claude`. Native default model observed in all five init events: `claude-sonnet-5-5`; permission mode `default`.

**Five bounded probes passed.** Fresh named Writer, Developer and Tester were discovered and ran; both legacy names reached native PreToolUse as their actual legacy identities. All 17 Read calls stayed within the approved fixture instructions. Every command exited 0, every result had `is_error: false`, and no tool error, permission denial or fixture-scope refusal occurred. All observed PreToolUse hook responses completed with exit 0.

## Exact fixture and scope

Fixture: `/private/tmp/card141-native-claude`, detached at the exact candidate. Final tracked diff is empty. Sparse checkout exposes only AGENTS/CLAUDE, roles, working-rules, host adapters and the files needed for the real hook. Original main and the owner's product worktree were not edited. No Card, journal or Telegram action occurred.

The real installer ran in the fixture:

```sh
python3 agents/tools/install-claude-role-hook.py --apply
```

The product hook command remains unchanged in fixture settings: `python3 "$CLAUDE_PROJECT_DIR/agents/tools/role-limit-hook.py"`. Canonical installed adapters are byte-identical to candidate sources. Two extra fixture-only adapters, `development-agent.md` and `specification-agent.md`, contain exact historical baseline `308b747` adapter bytes; their old role paths resolve through the candidate's relays.

A separate observational PreToolUse Read hook records only session ID, actual `agent_type`, tool name, file path and scope verdict. It also refuses any Read outside fixture AGENTS/CLAUDE, `agents/roles/` and `agents/guidelines/working-rules.md`, enforcing the User's narrow data-sharing scope. No such refusal occurred. This fixture restriction is separate from the unchanged product role policy.

## Results based on native hook inputs

| Requested native name | Actual `agent_type` | Canonical policy selected by exact candidate | Reads | Session ID |
| --- | --- | --- | ---: | --- |
| `writer` | `writer` | `agents/roles/writer.md` | 3 | `912bc41a-b5c7-493d-9c4e-16d3aadc580c` |
| `developer` | `developer` | `agents/roles/developer.md` | 3 | `37cd25d9-3cb5-44f8-aee3-b5ef9089a20b` |
| `tester` | `tester` | `agents/roles/tester.md` | 3 | `6ec3c79e-1f33-4f0f-9d52-d5646d57ab46` |
| `development-agent` | `development-agent` | `agents/roles/developer.md` | 4 | `cb232b63-075d-4b59-9669-391530cae6a7` |
| `specification-agent` | `specification-agent` | `agents/roles/writer.md` | 4 | `a7fe79e0-1152-48a1-9c66-030685f829b9` |

The canonical runs each read AGENTS, their canonical role and working-rules. Each legacy run additionally read its old role relay. The source hook's `ROLE_ALIASES` and `load_roles`/`decide` were compared locally against the captured native input: each identity selects the canonical policy shown and permits the observed Read. The alias comparison is a local check of the exact candidate; the native identity is proven by hook input, not by the assistant's self-description.

## Command and data isolation

Each run used this command, substituting one of the five names above and a matching output filename:

```sh
claude -p --agent writer --setting-sources project --disable-slash-commands --strict-mcp-config --tools Read --output-format stream-json --verbose --include-hook-events --permission-prompts none < /private/tmp/card141-native-claude-probe.txt > /private/tmp/card141-native-claude-writer-approved.jsonl 2> /private/tmp/card141-native-claude-writer-approved.stderr
```

The prompt requested only the named role's approved instructions and a one-line role identification; it prohibited project-record/Specification reads, search, shell commands, writes, child agents and notifications.

Isolation was checked before the authenticated call:

- No user or ancestor AGENTS.md, CLAUDE.md or CLAUDE.local.md; no user rules directory; fixture-specific auto-memory directory absent.
- User settings were excluded, removing user-installed plugins. Native init confirmed only builtin plugins, `tools: ["Read"]`, and empty `skills` and `mcp_servers` on all five runs.
- Project settings, the real role hook and native project-agent discovery remained active. No bare mode, safe mode, permission bypass, model override or broad permission grant was used.
- A nonauthenticated preflight with `--restricted` removed native project-agent discovery, so that mode was not used for the approved tests. The scope restriction above protects the approved file boundary without disabling discovery.

## Approval and earlier attempts

The initial pre-approval startup at `8f69fc3` discovered the three canonical agents but stopped before model/tool use because native authentication was unavailable inside the sandbox. A normal read-only `claude auth status` escalation established that native login exists outside the sandbox; no secret or account identifiers are included in this report.

Automatic review initially rejected the authenticated probe because private instructions would be transmitted to Anthropic without sufficiently specific authorization. No workaround or retry occurred before approval. The User subsequently explicitly approved **« Autoriser ce test Claude en lecture seule »**, in response to the request naming Claude/Anthropic and only the isolated project's instructions. Each successful escalation justification repeated that exact approval, destination and bounded payload. No further approval rejection occurred.

## Evidence and limits

- Sanitized machine-readable summary: `/private/tmp/card141-native-claude-summary.json`.
- Actual identity observations: `/private/tmp/card141-native-claude-events.jsonl`.
- Prompt: `/private/tmp/card141-native-claude-probe.txt`.
- Streams: `/private/tmp/card141-native-claude-<name>-approved.jsonl` and matching `.stderr` for the five names in the table.
- Observer: `/private/tmp/card141-native-claude-observer.py`; configuration is fixture-only `.claude/settings.json`.

No prohibited read was forced. Thus these are native discovery, actual-identity and positive Read/hook checks; the negative permission matrix remains covered by the owner's 14 passing migration unit tests, not relabeled as native denials. Legacy identities were launched now using historical adapters. A process genuinely started before upgrading and then resumed was not tested. No desktop-host, Codex-host, default-skill activation or native write/Git behavior claim is made by this report.
