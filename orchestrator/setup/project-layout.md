# Installed project layout

This is the resulting layout, not a copy list. [Installation](install.md) owns copying and configuration. Product code and tests stay alongside it.

```text
project/
  settings.json
  rememory/
    YYYY-MM-DD.md
  modules/
    notifications/
      backlog/
      cancellation/
      completion/
      development/
      resources/
    misc/
      backlog/
      cancellation/
      completion/
      development/
      resources/
```

The `workflow` section of `settings.json` defines stage names and order. Cards use one project-wide ID sequence. Attachments live under the owning module's `resources/<card-id>/`. The dated files in `rememory/` form one project journal. Coordination state lives in the clone's shared Git directory under `kanban-rememory/`, not in the repository.
