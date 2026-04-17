import json
import pandas as pd


def charger_et_aplatir(fichier):
    """Charge le JSON et retourne un DataFrame avec une ligne par album."""
    try:
        with open(fichier, "r", encoding="utf-8") as f:
            data = json.load(f)

        # On transforme la liste JSON en DataFrame (une ligne par artiste)
        df = pd.DataFrame(data)

        # explode() crée une ligne par album en répétant les infos de l'artiste
        df = df.explode("albums").reset_index(drop=True)

        # Chaque album est encore un dictionnaire, on l'éclate en colonnes
        # .tolist() garantit que les index sont bien alignés avant le concat
        albums_df = pd.json_normalize(df["albums"].tolist())

        # On assemble les infos artiste + infos album côte à côte
        df_final = pd.concat([
            df[["nom", "genre", "pays"]],
            albums_df
        ], axis=1)

        # Renommage pour plus de clarté
        df_final = df_final.rename(columns={"nom": "nom_artiste"})

        print(f"{len(df_final)} albums chargés.")
        return df_final

    except FileNotFoundError:
        print("Le fichier est introuvable.")
        return pd.DataFrame()

    except json.JSONDecodeError:
        print("Le fichier JSON est mal formaté.")
        return pd.DataFrame()


def top5_albums(df):
    """Retourne les 5 albums les plus streamés."""

    # sort_values trie du plus grand au plus petit, head(5) garde les 5 premiers
    top5 = df.sort_values("streams", ascending=False).head(5)

    print("\nTop 5 des albums les plus streamés :")
    for _, row in top5.iterrows():
        print(f"  {row['nom_artiste']} - {row['titre']} : {row['streams']:,} streams")

    return top5


def moyenne_par_genre(df):
    """Calcule la moyenne des streams par genre musical."""

    # groupby regroupe par genre, mean() calcule la moyenne des streams
    moyennes = df.groupby("genre")["streams"].mean().sort_values(ascending=False)

    print("\nMoyenne des streams par genre :")
    for genre, moy in moyennes.items():
        print(f"  {genre:<20} : {moy:>12,.0f} streams")

    return moyennes


def comptage_par_annee(df):
    """Compte le nombre d'albums sortis par année."""

    # size() compte le nombre de lignes par groupe d'année
    comptage = df.groupby("annee").size().sort_index()

    print("\nNombre d'albums par année :")
    for annee, nb in comptage.items():
        print(f"  {annee} : {nb} album(s)")

    return comptage


def exporter_csv(df, fichier):
    """Exporte le DataFrame en CSV en gardant les accents."""
    try:
        # utf-8-sig évite les problèmes d'accents à l'ouverture sur Excel
        df.to_csv(fichier, index=False, encoding="utf-8-sig")
        print(f"\nFichier '{fichier}' exporté avec succès ({len(df)} lignes).")

    except PermissionError:
        print(f"Impossible d'écrire '{fichier}' : permission refusée.")

    except Exception as e:
        print(f"Erreur lors de l'export : {e}")


if __name__ == "__main__":

    df = charger_et_aplatir("catalogue.json")

    if not df.empty:
        top5        = top5_albums(df)
        moyennes    = moyenne_par_genre(df)
        comptage    = comptage_par_annee(df)
        exporter_csv(df, "rapport.csv")