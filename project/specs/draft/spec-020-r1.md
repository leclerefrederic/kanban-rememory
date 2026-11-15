---
type: specification
id: "SPEC-020"
revision: "1"
---
# Review the kit installation procedure and its optional features

## Consolidation into CARD-00000141

On 2026-11-15 the User approved the migration plan and authorized CARD-00000141 refactoring. Its approved scope incorporates this installation review and all five acceptance scenarios below. This draft is retained as the source of those requirements and is no longer an independent proposal. Execution and verification belong to [CARD-00000141](../../kanban/development/card-00000141-harmonize-documentation-paths-and-role-names.md) and its [migration plan](../../rememory/evidence/card-00000141-plan.md).

## Expected outcome

A user can adopt Kanban Rememory in a new or existing Git repository, choose only the optional features they need, and verify what is usable after setup. The installation guide gives the user and the agent the same sequence and identifies any work that requires the user's action.

## Scope

- Give the core installation one clear path. Check prerequisites, preserve existing project instructions, agree on the board workflow and Git permissions, apply the approved setup, and verify the board and default KR Orchestrator in a fresh session. Use the current supported role and skill names.
- Present each optional feature when the user can decide whether to enable it: host skill installation and synchronization, the Batch module and its optional Git publication check, the Claude Code role check and named roles, and Telegram notifications. For each option state its benefit, dependencies, supported hosts, what setup changes, and how to verify the result. Explain that the scheduled Batch procedure is documentation and does not install a scheduler.
- Distinguish copying a feature's files from enabling it. Ask before enabling options that affect project settings or external services. Use the existing Telegram setup workflow and record its verification state without storing credentials in project records.
- Explain how to add an option after the core installation and how to rerun setup without replacing unrelated settings, existing project records, or other skills. Report each chosen option as verified, awaiting a user action, or blocked.
- Review the installation guide and its linked adoption, platform and feature instructions together. Repair missing dependencies, outdated commands and contradictory instructions. This is a review of adoption and verification; feature behavior changes, a new installer and scheduling automation are outside this draft.

## Acceptance criteria

1. Follow the guide in a fresh scratch repository with the core setup only. The board validates, a fresh project session applies the documented default role, and setup completes without requiring optional dependencies.
2. In an existing scratch project, keep its instructions, settings and unrelated skills. Install the selected modules and verify the documented dependency order, actual enablement and the relevant host or platform checks.
3. Add a previously skipped option and rerun the relevant setup steps. Verify that existing records and unrelated settings survive and that the final report distinguishes enabled and verified features from those awaiting user action.
4. Exercise one missing prerequisite. The procedure gives a clear recovery step and still identifies the core installation and any independent options that can be verified.
5. Check documentation links and commands against the current kit and confirm the Telegram path distinguishes local or simulated checks from real delivery.

## Resources

- [Installation procedure](../../../agents/setup/install.md)
- [Guided adoption](../../../agents/setup/configure-workflow.md)
- [Claude Code role check](../../../agents/setup/claude-role-check.md)
- [Telegram configuration](../../../agents/setup/telegram.md)
