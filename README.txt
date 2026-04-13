====================================================
  SAHELSOUND RECORDS — Projet Python L2 Informatique
  Année 2025-2026
====================================================

MEMBRES DU GROUPE
-----------------
1. [Prénom NOM]          - Rôle : Chef de projet / main.py
2. [Prénom NOM]          - Rôle : Module label.py (logique métier)
3. [Prénom NOM]          - Rôle : Module analyse.py (statistiques Pandas)
4. [Prénom NOM]          - Rôle : Tests & intégration / README
5. [Prénom NOM]          - Rôle : (si groupe de 5)

>> Remplacez les crochets par vos vrais noms et prénoms <<

EXTENSION CHOISIE
-----------------
[ ] Visualisation matplotlib (graphique streams par genre → PNG)
[ ] Recherche avancée (genre + pays + année minimale)
[ ] Historique (journalisation dans historique.log)
[ ] Aucune extension

>> Cochez l'extension choisie par le groupe (une seule) <<

DESCRIPTION DU PROJET
----------------------
Application console de gestion du catalogue du label musical fictif
SahelSound Records. Permet de consulter, ajouter et analyser les
artistes et leurs albums via un menu interactif.

FICHIERS INCLUS
---------------
- main.py          : Point d'entrée, menu principal et sous-menus
- label.py         : Fonctions de gestion du catalogue (chargement,
                     sauvegarde, ajout, recherche)
- analyse.py       : Analyse statistique avec Pandas, export CSV
- catalogue.json   : Données persistantes du catalogue (12 artistes)
- rapport.csv      : Rapport généré par le module analyse (option 4b)
- README.txt       : Ce fichier

INSTRUCTIONS D'EXÉCUTION
-------------------------
1. Installer les dépendances :
       pip install pandas

2. Lancer l'application :
       python main.py

3. Naviguer dans les menus en entrant le chiffre ou la lettre correspondante.

STRUCTURE DES MENUS
-------------------
  1. Consulter le catalogue
       a. Afficher tous les artistes
       b. Rechercher par nom ou genre
       c. Détail d'un artiste
  2. Ajouter un artiste
  3. Ajouter un album à un artiste existant
  4. Statistiques et rapport
       a. Afficher toutes les statistiques
       b. Exporter le rapport en CSV
  5. Quitter

====================================================
