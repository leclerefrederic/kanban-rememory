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

## Définir le flux à l’adoption

Les quatre dossiers ci-dessus forment un exemple de départ. Documenter ici les types de tâches suivis, les étapes utiles au projet, les critères d’entrée et de sortie, et les points précis où le travail compte comme démarré et terminé. Dans cet exemple, l’entrée en `in-progress` marque le début et l’entrée en `done` marque la fin. Définir l’ordre de sélection des cartes admissibles et les règles d’exception, ainsi que les rôles et autorisations dans les consignes du projet.

## Gérer le travail en cours

Fixer une limite explicite de travail en cours (WIP) pour l’ensemble du flux ou pour les étapes qui en ont besoin. Quand une place se libère, sélectionner la prochaine carte admissible selon l’ordre convenu. À la limite, aider à terminer ou à débloquer les tâches engagées. Consigner toute exception et sa justification.

Si une carte est bloquée après son démarrage, garder son étape visible, indiquer depuis quand, pourquoi et qui ou quoi peut la débloquer. Elle compte dans le WIP jusqu’à sa clôture ou son retrait explicite. Une carte du backlog dont un prérequis manque reste en attente et ne consomme pas de capacité.

## Mesurer et améliorer le flux

Utiliser les dates réelles de début et de fin, en jours calendaires dans cet exemple. Choisir une période de mesure et revoir le flux à un rythme adapté au projet.

| Mesure | Calcul dans le flux d’exemple |
| --- | --- |
| Travail en cours (WIP) | Nombre de cartes démarrées et encore actives, y compris les cartes bloquées |
| Débit | Nombre de cartes arrivées en `done` sur la période |
| Âge d’une carte en cours | Temps écoulé depuis son début jusqu’à aujourd’hui |
| Temps de cycle | Temps écoulé entre le début et la fin d’une carte terminée |

Suivre les abandons séparément du débit. Établir une prévision de délai à partir des temps de cycle observés, en donnant une durée et une probabilité. Par exemple, si 85 % des cartes comparables ont été terminées en 10 jours ou moins, utiliser ce repère pour examiner les cartes qui approchent de cet âge. Sans historique suffisant, partir d’une estimation explicite et la réviser à mesure que les données s’accumulent.

Lors des revues, examiner les cartes qui vieillissent, les blocages récurrents et l’évolution du débit. Ajuster les limites ou les règles de passage selon les observations, puis vérifier l’effet du changement lors d’une revue suivante.

Source : [The Kanban Guide](https://kanbanguides.org/the-kanban-guide).
