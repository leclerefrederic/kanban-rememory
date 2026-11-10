# Kanban & Rememory

Une méthode de travail dans Git pour suivre les tâches, conserver les preuves et reprendre un chantier entre personnes ou agents.

| Fichier | Rôle |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Consignes de reprise, d’exécution et de transmission |
| [Règles du Kanban](kanban/README.md) | Qualification, colonnes, identifiants et transitions |
| [Modèle de carte](kanban/task-template.md) | Résultat attendu, périmètre, dépendances et critères |
| [Guide Rememory](Rememory/README.md) | Journal des décisions, vérifications et suites |
| [Modèle de journal](Rememory/daily-template.md) | Structure d’une entrée quotidienne |

## Adopter la méthode

Copier `AGENTS.md`, `kanban/` et `Rememory/` dans le dépôt cible. Si un `AGENTS.md` existe, intégrer les consignes au fichier en place. Fixer le préfixe des cartes, le fuseau du journal et les autorisations Git du projet dans ses consignes. Pour un dépôt multi-applications, définir où chaque propriétaire tient son journal.

Le Kanban donne l’état officiel d’une tâche. Rememory explique les décisions, ce qui a été vérifié et par où reprendre. Git conserve les changements des deux.
