---
type: specification
id: "SPEC-021"
revision: "2"
---
# Track module work on a shared project board

## Expected outcome

The User can see and prioritize all Cards from one project Kanban and filter them by module. Each module retains its Specifications, Batches and journal. From the shared board and project Rememory, an agent can find each module's active work and latest verified publication. Each detail has one reference record.

Requested on 2026-11-15. Draft for review. Approval, development and live repository migration are separate decisions.

## Scope

This revision replaces per-module Card boards with one project board. The [SPEC-021 r1](../approved/spec-021-r1.md) rules for explicit scope and authority, per-module delivery ownership, isolated branches and worktrees, serialized integration, candidate verification and safe closure apply unless refined here.

### 1. Installation and layout

- Ask the User whether the project is simple or has modules, or reuse an explicit answer. Both choices use the same board and project journal.

| Installation choice | Project records | Module records |
| --- | --- | --- |
| Simple project | `project/kanban/` and `project/rememory/` | No module workspaces. |
| Multi-module project | The same `project/kanban/` and `project/rememory/` | Root `project.json` declares the module workspaces. Each has its own `rememory/` and any enabled `specs/` and `batches/`. |

- The project board's `workflow.json` owns stages, transitions, Card WIP and timezone. In a simple project, the scope is the project. A multi-module board also supports module scopes and filters. Board placement follows the same rule for both choices.
- Preview the project board, optional module workspaces and journal locations before application. Preserve the existing single-project layout. Any transition of an existing per-module board is a separate, explicitly approved migration plan. Preserve frozen paths, IDs, bytes and reference lookup, including module-qualified historical IDs. Account for unfinished work in that plan and keep archive records outside the active queue and WIP.

### 2. Card scope, identity and authority

- Each new Card on the shared board has one stored scope: a declared module or the project itself. The board provides one view of current work, including backlog, and a filter for each scope. Project-scoped Cards track operational work for the whole solution. For a change spanning several modules with a primary outcome, select its owning module and link affected dependencies.
- A shared-board Card has one unique project-wide ID, including across stages. Allocate it without reusing an ID in the original project board. Existing frozen module-qualified references keep their original identity; new Card IDs are independent of a module prefix. Spec and Batch IDs remain module-qualified and may repeat across modules.
- Resolve scope from the stored Card, an explicit invocation assignment or an unambiguous reference. With multiple possible scopes, ask before mutation. A filter changes the view only. Validate authority and scope against the manifest and reject links from a Card to a Batch in a different scope. Other modules may be referenced as dependencies. Reassign scope on the backlog only with authorization. Keep scope stable once picked up.
- The existing role rules govern creation, prioritization, pickup and closure. Writer/Orchestrator may prepare backlog work in their assigned scope. Developer may create an authorized operational Card from a module or project assignment, or from an Orchestrator handoff. Creation alone does not authorize pickup or expand Batch scope. A Batch may use Cards as implementation records, without requiring one Card per Spec.
- Adapt command checks, role policies and host context to identify scope on the shared board. Preserve r1 access restrictions when records move from module paths to the shared path. Verify actual host controls separately from advisory instructions.

### 3. One record for each fact

| Record | Information it owns |
| --- | --- |
| Project Card | Operational outcome, scope, owner, current stage, blocker and completion checks. Link to related Spec, Batch and evidence. |
| Module Spec | Expected behavior and the revision that defines it. |
| Module Batch | Approved scope, delivery state, tested revision, verdicts, decision and closure evidence. |
| Project Rememory | Decisions concerning the solution and one short milestone for each verified published delivery, including single-module work. |
| Module Rememory | Durable reasoning specific to the module and useful resumption context. Link to existing details and evidence. |

- Route work notes by scope, even though Cards live together. Record project-wide decisions and project-scoped resumption notes in project Rememory. Keep module-specific notes in that module's journal. Use one location for each decision, rationale or checkpoint. Other records link to it.
- Add a project milestone after verifying the remote publication. Include scope, result, the revision actually published and a link to the authoritative Card or Batch. A Batch publication produces one milestone for the Batch; its implementation Cards do not generate duplicate publication milestones. Pending or failed publications do not produce published milestones.
- Module entries are useful when future sessions need context not already on the Card, Spec or Batch. A small Card with enough detail needs only its project milestone. If interrupted after publication, verify the remote revision and record the missing milestone. Key it by project, scoped delivery and published revision. Retries keep one milestone and concurrent writes preserve distinct entries.
- To answer project status, combine the shared board and active Batch records for work in progress with the latest project milestone per scope. Open local journals only for the selected module and relevant links. The manifest identifies locations. Cards, Batches and the ownership record supply execution state.

### 4. Capacity, integration and notifications

- Continue to apply one active delivery per module, independent of where Cards are stored. A standalone Card or Batch occupies that slot through verified closure. Apply the configured Card WIP per scope, including Cards used inside a Batch. Shared intake can select an eligible scope while preserving project priority and dependency rules. Use common ownership/ID coordination across worktrees so stale checkout copies cannot claim work or overwrite tracking changes.
- Proposed policy for project-scoped standalone Cards: one active delivery in a separate project slot. It can coexist with module deliveries when dependencies and impact permit. Declare affected modules and sequence conflicting work. The project slot and module slots all use the same serialized integration procedure.
- Retain branch/worktree isolation, single-clone coordination, approval requirements and the exact-candidate rule from r1. Integration verifies the combined result and releases shared integration ownership when waiting. A changed product candidate needs the applicable acceptance and decision before publication.
- Keep existing notification events, language, delivery handling and deduplication. Use scope in the message and event identity. Project-scoped Card messages identify the project and Card, and module-scoped messages identify the module as well. Retries use the original delivery identity.

This revision covers one project board and journal routing. Repository cutover plans are separate. CARD-150 tracks the eight-module migration of this repository. Scheduling, additional channels, notification opt-in and distributed coordination remain separate.

## Acceptance criteria

Use disposable repositories with modules A and B. Keep technical observations and User decisions tied to the delivered revision.

| ID | Setup and action | Expected result |
| --- | --- | --- |
| SB-01 | Walk through guided installation twice. Choose simple in one fixture and multi-module with A/B in the other. Preview and apply each configuration. | The question is whether the project has modules. Both installations use the same project board and journal. The preview makes no writes. Modular setup adds the module workspaces and preserves sources. |
| SB-02 | Reopen an existing simple project and validate a shared-board fixture with frozen module-qualified historical references. | The existing project board remains usable. Historical references resolve to their original bytes and paths. Archived Cards stay outside the active queue and WIP. |
| SB-03 | Create A, B and project Cards from their assigned contexts, including simultaneous creation. Read the full and filtered views. | Each Card appears once with a unique ID and correct scope. Scope filters select the expected Cards and creation reserves no delivery slot. |
| SB-04 | Try an ambiguous write, wrong-scope edit or pickup, and link an A Card to a B Batch. Exercise applicable roles in Codex and Claude. | Invalid operations fail before tracking changes. Prior role limits apply at the shared path, with verified host enforcement recorded separately. |
| SB-05 | Race two A pickups while B is eligible. Run a Batch on A, create an operational A Card, and exercise project-scoped work. | Only one active delivery per scope. Batch Cards stay under the Batch claim and Card WIP. Blocked deliveries keep their slot. Shared integration remains serialized. |
| SB-06 | Interrupt A in a worktree and resume from fresh context. Record journals for a project Card, a module Card and a Batch. | Ownership and state are recovered. Scope routes the work note to the correct journal. Card/Batch records retain their own state and evidence. |
| SB-07 | Publish A and B, interrupt one after push and before its journal entry, replay, and attempt a failed publication. | Each verified delivery has one concise linked global milestone, including a Batch with supporting Cards. Interrupted recording recovers without duplicates, lost concurrent writes or false publication entries. |
| SB-08 | Finish a small Card that explains its outcome. Separately record a module-specific design decision and a solution-wide decision. | The small Card needs no local summary. Detailed decisions are recorded once, at their assigned level, with reference links from related records. |
| SB-09 | Ask for status across A and B, then resume only A. | The agent identifies active work and latest published changes for both, then retrieves the detail and next action for A. |
| SB-10 | Send project and module Card events through a test transport and replay one event. Verify the r1 changed-candidate and recovery paths. | Scope is clear and a replay is suppressed. Integration/closure guards and recovery still apply to the exact revision. |

## Resources

- [SPEC-021 r1](../approved/spec-021-r1.md) defines the delivered baseline.
- [Kanban rules](../../../agents/guidelines/kanban.md), [Batch rules](../../../agents/guidelines/batches.md) and [Rememory procedure](../../../agents/actions/maintain-rememory.md) define the existing record responsibilities.
- [Module coordination](../../../agents/actions/coordinate-modules.md) defines delivery ownership, integration and publication guards.
