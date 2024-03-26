import requests
from bs4 import BeautifulSoup
import csv

def get_element(game_url, element):
    response = requests.get(game_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_=element)
        results = []
        for elem in elements:
            if elem:
                results.append(elem.get_text().strip())
            else:
                results.append("Element non trouvé")
        if results != []:
            return results
    else:
        print("Erreur lors de la récupération de la page du jeu:", response.status_code)
        return None

# URL de la page JV.com avec la sélection populaire
url = "https://www.jeuxvideo.com/jeux/populaires/"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    game_links = soup.find_all(class_='gameTitleLink__196nPy')
    
    elements = [
        'gameHeaderBanner__title',
        'gameCharacteristicsMain__gaugeText',
        'gameCharacteristicsMain__synopsis',
        'gameCharacteristicsMain__releaseDate',
        'gameCharacteristicsDetailed__tr'
    ]

    # Créer un fichier CSV et écrire les en-têtes
    with open('jeux_populaires.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Titre', 'URL', 'Note Journaliste', "Note Publique", 'Synopsis', 'Date', "Caracteristique"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()
    
        # Pour chaque lien de jeu populaire, récupérer le titre et l'URL et écrire dans le CSV
        for link in game_links:
            game_url = link['href']
            if not game_url.startswith('http'):
                game_url = 'https://www.jeuxvideo.com' + game_url
            i = 0
            resultats = []
            for elem in elements:
                resultats.append(get_element(game_url, elem)) 
                print("Elements trouvé : " + str(resultats))
                i += 1
            writer.writerow({'Titre': resultats[0][0] if len(resultats[1]) > 0 else "", 
                             'URL': game_url, 
                             "Note Journaliste": resultats[1][0] if len(resultats[1]) > 0 else "", 
                             "Note Publique": resultats[1][1] if len(resultats[1]) > 1 else "", 
                             "Synopsis": resultats[2][0] if len(resultats[2]) > 0 else "",
                             'Date': resultats[3][0] if len(resultats[3]) > 0 else "",
                             'Caracteristique': resultats[4] 
                             })
else:
    print("Erreur lors de la récupération de la page:", response.status_code)