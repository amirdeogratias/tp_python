import json
import pandas as pd
def charger_catalogue_pd(chemin:str) -> pd.DataFrame:
    #création du dataframe
    df=pd.read_json(chemin)
    #aplatir les lignes par albums
    
    df = df.explode("albums").reset_index(drop=True)
    #extraire les champs de chaque album
    
    albums_df=pd.json_normalize(df["albums"])
    #fusionner infos artistes+infos albums
    df=df.drop(columns=["albums"])
    df=pd.concat([df,albums_df],axis=1)
    return df


#Top 5 artistes par nombres total de streams
def top5_artistes(df: pd.DataFrame) :
   
    #Retourne les 5 artistes ayant le plus grand nombre total de streams.
 
    if df.empty :
        return[]
    resultat = (
        df.groupby("nom")["streams"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    resultat.columns=["nom","streams_total"]
    resultat.index += 1  # classement à partir de 1
    return resultat

#  MOYENNE DES STREAMS PAR GENRE
 
def moyenne_streams_par_genre(df: pd.DataFrame) -> pd.DataFrame:
    
    #Calcule la moyenne des streams par album pour chaque genre musical.
    if df.empty :
        return[]
    moyenne = (
        df.groupby("genre")["streams"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    moyenne.columns=["genre","streams_moyenne"]
    return moyenne

# 4. NOMBRE D'ALBUMS PAR ANNÉE
 
def albums_par_annee(df: pd.DataFrame) -> pd.DataFrame:
    
   # Agrège le nombre d'albums sortis par année.
    if df.empty :
        return[]
    
    resultat = (
        df.dropna(subset=["annee"])  # exclure les années inconnues
        .groupby("annee")["titre"]
        .count()
        .sort_values(ascending=False)
        .reset_index()
    )
    resultat.columns=["annee","nb_d'albums"]
    resultat["annee"]=resultat["annee"].astype(int)
    return resultat

# 5. EXPORT DU RAPPORT COMPLET EN CSV
 
def exporter_rapport(df: pd.DataFrame, chemin_csv: str = "rapport.csv") -> None:
    
    #Génère rapport.csv avec les quatre sections d'analyse :
       
 
    #Encodage UTF-8 BOM pour compatibilité Excel/LibreOffice.
    separateur= "\n"+"-"*30+"\n"
 
    with open(chemin_csv, "w", encoding="utf-8-sig", newline="") as f:
 
        #section1
        f.write("TOP 5 ARTISTES PAR STREAMS TOTAUX \n")
        top5_artistes(df).to_csv(f, index=True, sep=",")
        f.write(separateur)
 
        #section2
        f.write(" MOYENNE DES STREAMS PAR GENRE \n")
        moyenne_streams_par_genre(df).to_csv(f, index=False, sep=",")
        f.write(separateur)
 
        #  Section 3 
        f.write(" NOMBRE D'ALBUMS PAR ANNEE \n")
        albums_par_annee(df).to_csv(f, index=False, sep=",")
        f.write(separateur)
 
        #  Section 4 
        f.write(" CATALOGUE COMPLET (DETAIL PAR ALBUM) \n")
        df.to_csv(f, index=False, sep=",")

 
 
