import sys
from label import (
    charger_catalogue,
    sauvegarder_catalogue,
    lister_artistes,
    rechercher_artiste,
    ajouter_artistes,
    ajouter_album,
    obtenir_detail_artiste
)
from analyse import (
    charger_et_aplatir,
    top5_albums,
    moyenne_par_genre,
    comptage_par_annee,
    exporter_csv

)


def main():
   
    chemin_json = "catalogue.json"
    chemin_csv  = "rapport.csv"

    print("\n  Bienvenue sur SahelSound Records")
    print("  Gestion du catalogue musical\n")

    try:
        catalogue = charger_catalogue(chemin_json)
    except Exception as e:
        print(f"  Erreur au chargement : {e}")
        sys.exit(1)

    while True:
        # ── MENU PRINCIPAL ──────────────────────────────
        print("\n" + "=" * 50)
        print("    SAHELSOUND RECORDS - CATALOGUE")
        print("=" * 50)
        print("  1. Consulter le catalogue")
        print("  2. Ajouter un artiste")
        print("  3. Ajouter un album a un artiste existant")
        print("  4. Statistiques et rapport")
        print("  5. Quitter")
        print("=" * 50)
        choix = input("Votre choix (1-5) : ").strip()

        #OPTION 1 : CONSULTER
        if choix == "1":
            while True:
                print("\n" + "-" * 45)
                print("  1. Consulter le catalogue")
                print("-" * 45)
                print("  a. Afficher tous les artistes")
                print("  b. Rechercher un artiste par nom ou genre")
                print("  c. Afficher le detail d'un artiste")
                print("  r. Retour au menu principal")
                print("-" * 45)
                choix1 = input("Votre choix : ").strip().lower()

                if choix1 == "a":
                    # Afficher tous les artistes
                    artistes = lister_artistes(catalogue)
                    if not artistes:
                        print("  Le catalogue est vide.")
                    else:
                        print()
                        print(f"  {'ID':<10} {'Nom':<25} {'Genre':<20} {'Pays':<15} {'Albums'}")
                        print("  " + "-" * 75)
                        for a in artistes:
                            print(f"  {a['id']:<10} {a['nom']:<25} {a['genre']:<20} {a['pays']:<15} {a['nb_albums']}")

                elif choix1 == "b":
                    # Rechercher par nom ou genre
                    print("\n  Rechercher par :")
                    print("    n. Nom")
                    print("    g. Genre")
                    c = input("  Votre choix : ").strip().lower()
                    if c == "n":
                        critere = "nom"
                    elif c == "g":
                        critere = "genre"
                    else:
                        print("  Choix invalide.")
                        continue
                    valeur = input(f"  Valeur a rechercher ({critere}) : ").strip()
                    try:
                        resultats = rechercher_artiste(catalogue, critere, valeur)
                        if not resultats:
                            print("  Aucun artiste trouve.")
                        else:
                            print(f"\n  {len(resultats)} resultat(s) :")
                            for a in resultats:
                                print(f"  [{a['id']}] {a['nom']} - {a['genre']} ({a['pays']})")
                    except ValueError as e:
                        print(f"  Erreur : {e}")

                elif choix1 == "c":
                    # Afficher le detail d'un artiste
                    id_artiste = input("  Entrez l'ID de l'artiste (ex: ART-001) : ").strip().upper()
                    try:
                        artiste = obtenir_detail_artiste(catalogue, id_artiste)
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
                    except ValueError as e:
                        print(f"  Erreur : {e}")

                elif choix1 == "r":
                    break
                else:
                    print("  Choix invalide. Entrez a, b, c ou r.")

        # OPTION 2 : AJOUTER UN ARTISTE 
        elif choix == "2":
            while True:
                print("\n" + "-" * 45)
                print("  2. Ajouter un artiste")
                print("-" * 45)
                print("  a. Saisir et ajouter un nouvel artiste")
                print("  r. Retour au menu principal")
                print("-" * 45)
                choix2 = input("Votre choix : ").strip().lower()

                if choix2 == "a":
                    # Saisir les informations de l'artiste
                    try:
                        id_artiste = input("  ID de l'artiste (ex: ART-013) : ").strip().upper()
                        nom        = input("  Nom de scene                  : ").strip()
                        genre      = input("  Genre musical                 : ").strip()
                        pays       = input("  Pays d'origine                : ").strip()
                        nouvel_artiste = {
                            "id": id_artiste, "nom": nom,
                            "genre": genre, "pays": pays, "albums": []
                        }
                        catalogue = ajouter_artistes(catalogue, nouvel_artiste)
                        sauvegarder_catalogue(catalogue, chemin_json)
                        print(f"  Artiste '{nom}' ajoute et catalogue sauvegarde.")
                    except ValueError as e:
                        print(f"  Erreur : {e}")

                elif choix2 == "r":
                    break
                else:
                    print("  Choix invalide. Entrez a ou r.")

        # OPTION 3 : AJOUTER UN ALBUM 
        elif choix == "3":
            while True:
                print("\n" + "-" * 45)
                print("  3. Ajouter un album a un artiste existant")
                print("-" * 45)
                print("  a. Ajouter un album")
                print("  b. Afficher la liste des IDs disponibles")
                print("  r. Retour au menu principal")
                print("-" * 45)
                choix3 = input("Votre choix : ").strip().lower()

                if choix3 == "a":
                    # Saisir les informations de l'album
                    try:
                        id_artiste = input("  ID de l'artiste cible : ").strip().upper()
                        titre      = input("  Titre de l'album      : ").strip()
                        annee      = input("  Annee de sortie       : ").strip()
                        streams    = input("  Nombre de streams     : ").strip()
                        album = {"titre": titre, "annee": int(annee), "streams": int(streams)}
                        catalogue = ajouter_album(catalogue, id_artiste)
                        sauvegarder_catalogue(catalogue, chemin_json)
                        print(f"  Album '{titre}' ajoute et catalogue sauvegarde.")
                    except ValueError as e:
                        print(f"  Erreur : {e}")

                elif choix3 == "b":
                    artistes = lister_artistes(catalogue)
                    print(f"\n  {'ID':<10} {'Nom':<25}")
                    print("  " + "-" * 35)
                    for a in artistes:
                        print(f"  {a['id']:<10} {a['nom']:<25}")

                elif choix3 == "r":
                    break
                else:
                    print("  Choix invalide. Entrez a, b ou r.")

        #  OPTION 4 : STATISTIQUES 
        elif choix == "4":
            while True:
                #catalogue_pandas=charger_et_aplatir("catalogue.json")
                print("\n" + "-" * 45)
                print("  4. Statistiques et rapport")
                print("-" * 45)
                print("  a. Top 5 artistes par streams")
                print("  b. Moyenne des streams par genre")
                print("  c. Nombre d'albums sortis par annee")
                print("  d. Exporter le rapport complet en CSV")
                print("  r. Retour au menu principal")
                print("-" * 45)
                choix4 = input("Votre choix : ").strip().lower()

                if choix4 =="a":

                    try:
                        five_artistes=top5_albums(catalogue)
                        print(f"les 5 artistes par streams sont :{five_artistes}\n")
                    except Exception as e:
                        print(f"  Erreur : {e}")
                elif choix4 =="b":
                    try:
                        moyenne_g=moyenne_par_genre(catalogue)
                        print(f"la moyenne des streams par genre est :{moyenne_g}\n")
                    except Exception as e:
                        print(f"  Erreur : {e}")
                elif choix4 =="c":
                    try:
                        albums_annee=comptage_par_annee(catalogue)
                        print(f"le nombre d,albums sorties par annee est :{albums_annee}\n")
                    except Exception as e:
                        print(f"  Erreur : {e}")

                elif choix4 == "d":
                    try:
                        message = exporter_csv(catalogue, chemin_csv)
                        print(f"  {message}")
                    except Exception as e:
                        print(f"  Erreur : {e}")

                elif choix4 == "r":
                    break
                else:
                    print("  Choix invalide. Entrez a, b, c, d ou r.")

        #  OPTION 5 : QUITTER 
        elif choix == "5":
            print("\n  Au revoir et bonne ecoute !\n")
            break

        else:
            print("  Choix invalide. Entrez un nombre entre 1 et 5.")


if __name__ == "__main__":
    main()