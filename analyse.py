"""
analyse.py - Module d'analyse statistique pour SahelSound Records
Utilise Pandas pour produire des rapports et les exporter en CSV.
"""

import json
import pandas as pd


def charger_en_dataframe(chemin):
    """
    Charge le catalogue JSON et l'aplatit en DataFrame Pandas.
    Chaque ligne représente un album avec les infos de son artiste.

    Args:
        chemin (str): Chemin vers catalogue.json

    Returns:
        pd.DataFrame: DataFrame avec colonnes :
                      id, nom, genre, pays, titre, annee, streams
    """
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")

    lignes = []
    for artiste in data:
        for album in artiste.get("albums", []):
            lignes.append({
                "id": artiste["id"],
                "nom": artiste["nom"],
                "genre": artiste["genre"],
                "pays": artiste["pays"],
                "titre": album["titre"],
                "annee": album["annee"],
                "streams": album["streams"],
            })

    return pd.DataFrame(lignes)


def top5_artistes_streams(df):
    """
    Retourne le top 5 des artistes par nombre total de streams.

    Args:
        df (pd.DataFrame): DataFrame aplati des albums

    Returns:
        pd.DataFrame: Top 5 avec colonnes 'nom' et 'total_streams'
    """
    top = (
        df.groupby("nom")["streams"]
        .sum()
        .reset_index()
        .rename(columns={"streams": "total_streams"})
        .sort_values("total_streams", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    top.index += 1
    return top


def moyenne_streams_par_genre(df):
    """
    Calcule la moyenne des streams par genre musical.

    Args:
        df (pd.DataFrame): DataFrame aplati des albums

    Returns:
        pd.DataFrame: Moyenne des streams par genre, trié décroissant
    """
    moyenne = (
        df.groupby("genre")["streams"]
        .mean()
        .round(0)
        .astype(int)
        .reset_index()
        .rename(columns={"streams": "moyenne_streams"})
        .sort_values("moyenne_streams", ascending=False)
        .reset_index(drop=True)
    )
    return moyenne


def albums_par_annee(df):
    """
    Agrège le nombre d'albums sortis par année.

    Args:
        df (pd.DataFrame): DataFrame aplati des albums

    Returns:
        pd.DataFrame: Nombre d'albums par année, trié chronologiquement
    """
    par_annee = (
        df.groupby("annee")["titre"]
        .count()
        .reset_index()
        .rename(columns={"titre": "nb_albums"})
        .sort_values("annee")
        .reset_index(drop=True)
    )
    return par_annee


def exporter_rapport(chemin_json, chemin_csv):
    """
    Génère un rapport complet et l'exporte dans un fichier CSV.
    Le rapport contient : top 5, moyenne par genre, albums par année.

    Args:
        chemin_json (str): Chemin vers catalogue.json
        chemin_csv (str): Chemin du fichier CSV à créer

    Returns:
        str: Message de confirmation avec le chemin du fichier créé
    """
    df = charger_en_dataframe(chemin_json)

    top5 = top5_artistes_streams(df).reset_index()
    top5.columns = ["Rang", "Artiste", "Total Streams"]
    top5["Section"] = "Top 5 artistes"

    genres = moyenne_streams_par_genre(df)
    genres.columns = ["Artiste", "Total Streams"]
    genres["Rang"] = ""
    genres["Section"] = "Moyenne streams par genre"
    genres = genres[["Rang", "Artiste", "Total Streams", "Section"]]

    par_an = albums_par_annee(df)
    par_an.columns = ["Artiste", "Total Streams"]
    par_an["Rang"] = ""
    par_an["Section"] = "Albums par année"
    par_an = par_an[["Rang", "Artiste", "Total Streams", "Section"]]

    rapport = pd.concat([top5, genres, par_an], ignore_index=True)

    rapport.to_csv(chemin_csv, index=False, encoding="utf-8-sig")
    return f"Rapport exporté avec succès : {chemin_csv}"


def afficher_stats(chemin_json):
    """
    Affiche toutes les statistiques dans la console.

    Args:
        chemin_json (str): Chemin vers catalogue.json
    """
    df = charger_en_dataframe(chemin_json)

    print("\n" + "=" * 50)
    print("  TOP 5 ARTISTES PAR STREAMS")
    print("=" * 50)
    top5 = top5_artistes_streams(df)
    for rang, row in top5.iterrows():
        print(f"  {rang}. {row['nom']:<25} {row['total_streams']:>12,} streams")

    print("\n" + "=" * 50)
    print("  MOYENNE DES STREAMS PAR GENRE")
    print("=" * 50)
    genres = moyenne_streams_par_genre(df)
    for _, row in genres.iterrows():
        print(f"  {row['genre']:<20} {row['moyenne_streams']:>12,} streams en moyenne")

    print("\n" + "=" * 50)
    print("  ALBUMS SORTIS PAR ANNÉE")
    print("=" * 50)
    par_an = albums_par_annee(df)
    for _, row in par_an.iterrows():
        barre = "█" * row["nb_albums"]
        print(f"  {int(row['annee'])} │ {barre} ({row['nb_albums']})")
