# Kanban Markdown

| Colonne | Condition |
| --- | --- |
| [backlog](backlog/) | Travail qualifié et accepté, en attente d’exécution |
| [in-progress](in-progress/) | Exécution autorisée et démarrée, y compris les interruptions avec point de reprise |
| [done](done/) | Critères d’acceptation vérifiés et preuves consignées |
| [discarded](discarded/) | Abandon décidé et motif consigné |

Le dossier fait foi. Une carte existe dans une seule colonne. Déplacer le même fichier en conservant son nom et son identifiant. Les tickets externes peuvent être liés comme sources.

## Qualification et exécution

1. Chercher les doublons dans les quatre colonnes. Réutiliser la carte pertinente ou qualifier une nouvelle tâche avec le demandeur. Poser les questions qui changent le périmètre ou la décision.
2. Une fois l’inscription approuvée, copier le [modèle](task-template.md) en `backlog/TASK-0001-sujet.md`. Relever le plus grand numéro dans toutes les colonnes et prendre le suivant. Vérifier à nouveau avant d’intégrer en cas de contributions parallèles. Ne jamais réutiliser un identifiant retiré.
3. Vérifier les prérequis avant de démarrer. Une dépendance non validée, non livrée ou renvoyée en réécriture bloque les cartes qui en dépendent, directement ou indirectement. Les cartes non démarrées restent en backlog avec la chaîne du blocage.
4. À l’autorisation d’exécution, déplacer la carte en cours. Une interruption conserve cet état et indique le blocage et l’action de reprise.
5. Vérifier chaque critère avant de déplacer la carte en terminé. Lier le journal et les preuves. Si un critère de validation utilisateur reste ouvert, le signaler explicitement. En cas d’abandon, consigner le motif et déplacer la carte en écarté.
