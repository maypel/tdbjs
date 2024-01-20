# -*- coding: utf-8 -*-
import re

def extrait_mot_cle(texts):
    """
    Prends une liste de textes et en détecte les mots les plus fréquents. Cette fonction renvoie 
    la liste des textes et le comptage des mots.
    """

    mot_cle = {}
    articles = []

    for i, text in enumerate(texts):
        # Extraction des éléments selon la structure JSON renvoyée par l'API NEWSAPI.ORG
        source = text["source"]["name"]
        titre = text["title"]
        description = text["description"]
        url = text["url"]
        publiele = text['publishedAt']
        contenu = text["content"]

        # Stockage des articles dans la variable articles
        articles.append({'titre': titre, 'url': url, 'source':source, 'publiele': publiele})

        # Détection des mots clés (mots les plus utilisés)
        text = str(titre) + ' ' + str(description) + ' ' + str(contenu)
        mots = normalise_and_get_mots(text)

        # Comptage des mots
        for w in mots :
            if w not in mot_cle:
                mot_cle[w] = {'cnt': 1, 'articles':[i]}
            else:
                mot_cle[w]['cnt'] += 1
                if i not in mot_cle[w]['articles']:
                    mot_cle[w]['articles'].append(i)

    # Tri des mots, du plus utilisé au moins utilisé
    mot_cle = [{'mot':mot, **data} for mot,data in mot_cle.items()] 
    mot_cle = sorted(mot_cle, key=lambda x: -x['cnt'])

    return mot_cle, articles

def load_stop_mots():
    """
    Charge la liste des stopmots français (les mots très utilisés qui ne sont pas porteurs de sens comme LA, LE, ET, etc.)
    """

    mots = []
    # Ouverture du fichier "stop_mots.txt"
    with open("stop_mots.txt") as f:
        for mot in f.readlines():
            mots.append(mot[:-1])
    return mots

def normalise_and_get_mots(text):
    """
    Prends un texte, le formate puis renvoie tous les mots significatifs qui le constituent
    """

    stop_mots = load_stop_mots()

    # Utilisation des expressions régulières (voir https://docs.python.org/3.7/library/re.html et https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4464009-utilisez-des-expressions-regulieres)
    text = re.sub("\W"," ",text) # suppression de tous les caractères autres que des mots
    text = re.sub(" \d+", " ", text) # suppression des nombres
    text = text.lower() # convertit le texte en minuscules
    mots = re.split("\s",text) # sépare tous les mots du texte

    mots = [w for w in mots if len(w) > 2] # suppression des mots de moins de 2 caractères
    mots = [w for w in mots if w not in stop_mots] # suppression des stopmots
    return mots
