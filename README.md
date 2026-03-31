# tiki-taka-helper
Tiki-Taka Helper est une solution technique hybride (Extension Chrome + API Python) conçue pour aider les joueurs de jeux de réflexion footballistiques comme le Footy Tic-Tac-Toe ou le Tiki-Taka-Toe.  L'objectif est de trouver instantanément des joueurs "intersections" qui répondent à deux critères simultanés

Le projet repose sur trois piliers technologiques :

    Le Moteur d'Analyse (Backend Python / Pandas) :

        Utilise la puissance de la bibliothèque pandas pour traiter des fichiers CSV massifs (plusieurs millions de lignes pour les feuilles de match).

        Gère une API locale avec Flask pour répondre aux requêtes de l'extension.

        Algorithme : Il calcule l'intersection de deux ensembles d'IDs de joueurs filtrés par club ou par pays.

    L'Interface Utilisateur (Frontend Extension Chrome) :

        Une fenêtre contextuelle (Popup) développée en HTML5/CSS3.

        Un script JavaScript asynchrone (fetch) qui communique en temps réel avec le serveur local.

        Système d'autocomplétion dynamique pour éviter les erreurs de saisie sur les noms de clubs.

    La Base de Données (Dataset Kaggle) :

        Exploitation du dataset Football Data from Transfermarkt (par David Cariboo).

        Fichiers utilisés : players.csv (infos joueurs), clubs.csv (noms des clubs) et appearances.csv (historique des matchs pour lier joueurs et clubs).
