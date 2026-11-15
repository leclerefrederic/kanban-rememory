---
type: specification
id: "SPEC-021"
revision: "1"
---
# Independent modules in one shared repository

## Expected outcome

A User can evolve modules of one solution independently, each with its priorities, Kanban, Specifications, Batches and memory. Sources and data models remain shared. Agents retain their roles and integrate scoped, compatible changes into the same main branch.

Requested on 2026-11-15. Draft for User review; approval and development authorization are pending. No multi-module activation or repository migration is authorized.

## Scope

### 1. Project manifest and compatibility

An optional root `project.json` declares identity, stable module IDs, paths and execution constraints for agents/tools. Proposed schema v1, with illustrative module names:

```json
{
  "schema_version": 1,
  "project": {
    "id": "kanban-rememory",
    "name": "Kanban Rememory"
  },
  "shared": {
    "memory": "project/rememory/",
    "sources": ["agents/", "documentation/"]
  },
  "modules": {
    "workflow": { "workspace": "project/modules/workflow/" },
    "integrations": { "workspace": "project/modules/integrations/" },
    "remy": { "workspace": "project/modules/remy/" }
  },
  "execution": {
    "active_deliveries_per_module": 1,
    "branch_required": true,
    "worktree_required": true,
    "concurrent_integrations": 1
  }
}
```

- Tools enforce these v1 execution values; reject unsupported values/schema versions.
- Paths are repository-relative. Reject duplicate IDs/JSON keys, escaping paths, overlapping module workspaces or global/module memory, including symlink aliases. An invalid manifest blocks affected operations without falling back to legacy mode.
- `shared.sources` locates common sources without relocating them or granting permissions. Worktrees have separate working copies of the same repository.
- Module workspaces contain `kanban/`, `rememory/`, optional `specs/` and `batches/`, using existing lifecycles. Local `kanban/workflow.json` owns stages, transitions and Card WIP. Enforce both local and project constraints; report contradictions before execution.
- Without a manifest, existing single-project behavior remains valid. Setup shows the layout and requires explicit activation/migration approval. Preserve IDs and frozen records' bytes/paths; never automatically redistribute history. Finish existing active work under its current rules before activation; do not erase ownership by switching layouts.

### 2. Identity, selection and agent scope

- Identity is project + module + record type + local ID, plus revision for Specs. Local IDs may repeat across modules. Qualify references, ownership, recovery and notifications to avoid collisions; retain existing local naming conventions.
- Invocation identifies role, project, module and authorized mission. Auto-select a sole module. Otherwise require an explicit assignment or unambiguous reference; clarify before writes/pickup, never default to the first module.
- KR Orchestrator coordinates the solution/dependencies; KR Writer prepares module scope and User decisions; KR Developer owns authorized execution/integration; KR Tester checks the exact candidate and relevant shared effects. Roles and their authority remain unchanged.
- Read manifest, common instructions, recent relevant global memory, then assigned module records. Follow dependency links as needed instead of loading every module's history.
- Authorized work may touch shared sources, but not unrelated work or another module's records without its own assignment. Cross-module changes have one owning module/Developer, explicit dependencies and affected checks; unmet prerequisites block dependent work.
- Adapt path resolution, role policies and Codex/Claude context while preserving role/configuration protections. The manifest cannot widen rights. Distinguish verified host enforcement from advisory instructions.

### 3. Global and module Rememory

- Local journals hold decisions, execution/verification milestones and resumption checkpoints. Global memory holds shared decisions, verified published deliveries, dependencies created/lifted, common format/rule changes and cross-module blockers.
- Use concise dated entries linking module, Card/Batch, revision and local evidence; avoid duplicate narratives. Global entries identify impact and next coordination action when relevant.
- Coordinate Developer-owned writes: concurrent entries survive, retries do not duplicate a milestone. Existing journal conventions/permissions apply at both levels.
- Journals are context, not locks or WIP counters. `project.json` contains no execution state.

### 4. One active delivery per module

- A standalone Card or Batch occupies its module's slot from pickup through verified closure, including blocking, interruption, acceptance/integration waits and rejected archival. Other independent modules may progress.
- Batch Cards retain local Card WIP and mission order. The owning Developer may delegate independent tasks in parallel without creating another delivery or bypassing WIP.
- One open Batch per module; a draft/ready Batch does not occupy the execution slot. After pickup it excludes standalone deliveries until closure. Every pickup requires approved scope, execution authority, dependencies and capacity.
- Sessions share durable ownership independent of branch snapshots. Atomic module pickup records owner, delivery, branch, worktree and checkpoint; simultaneous attempts yield one owner. Tracking updates become visible across sessions without merging unfinished product changes or losing writes. Resume the same assignment; age alone never justifies clearing ownership.
- Initial concurrency covers worktrees of one clone. Separate clones require shared coordination before concurrent execution; building distributed coordination is outside this revision. Report unsupported setups explicitly.

### 5. Isolation and common integration

- Each standalone Card/Batch has a temporary branch and worktree, recorded owner/base revision and existing branch conventions (`codex/` here). Batch Cards use their delivery branch. No product development directly on main. Preserve control-record ownership and separation from Batch implementation branches.
- Isolate runtime resources used by concurrent checks where needed: temporary files, databases, ports and artifacts. Git isolation alone is insufficient.
- Serialize integration from selecting current main through combined verification and publication. If main changes, reconcile and recheck; never overwrite intervening work.
- Release global integration ownership while waiting for a human decision or a blocking prerequisite; retain the module slot and candidate evidence. Other modules may integrate. Reacquire ownership and recheck current main on resumption.
- Check the combined result, affected shared contracts and module regressions, even without merge conflicts. If integration changes an accepted candidate, preserve previous evidence and apply affected acceptance checks and existing User decision rules to the new candidate before publication.
- Developer owns review/integration; Orchestrator coordinates order/dependencies. Sequence incompatible shared changes or restore compatibility before dependent delivery; do not silently extend another module's scope.
- Resume interrupted integration/publication from revision and remote evidence. Retain existing accepted/rejected closure, recovery, immutable-history and safe branch-retirement rules, qualified by module. Release capacity only after verified closure.

### 6. Notifications and boundaries

Retain Remy's events, language fallback, structure and delivery handling. Identify solution, module and Card/Batch, including module in deduplication. Use one sender per event and existing completion/publication and authorization rules.

Scheduling (SPEC-005), notification opt-in (SPEC-013), new channels, secret stores, deployment environments and migrating our repository are separate scope. No automatic start authority. Keep agent instructions concise and load module context on demand.

## Acceptance criteria

Use isolated repositories with modules A/B and shared sources. Developer supplies candidate/environment; Tester records acceptance. These scenarios are requirements, not results.

| ID | Setup and action | Expected result |
| --- | --- | --- |
| MM-01 | Operate an existing project without a manifest; separately configure two modules through approved setup. | Legacy behavior is preserved; setup shows the intended layout, creates separate tracking spaces and retains common sources. |
| MM-02 | Supply invalid JSON, duplicate IDs/keys, unknown schema, unsupported policy values, overlapping/escaping paths and symlink aliases. | Explicit actionable failure before affected writes; no fallback to another project/module. |
| MM-03 | Give A and B identical Card/Spec/Batch IDs; select each, then submit an ambiguous command. | Qualified references resolve correctly, including Spec revisions; the ambiguous write/pickup waits for clarification. |
| MM-04 | Invoke all four roles on A in Codex and Claude; exercise forbidden role operations and an authorized shared-source change. | Existing role limits hold at new paths; B's records remain outside A's assignment. Host enforcement/advisory evidence is distinguished. |
| MM-05 | Publish independent A and B deliveries, retry one journal write, then start a fresh session scoped to A. | Both local histories and concise linked global milestones survive once; startup loads relevant common/A context and follows needed dependencies. |
| MM-06 | Race two agents for A while another starts B; update tracking with conflicting branch-local state. | One owner per module; tracking is visible without unfinished product integration or lost writes. Stale copies cannot bypass ownership. |
| MM-07 | Block A, deliver it for acceptance, then wait for integration; attempt another A delivery at each stage. | A's slot remains occupied until verified closure; independent B work can continue. Rejection also retains A's slot until closure. |
| MM-08 | Prepare a Batch during an A Card, then execute that Batch after closure alongside a B Card; delegate tasks and try a second A pickup. | Draft/ready reserves no slot. Active deliveries each have a branch/worktree; helpers obey owner/Card WIP; a second A delivery cannot start. |
| MM-09 | Interrupt an owner and resume in a fresh session; attempt a takeover while the original still runs. Try unsupported multi-clone execution. | Resume preserves identity/checkpoint; no live-owner takeover or unsupported concurrency guarantee. |
| MM-10 | Run checks concurrently using the same default resource names. | Required runtime isolation prevents one module's checks from altering the other's artifacts or results. |
| MM-11 | Request two integrations together and advance main before the second publishes. | One integration at a time; the second verifies against current main and preserves intervening changes. |
| MM-12 | Make passing branches incompatible via a shared format; alter an accepted candidate at integration, then await a decision. | Incompatible publication stops; affected acceptance/decision refer to the new candidate. Global integration ownership is released, B can publish, and A rechecks main on resumption. |
| MM-13 | Interrupt accepted publication and rejected archival, then resume each. | Existing recovery completes once for the qualified delivery; rejected product changes stay outside main, evidence survives and slots release only at closure. |
| MM-14 | Produce equivalent Remy events for A and B with identical local IDs; replay one event. | Two distinct module-qualified alerts, one per event; confirmed replay is deduplicated and existing language/next-action rules hold. |
| MM-15 | Propose activation with frozen records and active work; decline, then approve it. | Decline changes nothing. Activation waits for existing work to close; approved setup preserves frozen bytes/paths and IDs, and starts with reconciled ownership. |

## Resources

- [Project layout](../../../agents/setup/project-layout.md): existing tracking structure and optional Batch records.
- [Kanban](../../../agents/guidelines/kanban.md) and [Batches](../../../agents/guidelines/batches.md): lifecycle, WIP, approval and immutable-history baseline.
- [Orchestration](../../../agents/actions/orchestrate-work.md): role delegation, parallel helpers and coordinated notifications.
- [Development](../../../agents/actions/develop-batch.md) and [closure](../../../agents/actions/close-batch.md): isolation, exact candidates, recovery and publication baseline.
- [Notifications](../../../agents/actions/notify-user.md): existing Remy contract; no external attachment required.
