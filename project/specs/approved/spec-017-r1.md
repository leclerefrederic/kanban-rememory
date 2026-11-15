---
type: specification
id: "SPEC-017"
revision: "1"
---
# Start the main session as KR Orchestrator

## Expected outcome

When the user opens a standard Codex or Claude Code session on a project that has adopted the kit, the session takes the KR Orchestrator role as soon as it reads the project's startup instructions. The user can describe the work directly without naming a skill or role first.

## Scope

- Use KR Orchestrator as the displayed name. Preserve existing technical entry points for compatibility. Set the default in the repository startup instructions used by each host. Both entry points direct the session to the Orchestrator role defined by SPEC-016.
- Apply the default to the main session only when no other role was explicitly selected for that session. An explicitly selected role and a delegated agent's assigned role take precedence, including when the agent reads the same repository instructions.
- Starting as Orchestrator means reading its role instructions and leading the conversation. Approval requirements for changes, Batch pickup and delegation continue to apply.
- The repository instructions establish a behavioral default. Any enforced role identity still follows the launch mechanism defined by the project and host. Document the distinction and update the kit adoption instructions for both hosts.

## Acceptance criteria

Exercise these checks within the Card and Batch journeys specified in the Batch acceptance plan. Start the host in the ordinary project with the integrated candidate; target an isolated fixture for disposable work. Verify launch-role enforcement within the applicable technical checks.

1. Open a normal session in the project and describe a bounded change without naming a role or skill. It identifies itself as the KR Orchestrator, proposes the appropriate route, and waits for approval before development.
2. Open a session explicitly as Development Agent, then as Specification Agent. Each retains its selected role after reading the repository startup instructions.
3. From the default Orchestrator session, authorize a small change and observe the delegated Development Agent. It retains the assigned Development Agent role after reading the same startup instructions.
4. Where the optional Claude Code role hook is installed, verify that the declared launch role still controls enforcement. An undeclared session is described according to the hook's actual coverage.

## Resources

- [SPEC-016 revision 1](../approved/spec-016-r1.md) defines the Orchestrator workflow. The default depends on that role being available.
- [SPEC-012 revision 1](../approved/spec-012-r1.md) defines how the optional Claude Code hook determines role identity.
