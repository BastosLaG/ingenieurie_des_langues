from dateparser.search import search_dates
import re
import glob

liste_demain = ["hier", "avant-hier", "aujourd'hui", "demain", "après-demain"]
liste_semaine = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
liste_mot_deb = ["à", 'juste', 'après', 'avant', 'vers']
liste_mot_deb_long = ["à", 'juste', 'après', 'avant', 'vers'] + liste_demain + liste_semaine


# Fonction pour nettoyer le texte
def nettoyer_texte(texte):
    texte_propre = re.sub(r'[^\w\s]', '', texte)
    texte_propre = texte_propre.lower()
    return texte_propre

def examine_phrase(phrase):
    current_phrase = phrase.split(' ')
    for i in range(len(current_phrase)):
        current_phrase.append(mot)
        if current_phrase[i] in liste_mot_deb:
            print(current_phrase[i])
        elif current_phrase[i] in liste_demain:
            print(current_phrase[i])
        elif current_phrase[i] in liste_semaine:
            print(current_phrase[i])

for filename in glob.glob("src/*.txt"):
    print(filename + " :")
    with open(filename, 'r') as file:
        text = file.read()
        text = text.lower()
        for phrase in re.split(r'[.!?_,]+', text):            
            for mot in re.split(r'[,\s.!?«»;:]+', phrase):
                if mot in liste_mot_deb_long:
                    examine_phrase(phrase)

        text = nettoyer_texte(text)

        # Pas de version FR
        # print(re.findall(r'[A-Z]\w+\s\d+', text)) 
        
        # Mots parasite
        # for date_tuple in search_dates(text, languages=['fr']):
        #     date_str, date_obj = date_tuple
        #     if date_str.lower() not in ["je", "sa", "me", "ma"]:
        #         print(str(date_str) + '\t||\t' + str(date_obj))
