# Add the Batch module

Optional. Confirm project permissions and include it in the approved setup.

Use `--with-batches` in the preview and application of [single-project setup](configure-workflow.md#apply-and-verify) or [initial module setup](project-modules.md). To enable Batches later in an existing module, create the approved [record directories](project-layout.md) in its workspace without rerunning module activation. New workspaces use `specifications/`. Preserve an existing `specs/` layout, including frozen records. Resolve an ambiguous workspace containing both names before applying changes.

The blank templates ship with the core package. Copy `agents/tools/guard-batch-work.py` for artifact protection. For optional automatic closure checks copy `check-batch-publication.py` and `agents/tools/git-hooks/`. The core `kanban/` package provides their dependencies.

The shared role instructions define Writer, Developer and Tester responsibilities. Skills are an optional explicit entry. Verify a fresh role session identifies its observed Batch state and next permitted action. Writer prepares scope and records; Developer verifies approval/pickup and Git; Tester owns delivered acceptance observations. [Batch rules](../guidelines/batches.md) define states/data; [develop](../actions/develop-batch.md) and [close](../actions/close-batch.md) define execution. No Batch is created just to activate this option.

## Optional push check

First inspect existing `core.hooksPath` and project hooks. Do not replace unrelated hooks without an approved integration. If the kit hook directory is the agreed configuration, enable once per clone:

```sh
git config core.hooksPath agents/tools/git-hooks
```

When a push to main closes a Batch with a guard record, the hook invokes `publish` against the pushed commit for accepted or rejected closure and refuses failures. Other pushes are not checked; non-Git changes are outside coverage. Guard data lives in the clone's shared Git directory, not in a fresh clone or the artifact. [Development](../actions/develop-batch.md#protect-acceptance-builds) owns guard creation/freeze/correction and closure owns final publication checks.

Verify board records, approval comparison, guard behavior and hook preservation in a disposable repository before relying on the option. Record installation versus activation and observed checks separately.

The [scheduled-job document](../actions/scheduled-batch-job.md) describes a future agent procedure. Copying it installs/enables no scheduler or autonomous dispatch; actual future scheduling needs separate implementation, authorization and end-to-end tests.
