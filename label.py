"""
label.py - Module de logique métier pour SahelSound Records
Gère le chargement, la sauvegarde et la manipulation du catalogue.
"""

import json


def charger_catalogue(chemin):
    """
    Charge et retourne le catalogue depuis un fichier JSON.

    Args:
        chemin (str): Chemin vers le fichier catalogue.json

    Returns:
        list: Liste des artistes du catalogue

    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        json.JSONDecodeError: Si le fichier JSON est mal formé
    """
    try:
        with open(chemin, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier introuvable : {chemin}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Fichier JSON invalide : {e.msg}", e.doc, e.pos)


def sauvegarder_catalogue(data, chemin):
    """
    Écrit les données du catalogue dans un fichier JSON.

    Args:
        data (list): Liste des artistes à sauvegarder
        chemin (str): Chemin vers le fichier catalogue.json
    """
    try:
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        raise IOError(f"Impossible d'écrire dans le fichier : {e}")


def lister_artistes(catalogue):
    """
    Retourne la liste résumée des artistes (nom, genre, pays, nb albums).

    Args:
        catalogue (list): Liste complète des artistes

    Returns:
        list: Liste de dicts avec les infos résumées
    """
    return [
        {
            "id": artiste["id"],
            "nom": artiste["nom"],
            "genre": artiste["genre"],
            "pays": artiste["pays"],
            "nb_albums": len(artiste.get("albums", [])),
        }
        for artiste in catalogue
    ]


def rechercher_artiste(catalogue, critere, valeur):
    """
    Recherche des artistes par nom ou par genre (insensible à la casse).

    Args:
        catalogue (list): Liste des artistes
        critere (str): Champ de recherche : 'nom' ou 'genre'
        valeur (str): Valeur à rechercher

    Returns:
        list: Liste des artistes correspondants

    Raises:
        ValueError: Si le critère n'est pas 'nom' ou 'genre'
    """
    if critere not in ("nom", "genre"):
        raise ValueError("Le critère doit être 'nom' ou 'genre'.")
    valeur_lower = valeur.strip().lower()
    return [
        a for a in catalogue
        if valeur_lower in a.get(critere, "").lower()
    ]


def ajouter_artiste(catalogue, artiste):
    """
    Ajoute un artiste au catalogue après validation de l'identifiant.

    Args:
        catalogue (list): Liste des artistes existants
        artiste (dict): Nouvel artiste à ajouter

    Returns:
        list: Catalogue mis à jour

    Raises:
        ValueError: Si l'identifiant existe déjà ou si des champs sont manquants
    """
    champs_requis = ("id", "nom", "genre", "pays")
    for champ in champs_requis:
        if champ not in artiste or not str(artiste[champ]).strip():
            raise ValueError(f"Champ obligatoire manquant ou vide : '{champ}'")

    ids_existants = {a["id"] for a in catalogue}
    if artiste["id"] in ids_existants:
        raise ValueError(f"L'identifiant '{artiste['id']}' existe déjà.")

    if "albums" not in artiste:
        artiste["albums"] = []

    catalogue.append(artiste)
    return catalogue


def ajouter_album(catalogue, id_artiste, album):
    """
    Ajoute un album à un artiste existant identifié par son ID.

    Args:
        catalogue (list): Liste des artistes
        id_artiste (str): Identifiant de l'artiste cible
        album (dict): Album à ajouter (titre, annee, streams)

    Returns:
        list: Catalogue mis à jour

    Raises:
        ValueError: Si l'artiste est introuvable ou si les champs album sont invalides
    """
    champs_requis = ("titre", "annee", "streams")
    for champ in champs_requis:
        if champ not in album:
            raise ValueError(f"Champ album manquant : '{champ}'")

    for artiste in catalogue:
        if artiste["id"] == id_artiste:
            try:
                album["annee"] = int(album["annee"])
                album["streams"] = int(album["streams"])
            except (ValueError, TypeError):
                raise ValueError("L'année et les streams doivent être des entiers.")
            artiste["albums"].append(album)
            return catalogue

    raise ValueError(f"Artiste avec l'ID '{id_artiste}' introuvable.")


def afficher_detail_artiste(catalogue, id_ou_nom):
    """
    Retourne le détail complet d'un artiste (albums inclus).

    Args:
        catalogue (list): Liste des artistes
        id_ou_nom (str): ID ou nom de l'artiste

    Returns:
        dict or None: L'artiste trouvé, ou None
    """
    id_ou_nom_lower = id_ou_nom.strip().lower()
    for artiste in catalogue:
        if (artiste["id"].lower() == id_ou_nom_lower
                or artiste["nom"].lower() == id_ou_nom_lower):
            return artiste
    return None
