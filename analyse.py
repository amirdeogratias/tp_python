import json
import pandas as pd
def charger_catalogue(chemin: str = "catalogue.json") -> pd.DataFrame:
    with open(chemin, "r", encoding="utf-8") as f:
        artistes = json.load(f)
    
    #Applatissement avec une liste par album
    lignes = []
    for artistes in lignes:
        for albums in artistes.get("albums", []):
            lignes.append({
                "artiste_id": artistes.get("id"),
                "nom": artistes.get("nom"),
                "genre": artistes.get("genre"),
                "pays": artistes.get("pays"),
                "album_titre": albums.get("titre"),
                "album_annee": albums.get("annee"),
                "album_streams": albums.get("streams", 0)
            })
    df = pd.DataFrame(lignes)

    #Typage explicite
    if not df.empty:
        df["album_annee"] = pd.to_numeric(df["album_annee"], errors="coerce").astype("Int64")
        df["album_streams"] = pd.to_numeric(df["album_streams"], errors="coerce").fillna(0).astype(int)

    return df


#Top 5 artistes par nombres total de streams
def top5_artistes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retourne les 5 artistes ayant le plus grand nombre total de streams.
 
    Colonnes : nom, genre, pays, total_streams
    """
    resultat = (
        df.groupby(["artiste_id", "nom", "genre", "pays"], as_index=False)["album_streams"]
        .sum()
        .rename(columns={"album_streams": "total_streams"})
        .sort_values("total_streams", ascending=False)
        .head(5)
        .reset_index(drop=True)
    )
    resultat.index += 1  # classement à partir de 1
    return resultat

# 3. MOYENNE DES STREAMS PAR GENRE
 
def moyenne_streams_par_genre(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la moyenne des streams par album pour chaque genre musical.
 
    Colonnes : genre, moyenne_streams
    """
    resultat = (
        df.groupby("genre", as_index=False)["album_streams"]
        .mean()
        .rename(columns={"album_streams": "moyenne_streams"})
        .sort_values("moyenne_streams", ascending=False)
        .reset_index(drop=True)
    )
    resultat["moyenne_streams"] = resultat["moyenne_streams"].round(0).astype(int)
    return resultat

# 4. NOMBRE D'ALBUMS PAR ANNÉE
 
def albums_par_annee(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrège le nombre d'albums sortis par année.
 
    Colonnes : annee, nombre_albums
    """
    resultat = (
        df.dropna(subset=["album_annee"])  # exclure les années inconnues
        .groupby("album_annee", as_index=False)["album_titre"]
        .count()
        .rename(columns={"album_annee": "annee", "album_titre": "nombre_albums"})
        .sort_values("annee")
        .reset_index(drop=True)
    )
    return resultat

# 5. EXPORT DU RAPPORT COMPLET EN CSV
 
def exporter_rapport(df: pd.DataFrame, chemin_csv: str = "rapport.csv") -> None:
    """
    Génère rapport.csv avec les quatre sections d'analyse :
        - Top 5 artistes par streams
        - Moyenne des streams par genre
        - Nombre d'albums par année
        - Détail complet du catalogue (aplati)
 
    Encodage UTF-8 BOM pour compatibilité Excel/LibreOffice.
    """
    separateur = "\n"  # ligne vide entre sections
 
    with open(chemin_csv, "w", encoding="utf-8-sig", newline="") as f:
 
        # --- Section 1 ---
        f.write("=== TOP 5 ARTISTES PAR STREAMS TOTAUX ===\n")
        top5_artistes(df).to_csv(f, index=True, sep=",")
        f.write(separateur)
 
        # --- Section 2 ---
        f.write("=== MOYENNE DES STREAMS PAR GENRE ===\n")
        moyenne_streams_par_genre(df).to_csv(f, index=False, sep=",")
        f.write(separateur)
 
        # --- Section 3 ---
        f.write("=== NOMBRE D'ALBUMS PAR ANNEE ===\n")
        albums_par_annee(df).to_csv(f, index=False, sep=",")
        f.write(separateur)
 
        # --- Section 4 ---
        f.write("=== CATALOGUE COMPLET (DETAIL PAR ALBUM) ===\n")
        df.to_csv(f, index=False, sep=",")

 
 
