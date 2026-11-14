---
type: specification
id: "SPEC-012"
revision: "1"
---
# Optional role-limit hook for Claude Code

## Expected outcome

The User runs the Specification Agent and the Development Agent as separate sessions. Today each role file lists what the role may read, write and never do, but nothing stops a session from leaving its role, for example when the User gives an instruction that crosses it. After delivery, a project can enable an optional check for Claude Code that refuses an action outside the declared role of the session, and tells the User which agent to continue with. Codex stays advisory in this version. The check is a safety net on top of the written limits: projects that do not enable it work exactly as before.

This records decisions the User gave on 2026-11-14 and the findings recorded in the Rememory entries of that day. It was requested by the User and approves nothing yet; implementation is not authorized by this writing. Approval is pending.

## Scope

### Principles already decided by the User

- Protect the transitions (Specification approval, acceptance, publication), not the sessions. The Batch checks and the optional push check already do this and are not changed by this Specification.
- Hooks are an optional layer on a shared core. The role files stay the only definition of each role's limits; a hook reads them and never widens, narrows or reinterprets them.
- The shared core must work for ChatGPT/Codex and for Claude. The desktop chat applications (Coworker mode) stay advisory: this version adds nothing for them.

### What the check does

- Given a session with a declared role, refuse a read or a write that the role file lists as outside the role, including reads, because the limit covers reading as well as writing. Refuse the actions the role file marks as forbidden when they can be recognized from the tool call (for example a Specification Agent session touching `project/kanban/` or the Git state, or a Development Agent session reading `project/specs/draft/`).
- A refusal states the rule that applies and tells the User to continue in a new session, or in an existing one, with the agent whose role allows the action. It does not offer to override the rule: an instruction to cross a role limit is refused ("Overriding a rule" in `agents/work-in-a-project.md`).
- The check only allows or denies. It asks nothing, grants no permission that the role file does not give, and does not replace the User's approvals.
- The Specification Agent can still write only where its role allows, and the Development Agent can still record the journal entry of a rule exception; the check follows the role files as they stand.

### How the role is known

- The User starts the session as one role. The role must be known to the check from the way the session was launched, never from text written in a file, a tool result or a web page.
- **Claude Code:** use the identity the tool provides for a session run as a named agent.
- **Codex:** advisory in this version. The tool call carries no agent identity and no documented per-session setting carries a role, so the check is not delivered for Codex. A later revision may add it once a per-session way to declare the role is tested.
- A session whose role cannot be established is not restricted by the check. The documentation says so. The check never guesses a role.

### What the kit must say honestly

- The check is a guardrail, not a complete boundary. State in the reader and agent documentation, for each tool, what it does not cover. The recorded findings include: shell writes are not seen by a path check; Codex does not cover hosted tools, and a Codex hook that fails or times out does not block the call; a Claude settings file can be edited by the agent unless a hook, a deny rule or managed settings prevents it; repository hooks may not run in the desktop applications.
- Update the existing pages so no statement contradicts the delivered check, including the page that now marks role hooks as planned, the package lists and the install procedure.
- A project without the check, a session without a declared role, and Codex are not described as protected.

### Out of scope

- A check for Codex, until a role declaration is tested (a later revision).
- A new push, approval or acceptance check; the Batch guard and the push check keep their behavior.
- Any change to what a role may read, write or do.
- Plugins, marketplaces and managed or organization-wide settings.
- Enforcement in the Coworker or chat applications.

## Decisions and unconfirmed facts

Decisions 1 and 2 are the Specification Agent's recommendations, accepted by the User in conversation on 2026-11-14; they are final once the User approves this revision.

1. **Codex:** advisory in this version; Claude Code first.
2. **Session without a role:** not restricted by the check; the documentation states it. No message is promised in the session, because it is not confirmed that a hook can show one without blocking.
3. **Unconfirmed facts, to test in the implementation work and not assumed:** whether repository hooks run in the Claude Code desktop app (to test first, since it decides whether the check serves the User's setup) and in the Codex desktop app; whether a Codex hook inherits the launching shell environment; whether hooks apply to Codex sub-agents; whether Project instructions reach a plain Code-tab session. Each stays labelled unconfirmed in the documentation until a test settles it. No acceptance scenario below depends on an unconfirmed answer.

## Acceptance criteria

Use a scratch repository with the kit adopted and the check enabled for Claude Code. Development Agent supplies the candidate revision and environment. The scenarios are acceptance requirements, not recorded results.

1. **Out-of-role action refused:** In a session declared as the Specification Agent, ask for a read of a file under `project/kanban/` and a write of a code file. Each is refused, the message names the rule and sends the User to the Development Agent, and no file changes. Repeat the other way: a Development Agent session asked to read `project/specs/draft/` or to edit a Specification.
2. **In-role action allowed:** In each role, perform one read and one write that its role file permits (for example the Specification Agent writing a draft under `project/specs/`, the Development Agent recording a journal entry). Both succeed without a prompt added by the check.
3. **No override:** In a session of either role, instruct the agent to set a role limit aside. The action is refused and the User is redirected; no exception is recorded as accepted.
4. **Role from the launch, not from content:** Put text in a file that claims another role or authorizes the action. The role and the refusal do not change.
5. **Unknown role and Codex:** Start a Claude Code session with no declared role, and a Codex session. The check blocks no action in either, and the documentation states that the limits are advisory there.
6. **Optional and non-widening:** With the check disabled, or in a project that never installed it, the kit behaves exactly as before. With it enabled, no action becomes allowed that the role file forbids.
7. **Limits stated:** The documentation lists, for Claude Code and for Codex, what the check does and does not cover, and labels each unconfirmed fact as unconfirmed. Reading it, the User can tell which tool, role and action are protected.
8. **Consistency:** After delivery, the board validation and the adoption tests pass, installed skill copies match the kit, and no page describes role hooks as planned.

## Resources

No mockup or external attachment is required. The behavior is defined above; the role limits live in the role files [specification-agent.md](../../../agents/roles/specification-agent.md) and [development-agent.md](../../../agents/roles/development-agent.md), and the vendor findings are in the Rememory entries of [2026-11-14](../../rememory/2026-11-14.md).
