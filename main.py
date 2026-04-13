import sys


def menu_principal():
    """Affiche le menu principal de l'application."""
    sep = "=" * 55
    print("\n" + sep)
    print("    SAHELSOUND RECORDS - CATALOGUE")
    print(sep)
    print("  1. Consulter le catalogue")
    print("  2. Ajouter un artiste")
    print("  3. Ajouter un album a un artiste existant")
    print("  4. Statistiques et rapport")
    print("  5. Quitter")
    print(sep)


def menu_consulter(catalogue):
    """
    Sous-menu pour consulter le catalogue.

    Args:
        catalogue (list): Liste des artistes chargee en memoire.
    """
    from label import rechercher_artiste, lister_artistes, afficher_detail_artiste
    while True:
        print("\n" + "-" * 45)
        print("  1. Consulter le catalogue")
        print("-" * 45)
        print("  a. Afficher tous les artistes")
        print("  b. Rechercher un artiste par nom ou genre")
        print("  c. Afficher le detail d'un artiste")
        print("  r. Retour au menu principal")
        print("-" * 45)
        choix = input("Votre choix : ").strip().lower()
        if choix == "a":
            afficher_artistes(catalogue, lister_artistes)
        elif choix == "b":
            rechercher_artiste(catalogue, rechercher_artiste)
        elif choix == "c":
            afficher_detail(catalogue, afficher_detail_artiste)
        elif choix == "r":
            break
        else:
            print("  Choix invalide. Entrez a, b, c ou r.")


def afficher_artistes(catalogue, fn_lister):
    """
    Affiche tous les artistes avec nom, genre, pays et nombre d'albums.

    Args:
        catalogue (list): Liste des artistes.
        fn_lister (callable): Fonction lister_artistes de label.py.
    """
    artistes = fn_lister(catalogue)
    if not artistes:
        print("  Le catalogue est vide.")
        return
    print()
    print(f"  {'ID':<10} {'Nom':<25} {'Genre':<20} {'Pays':<15} {'Albums'}")
    print("  " + "-" * 75)
    for a in artistes:
        print(f"  {a['id']:<10} {a['nom']:<25} {a['genre']:<20} {a['pays']:<15} {a['nb_albums']}")


def rechercher_artiste(catalogue, fn_rechercher):
    """
    Recherche un artiste par nom ou par genre.

    Args:
        catalogue (list): Liste des artistes.
        fn_rechercher (callable): Fonction rechercher_artiste de label.py.
    """
    print("\n  Rechercher par :")
    print("    n. Nom")
    print("    g. Genre")
    choix = input("  Votre choix : ").strip().lower()
    if choix == "n":
        critere = "nom"
    elif choix == "g":
        critere = "genre"
    else:
        print("  Choix invalide.")
        return
    valeur = input(f"  Valeur a rechercher ({critere}) : ").strip()
    try:
        resultats = fn_rechercher(catalogue, critere, valeur)
    except ValueError as e:
        print(f"  Erreur : {e}")
        return
    if not resultats:
        print("  Aucun artiste trouve.")
    else:
        print(f"\n  {len(resultats)} resultat(s) :")
        for a in resultats:
            print(f"  [{a['id']}] {a['nom']} - {a['genre']} ({a['pays']})")


def afficher_detail(catalogue, fn_detail):
    """
    Affiche le detail complet d'un artiste et la liste de ses albums.

    Args:
        catalogue (list): Liste des artistes.
        fn_detail (callable): Fonction afficher_detail_artiste de label.py.
    """
    id_ou_nom = input("  Entrez l'ID ou le nom de l'artiste : ").strip()
    artiste = fn_detail(catalogue, id_ou_nom)
    if not artiste:
        print("  Artiste introuvable.")
        return
    print()
    print("  " + "=" * 50)
    print(f"  Artiste : {artiste['nom']}  [{artiste['id']}]")
    print(f"  Genre   : {artiste['genre']}")
    print(f"  Pays    : {artiste['pays']}")
    print("  " + "-" * 50)
    albums = artiste.get("albums", [])
    if not albums:
        print("  Aucun album enregistre.")
    else:
        print(f"  {'Titre':<32} {'Annee':<8} {'Streams':>12}")
        print("  " + "-" * 54)
        for alb in albums:
            print(f"  {alb['titre']:<32} {alb['annee']:<8} {alb['streams']:>12,}")
    print("  " + "=" * 50)


def menu_ajouter_artiste(catalogue, chemin_json):
    """
    Sous-menu pour saisir et ajouter un nouvel artiste.

    Args:
        catalogue (list): Liste des artistes.
        chemin_json (str): Chemin vers le fichier catalogue.json.

    Returns:
        list: Catalogue mis a jour.
    """
    from label import ajouter_artiste, sauvegarder_catalogue, lister_artistes
    while True:
        print("\n" + "-" * 45)
        print("  2. Ajouter un artiste")
        print("-" * 45)
        print("  a. Saisir et ajouter un nouvel artiste")
        print("  r. Retour au menu principal")
        print("-" * 45)
        choix = input("Votre choix : ").strip().lower()
        if choix == "a":
            catalogue = saisir_artiste(
                catalogue, chemin_json, ajouter_artiste, sauvegarder_catalogue
            )
        elif choix == "r":
            break
        else:
            print("  Choix invalide. Entrez a ou r.")
    return catalogue


def saisir_artiste(catalogue, chemin_json, fn_ajouter, fn_sauvegarder):
    """
    Saisie au clavier et ajout d'un nouvel artiste dans le catalogue.

    Args:
        catalogue (list): Liste des artistes.
        chemin_json (str): Chemin vers catalogue.json.
        fn_ajouter (callable): Fonction ajouter_artiste de label.py.
        fn_sauvegarder (callable): Fonction sauvegarder_catalogue de label.py.

    Returns:
        list: Catalogue mis a jour.
    """
    print("\n  --- Saisie du nouvel artiste ---")
    try:
        id_artiste = input("  ID de l'artiste (ex: ART-013) : ").strip().upper()
        nom        = input("  Nom de scene                  : ").strip()
        genre      = input("  Genre musical                 : ").strip()
        pays       = input("  Pays d'origine                : ").strip()
        nouvel_artiste = {"id": id_artiste, "nom": nom, "genre": genre, "pays": pays, "albums": []}
        catalogue = fn_ajouter(catalogue, nouvel_artiste)
        fn_sauvegarder(catalogue, chemin_json)
        print(f"  Artiste '{nom}' ajoute et catalogue sauvegarde.")
    except ValueError as e:
        print(f"  Erreur : {e}")
    return catalogue


def ajouter_album(catalogue, chemin_json):
    """
    Sous-menu pour ajouter un album a un artiste existant.

    Args:
        catalogue (list): Liste des artistes.
        chemin_json (str): Chemin vers le fichier catalogue.json.

    Returns:
        list: Catalogue mis a jour.
    """
    from label import ajouter_album, sauvegarder_catalogue, lister_artistes
    while True:
        print("\n" + "-" * 45)
        print("  3. Ajouter un album a un artiste existant")
        print("-" * 45)
        print("  a. Ajouter un album (saisie de l'ID artiste)")
        print("  b. Afficher la liste des IDs disponibles")
        print("  r. Retour au menu principal")
        print("-" * 45)
        choix = input("Votre choix : ").strip().lower()
        if choix == "a":
            catalogue = saisir_album(
                catalogue, chemin_json, ajouter_album, sauvegarder_catalogue
            )
        elif choix == "b":
            afficher_artistes(catalogue, lister_artistes)
        elif choix == "r":
            break
        else:
            print("  Choix invalide. Entrez a, b ou r.")
    return catalogue


def saisir_album(catalogue, chemin_json, fn_ajouter_album, fn_sauvegarder):
    """
    Saisie au clavier et ajout d'un album a un artiste existant.

    Args:
        catalogue (list): Liste des artistes.
        chemin_json (str): Chemin vers catalogue.json.
        fn_ajouter_album (callable): Fonction ajouter_album de label.py.
        fn_sauvegarder (callable): Fonction sauvegarder_catalogue de label.py.

    Returns:
        list: Catalogue mis a jour.
    """
    print("\n  --- Saisie du nouvel album ---")
    try:
        id_artiste = input("  ID de l'artiste cible : ").strip().upper()
        titre      = input("  Titre de l'album      : ").strip()
        annee      = input("  Annee de sortie       : ").strip()
        streams    = input("  Nombre de streams     : ").strip()
        album = {"titre": titre, "annee": annee, "streams": streams}
        catalogue = fn_ajouter_album(catalogue, id_artiste, album)
        fn_sauvegarder(catalogue, chemin_json)
        print(f"  Album '{titre}' ajoute et catalogue sauvegarde.")
    except ValueError as e:
        print(f"  Erreur : {e}")
    return catalogue


def statistiques(chemin_json, chemin_csv):
    """
    Sous-menu pour afficher les statistiques et exporter le rapport.

    Args:
        chemin_json (str): Chemin vers catalogue.json.
        chemin_csv (str): Chemin vers le fichier rapport.csv a generer.
    """
    while True:
        print("\n" + "-" * 45)
        print("  4. Statistiques et rapport")
        print("-" * 45)
        print("  a. Top 5 artistes par streams")
        print("  b. Moyenne des streams par genre")
        print("  c. Nombre d'albums sortis par annee")
        print("  d. Exporter le rapport complet en CSV")
        print("  r. Retour au menu principal")
        print("-" * 45)
        choix = input("Votre choix : ").strip().lower()
        if choix == "a":
            top5(chemin_json)
        elif choix == "b":
            moyenne_genre_musical(chemin_json)
        elif choix == "c":
            albums_annee(chemin_json)
        elif choix == "d":
            exporter_rapport(chemin_json, chemin_csv)
        elif choix == "r":
            break
        else:
            print("  Choix invalide. Entrez a, b, c, d ou r.")


def top5(chemin_json):
    """
    Charge les donnees et affiche le top 5 artistes par streams totaux.

    Args:
        chemin_json (str): Chemin vers catalogue.json.
    """
    from analyse import charger_en_dataframe, top5_artistes_streams
    try:
        df  = charger_en_dataframe(chemin_json)
        top = top5_artistes_streams(df)
        print("\n  --- Top 5 artistes par nombre total de streams ---")
        print(f"  {'Rang':<6} {'Artiste':<25} {'Total Streams':>15}")
        print("  " + "-" * 48)
        for rang, row in top.iterrows():
            print(f"  {rang:<6} {row['nom']:<25} {row['total_streams']:>15,}")
    except FileNotFoundError as e:
        print(f"  Erreur fichier : {e}")
    except Exception as e:
        print(f"  Erreur : {e}")


def moyenne_genre_musical(chemin_json):
    """
    Charge les donnees et affiche la moyenne des streams par genre musical.

    Args:
        chemin_json (str): Chemin vers catalogue.json.
    """
    from analyse import charger_en_dataframe, moyenne_streams_par_genre
    try:
        df      = charger_en_dataframe(chemin_json)
        moyenne = moyenne_streams_par_genre(df)
        print("\n  --- Moyenne des streams par genre musical ---")
        print(f"  {'Genre':<22} {'Moyenne Streams':>15}")
        print("  " + "-" * 40)
        for _, row in moyenne.iterrows():
            print(f"  {row['genre']:<22} {row['moyenne_streams']:>15,}")
    except FileNotFoundError as e:
        print(f"  Erreur fichier : {e}")
    except Exception as e:
        print(f"  Erreur : {e}")


def albums_annee(chemin_json):
    """
    Charge les donnees et affiche le nombre d'albums sortis par annee.

    Args:
        chemin_json (str): Chemin vers catalogue.json.
    """
    from analyse import charger_en_dataframe, albums_par_annee
    try:
        df     = charger_en_dataframe(chemin_json)
        par_an = albums_par_annee(df)
        print("\n  --- Albums sortis par annee ---")
        print(f"  {'Annee':<8} {'Nb Albums':<12} {'Graphique'}")
        print("  " + "-" * 40)
        for _, row in par_an.iterrows():
            barre = "=" * int(row["nb_albums"])
            print(f"  {int(row['annee']):<8} {int(row['nb_albums']):<12} {barre}")
    except FileNotFoundError as e:
        print(f"  Erreur fichier : {e}")
    except Exception as e:
        print(f"  Erreur : {e}")


def exporter_rapport(chemin_json, chemin_csv):
    """
    Exporte le rapport complet en fichier CSV.

    Args:
        chemin_json (str): Chemin vers catalogue.json.
        chemin_csv (str): Chemin du fichier rapport.csv a creer.
    """
    from analyse import exporter_rapport
    try:
        message = exporter_rapport(chemin_json, chemin_csv)
        print(f"  {message}")
    except FileNotFoundError as e:
        print(f"  Erreur fichier : {e}")
    except Exception as e:
        print(f"  Erreur lors de l'export : {e}")


def main():
    """
    Boucle principale de l'application SahelSound Records.
    Les chemins de fichiers sont definis ici et passes en parametre
    aux fonctions — aucune variable globale.
    """
    from label import charger_catalogue

    chemin_json = "catalogue.json"
    chemin_csv  = "rapport.csv"

    print("\n  Bienvenue sur SahelSound Records")
    print("  Gestion du catalogue musical\n")

    try:
        catalogue = charger_catalogue(chemin_json)
    except FileNotFoundError:
        print(f"  Fichier '{chemin_json}' introuvable. Catalogue vide cree.")
        catalogue = []
    except Exception as e:
        print(f"  Erreur au chargement : {e}")
        sys.exit(1)

    while True:
        menu_principal()
        choix = input("Votre choix (1-5) : ").strip()
        if choix == "1":
            menu_consulter(catalogue)
        elif choix == "2":
            catalogue = menu_ajouter_artiste(catalogue, chemin_json)
        elif choix == "3":
            catalogue = ajouter_album(catalogue, chemin_json)
        elif choix == "4":
            statistiques(chemin_json, chemin_csv)
        elif choix == "5":
            print("\n  Au revoir et bonne ecoute !\n")
            break
        else:
            print("  Choix invalide. Entrez un nombre entre 1 et 5.")


if __name__ == "__main__":
    main()