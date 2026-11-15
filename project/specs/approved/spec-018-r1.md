---
type: specification
id: "SPEC-018"
revision: "1"
---
# Let KR Writer draft Cards and KR Developer execute them

## Expected outcome

The user can frame a standalone change with KR Writer and review a complete backlog Card before authorizing development. KR Developer picks up that same Card, performs the work, and records its outcome. KR Orchestrator guides the handoff in the work chat.

## Scope

- Use **KR Writer** and **KR Developer** as the user-facing names for Specification Agent and Development Agent. Preserve their technical identifiers for existing launches, skills and hooks.
- KR Writer retains its Specification and Batch preparation responsibilities. It may read the board to find existing Cards and create or revise backlog Cards to record the proposed outcome, scope and acceptance checks. It follows the existing rules for IDs and backlog entry. KR Orchestrator may do this when acting within KR Writer's role.
- KR Developer owns pickup, stage transitions, execution records, blockers, technical checks, Git and closure. It reuses the Card handed off by KR Writer. The existing standalone flow remains available to users working directly with KR Developer.
- Card preparation is distinct from user approval of scope and authorization to start. At pickup, KR Developer verifies both, checks eligibility and work-in-progress limits, and takes ownership of the Card.
- If development reveals a material scope change, KR Developer pauses the affected work and reports the proposed change. KR Writer drafts revised scope for review, KR Orchestrator obtains the user's decision, and KR Developer records any approved revision on the active Card before continuing. Completed Cards follow the existing follow-up rules.
- Align role files, skills, startup instructions, guides, fixtures and the optional Claude Code role hook with these names and permissions. Update references and dependent instructions across the three roles and the Orchestrator. KR Tester owns guided acceptance under SPEC-019. A launch declared as KR Writer's existing technical role may prepare backlog Cards within the written limits. The hook continues to refuse changes to active or completed Cards by that role when the relevant operation is covered. Describe the actual enforcement coverage. This Specification makes no change to default activation or parallel development.

## Acceptance criteria

Cover these checks within the Batch acceptance plan and technical role checks. Use isolated work targets for disposable changes.

1. Frame a standalone change with KR Writer. It finds an existing backlog Card or creates one, records the proposed checks, and presents the scope for review. Nothing enters Development before user authorization.
2. Authorize the proposed scope. KR Orchestrator hands off the same Card ID, and KR Developer picks it up, verifies eligibility, performs the work, records evidence, and closes it when the applicable rules allow.
3. During development, surface a material scope change. KR Writer can propose amended wording, and development of the changed scope waits for the user's decision. KR Developer records the approved change on the active Card.
4. With the optional Claude Code hook enabled, exercise the technical launch roles. KR Writer can edit an eligible backlog Card. A covered attempt to edit a Development or Completion Card or write product code is refused. KR Developer retains its existing authority over execution and closure.
5. Follow the user-facing instructions for both roles and verify that existing technical launch identifiers and the direct KR Developer workflow still work.

## Resources

- [SPEC-019 revision 1](spec-019-r1.md) defines the KR Tester role and guided acceptance handoff.

- [SPEC-016 revision 1](../approved/spec-016-r1.md) defines orchestration and the current handoff.
- [SPEC-012 revision 1](../approved/spec-012-r1.md) defines the optional role hook.
- [SPEC-017 draft](spec-017-r1.md) separately describes default role activation.
