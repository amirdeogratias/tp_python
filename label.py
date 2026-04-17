import json
def charger_catalogue(chemin:str):
    #charger les données du catalogue depuis un fichier json et retourne une liste vide si le fichier n'existe pas  
    try:
        with open (chemin,'r') as f:
            return json.load(f) 
    except(FileNotFoundError,json.JSONDecodeError):
        return[]
    
def sauvegarder_catalogue(data:list,chemin:str):
    #inscrire les données dans  le catalogue
    try:
        with open(chemin,'w') as f:
            json.dump(data,f,ensure_ascii=False,indent=4)
    except IOError as e:
        raise IOError(f"impossible d'écrire dans le fichier'{chemin}':{e}")

def lister_artistes(catalogue:list):
    #retourner la liste des artistes avec leurs informations
    resume=[]
    for artiste in catalogue:
        resume.append({
            "id":artiste.get("id","N/A"),
            "nom":artiste.get("nom","N/A"),
            "genre":artiste.get("genre","N/A"),
            "pays":artiste.get("pays","N/A"),
            "nb_albums":len(artiste.get("albums",[]))
        })
    return resume

def rechercher_artiste(catalogue:list,critere:str,valeur:str):
    #definition des critéeres de recherche valide
    criteres_valides =["nom","genre","pays"]
    #envoyer message d'erreur si critère non disponible
    if critere not in criteres_valides:
        raise ValueError(f"'{critere}' invalide")
    #lister les artistes correspondants à la recherche
    valeur_lower= valeur.strip().lower()
    resultats=[artiste for artiste in catalogue if valeur_lower in str(artiste.get(critere,"")).lower()]
    return resultats

def ajouter_artistes(catalogue:list,artiste:dict):
    #création du champ et vérification
    champ_requis=["id","nom","genre","pays","albums"]
    for champ in champ_requis:
        if champ not in artiste:
            raise ValueError(f"champ obligatoire manquant :'{champ}'")
    #verifier si l'artiste n'existe pas déja
    id_existant = [a.get(id) for a in catalogue]
    if artiste["id"] in id_existant:
        raise ValueError("l'artiste existe déja")
    catalogue.append(artiste)
    return catalogue

def ajouter_album(catalogue:list,id_artiste:str):
    #champ requis pour l'album
    champs=("titre","annee","streams")
    for champ in champs:
        if champ not in champs:
            raise ValueError(f"champ obligatoire manquant :'{champ}'")
   #ajouter l'album si l'id correspond a l'id dans le catalogue
    for artiste in catalogue:
        if artiste.get("id")== id_artiste:
            album={}
            artiste["albums"].append(album)
            return catalogue
    raise ValueError("artiste introuvable")

def obtenir_detail_artiste(catalogue:list,id_artiste:str):
    #afficher les détails selon l'id
    for artiste in catalogue:
        if artiste.get("id")==id_artiste:
            return artiste
    raise ValueError("artiste introuvable")


