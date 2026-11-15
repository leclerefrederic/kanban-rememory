---
type: specification
id: "SPEC-012"
revision: "2"
---

# Protect agent settings and verify Codex role enforcement

## Expected outcome

When the User enables role protection, routine agent work leaves the settings and policy behind that protection intact. The User can see where the kit enforces role limits and where its instructions remain advisory. This revision supersedes r1 only if approved. It is submitted for scope review. Development has not started.

## Rules carried forward

Role files remain the authority for permitted reads, writes and Git operations. The optional host integrations apply those rules to supported actions and never grant permissions. Refusals explain the applicable limit and direct the User to the appropriate role. An instruction in a prompt, repository document or tool result cannot change the active role. The shared workflow, Batch approvals, acceptance and publication rules keep their existing behavior.

## Protect the settings used by the check

For an enabled integration, identify the effective project settings, hook definitions and executable, role policy files, and any role declaration or state used by the check. Protect these from agent writes during ordinary work on supported paths, including deletion or replacement. Verify protection with the host's effective permissions. A hook's ability to deny a single tool call is insufficient evidence that its configuration is protected.

Provide the User with an explicit setup, update and removal procedure through a host-supported authorization path. Preserve unrelated settings and custom hooks. Report the status for each host and action surface as verified, advisory, or unconfirmed. Projects that skip the optional integration continue using the written role rules.

## Default role at startup

The User confirmed on 2026-11-15 that opening a normal session in an adopted Rememory project starts the agent as KR Orchestrator in both Codex and Claude Code. Preserve this default. Explicitly selected and delegated roles retain precedence. This observation concerns the role the agent recognizes from the project instructions. Whether the host can independently resolve that role for a given tool call remains to be verified.

## Qualify Codex before enabling enforcement

First verify, on identified clients and versions, whether a user-controlled launch or trusted host setting can bind a role to a session and whether the host exposes enough trustworthy information to apply that role to supported tool calls. Check separate sessions in the same project, resumption and delegation. Verify desktop coverage, availability of launch configuration to the check, and behavior when the check is unavailable or fails. Treat each client and tool surface independently.

Enable the optional Codex check only for combinations where role binding, allowed/denied behavior and protection of the effective settings are verified. Sessions without a verifiable role remain advisory and must be described that way in the setup and coverage matrix. If no Codex combination qualifies, deliver the evidence, keep Codex advisory and record the missing prerequisite. Claude Code retains its existing named-role integration and legacy launch compatibility.

## Acceptance criteria

Use scratch repositories, dummy files and the exact candidate revision. Record host, version, session type, tool surface and observed result.

1. **Settings protected.** With protection enabled, verify that ordinary agent operations leave the listed settings and policy fixtures unchanged while permitted project edits still succeed. Report any unverified surface separately.
2. **Maintenance works.** The authorized setup/update/removal procedure works without replacing unrelated settings or custom hooks. Repeating setup produces no unintended changes.
3. **Role binding.** For each proposed Codex configuration, start Writer and Developer sessions in the same project. Check permitted and disallowed fixture operations for each. Resume and delegate where supported. A contradictory role claim in task content has no effect. Reject the configuration as an enforcement option if the binding or decisions cannot be verified.
4. **Default startup and accurate coverage.** Check that a normal session in an adopted project identifies KR Orchestrator in both hosts and that explicit or delegated assignments retain precedence. Record separately whether the host can verify the role for tool calls. Then check a session without a verified role and each supported failure or unavailable-check condition. Confirm these cases are never reported as enforcing role limits. Mark desktop, delegated sessions and other untested surfaces unconfirmed.
5. **No regression.** Verify Claude Code named roles, legacy identities, optional installation and shared workflow. Board, adoption and skill consistency checks pass. Document the verified and advisory surfaces together.

## Out of scope

New organization-wide policy, changes to the roles' permissions, new Batch or Git guards, and claims of enforcement over unverified hosts or tools.

## Resources

- [SPEC-012 r1](../approved/spec-012-r1.md)
- [CARD-128](../../kanban/backlog/card-00000128-protect-the-agent-settings-from-edits-and-cover-codex-with-role-limits.md)
- [Claude Code role check](../../../agents/setup/claude-role-check.md)
- [Claude Code settings and precedence](https://code.claude.com/docs/en/settings)
- [OpenAI hook configuration and trust](https://developers.openai.com/plugins/build/plugins)
