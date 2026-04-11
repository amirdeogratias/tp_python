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

