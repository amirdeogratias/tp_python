import json
import pandas as pd
def charger_catalogue(catalogue:list) -> pd.DataFrame:
    #création du dataframe
    df=pd.DataFrame(catalogue)
    #aplatir les lignes par albums
    df = df.explode("albums")
    #extraire les champs de chaque album
    albums_df=pd.json_normalize(df["albums"])
    return df


#Top 5 artistes par nombres total de streams
def top5_artistes(df: pd.DataFrame) :
   
    #Retourne les 5 artistes ayant le plus grand nombre total de streams.
 
    if df.empty :
        return[]
    resultat = (
        df.groupby("nom")["streams"]
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
    
    #Calcule la moyenne des streams par album pour chaque genre musical.
 
    resultat = (
        df.groupby("genre", as_index=False)["streams"]
        .mean()
        
    
        .sort_values(ascending=False)
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
        df.dropna(subset=["annee"])  # exclure les années inconnues
        .groupby("annee", as_index=False)["titre"]
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

 
 
