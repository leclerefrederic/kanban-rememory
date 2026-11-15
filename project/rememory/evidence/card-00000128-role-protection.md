# CARD-128 — Settings protection and coverage

Approval: SPEC-012 r2, SHA-256 `21417b433138ab4c96310db0d64b50db55d0ee606fcf64364f48440262da21c6`. The User confirmed normal Orchestrator startup in Codex and Claude Code and approved implementation. Delivery adds the optional Claude CLI launch profile to setup documentation and a host coverage matrix. The hook and role policy contents are unchanged.

## Native Claude Code evidence

Claude Code CLI 2.1.323 on macOS, print sessions, synthetic files only. A User-controlled external profile supplied native Edit deny rules and strict Bash sandbox denyWrite. Project settings were included. The probes asked the agent to exercise a fixed list of operations, stop after a refusal, and avoid other files or methods. No project data was sent. Independent comparisons of the fixture bytes checked the results.

| Session | Surface | Result |
| --- | --- | --- |
| CLI without named role | Native Read and Edit/Write | Read succeeded. Edit and Write on protected dummy files were refused by the host permissions. |
| CLI without named role | Sandboxed Bash | File overwrite and deletion were refused. An ordinary project write succeeded. |
| CLI named synthetic Developer | Native Write | Project settings and policy writes were refused. |
| CLI named synthetic Developer | Sandboxed Bash | Deletion of an installed role, hook executable, hook dependency and external launch profile was refused. An ordinary project write succeeded. |

Replaying the named probe with the final profile and automatic Bash approval disabled yielded the same results. The probe authorized only its fixture tools. All six protected files in the named fixture retained identical SHA-256 digests. These probes verify the host protection layer, not a live test of the repository hook. The existing role migration suite verifies named roles, legacy IDs, installer updates/removal, preservation of custom settings and hooks, and idempotence. Desktop, IDE and unsupported tool surfaces were not tested. Settings can be maintained from the User's terminal before starting a protected agent session.

## Codex qualification

Local CLI 0.169.0 exposes profile selection at startup and resumption. The [documented hook schema](https://learn.chatgpt.com/docs/hooks) exposes session information, but it provides no verified association between an individual PreToolUse call and a role selected at launch. Subagent startup metadata does not prove the role for a later tool call. [Host sandbox protections](https://learn.chatgpt.com/docs/permissions) can restrict paths separately; they do not establish this association.

No Codex configuration qualified for optional KR role enforcement. The expected Orchestrator startup remains the User's confirmed observation. Role binding during resume and delegation, environment inheritance, desktop hooks and runtime failure coverage remain unconfirmed. There is no Codex hook installation or coverage claim for those surfaces.

## Repository checks

Diff reviewed in Development. Live board validation, skill consistency and all 37 Kanban tests passed. All 14 role migration tests passed in a clean archive with the candidate guides overlaid. The live migration test fixture also discovered a local ignored macOS metadata file under the source skills and failed that case; the clean archive excluded it. No implementation modified the approved Specification, previously completed records or unrelated local drafts.
