---
id: "CARD-00000229"
module: "misc"
---

# CARD-00000229 — Créer et publier le wiki GitHub de Kanban Rememory

- Dependencies: Aucune.

## Expected outcome

Un wiki GitHub en anglais, accessible depuis le dépôt KR, avec accueil, navigation et guides pour installer KR, donner une première mission, comprendre le fonctionnement, gérer les permissions et la publication, reprendre une session, configurer Remy et résoudre les blocages courants.

## Scope and authorization

L’utilisateur accepte la proposition de créer, rédiger et publier les pages du wiki GitHub : « Vas y fait le alors :) ». Le wiki cible est https://github.com/leclerefrederic/kanban-rememory/wiki ; son dépôt Git est séparé. Initialiser sa première page si nécessaire. Conserver l’anglais du README et les procédures existantes comme sources de vérité. Continuité du choix de travail documentaire précédent : suivi sur main, fast-forward et aucun changement de version ni nouveau tag KR. Publication du wiki et des traces de cette Card autorisée par cette demande ; ne modifier ni moteur, ni kit, ni réglages hôte.

## Acceptance criteria

- Les huit guides proposés existent en anglais, sans contradiction avec INSTALL.md, le guide utilisateur et le workflow.
- Une barre latérale permet d’accéder à chaque guide et de revenir à l’accueil.
- Les liens internes, les liens vers les sources du dépôt et le kit 0.1.49 sont vérifiés.
- Aucun secret, fichier de configuration privée ou donnée personnelle superflue n’est publié.
- Le wiki est publié et sa page d’accueil ainsi que sa navigation sont vérifiées sur GitHub.
- La validation KR passe ; la version reste 0.1.49 et les tags existants restent inchangés.

## Execution and evidence

Huit pages utilisateur rédigées, avec _Sidebar.md et _Footer.md. Vérification des 45 liens internes et des liens vers les sources du dépôt ; blocs Markdown équilibrés et git diff --check sans erreur. Relecture indépendante : concordance avec INSTALL.md, guide, workflow et configuration Telegram ; ton anglais incisif et accessible conservé selon la demande complémentaire.

Première page initialisée dans la session GitHub du navigateur, puis ensemble publié dans le dépôt Git séparé du wiki. Révision wiki : `67d2f12`. Accueil publié et contrôlé dans GitHub : huit pages visibles, barre latérale et pied de page rendus. Lien Installation testé depuis la barre latérale : page complète, tableaux et blocs de commandes correctement rendus. Aucun fichier du kit ou du moteur modifié.

## Resources

- [Wiki GitHub](https://github.com/leclerefrederic/kanban-rememory/wiki)
- [Historique de l’accueil](https://github.com/leclerefrederic/kanban-rememory/wiki/Home/_history)
- [Procédure d’installation](../../../../dist/INSTALL.md)
- [Guide utilisateur](../../../../kanban-rememory/documentation/guide.md)

## History

- Demande complémentaire de l’utilisateur : « Tu gardes notre style d’écriture hein :D C’est important :) ». Conserver le ton anglais incisif et accessible du README, avec humour et instructions précises.

- 2026-11-16T20:50:56+01:00 — Stage moved from `backlog` to `development`.

- 2026-11-16T20:55:43+01:00 — Stage moved from `development` to `completion`.

- 2026-11-16T20:55:43+01:00 — Merge approved for the verified candidate `f4c75dfe662c3cacd7e7e081eb518b9ac9dd63f8`: “Vas y fait le alors :)”.
