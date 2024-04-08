import requests
from bs4 import BeautifulSoup
import csv

debug = False

def get_url(filename):
    urls = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls

def get_element(game_url, element):
    response = requests.get(game_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        elements = soup.find_all(class_=element)

        results = [elem.get_text().strip() for elem in elements]
        if debug: print(results)
        return results
    else:
        if debug: print("Erreur lors de la récupération de la page du jeu:", response.status_code)
        return []

def get_avis(urls, elements):
    previous_pseudos = set()  # Ensemble des pseudonymes de la page précédente

    with open('database/jeux_avis_populaire.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Titre', 'URL', 'Note', 'Pseudo', 'Avis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
        writer.writeheader()

        for i, url_main in enumerate(urls):
            print(f"url {i+1} : {url_main}")
            recurrence = False
            r = 1
            while recurrence == False:
                url = url_main + "?p=" + str(r)
                print(f"url {i+1} : {url}")
                response = requests.get(url)
                if response.status_code == 200:
                    resultats = [get_element(url, elem) for elem in elements]
                    titre, note, pseudo, avis = resultats
                    note = note[2:]
                    pseudo = [p.split('\n')[0] for p in pseudo]
                    if debug: print(pseudo)
                    avis = avis[1:-1]

                    # Vérifie si les pseudonymes de la page actuelle sont égaux à ceux de la page précédente
                    current_pseudos = set(pseudo)
                    if current_pseudos == previous_pseudos:
                        print("Les pseudonymes de la page actuelle sont les mêmes que ceux de la page précédente. La page est ignorée.")
                        recurrence = True
                        continue

                    previous_pseudos = current_pseudos  # Met à jour les pseudonymes de la page précédente

                    max_length = max(len(titre), len(note), len(pseudo)-2, len(avis))
                    for j in range(max_length):
                        titre_value = titre[j] if j < len(titre) else ""
                        note_value = note[j] if j < len(note) else []
                        pseudo_value = pseudo[j] if j < len(pseudo) else ""
                        avis_value = avis[j] if j < len(avis) else ""

                        writer.writerow({'Titre': titre_value, 'Note': note_value, 'URL': url, 'Pseudo': pseudo_value, 'Avis': avis_value})
                else:
                    if debug: print("Erreur lors de la récupération de la page:", response.status_code)
                url = url_main + "/?p=" + str(r)
                r += 1

def main():
    urls = get_url("database/url.txt")
    elements = [
        "gameHeaderBanner__title",
        "note-avis",
        "bloc-header",
        "txt-avis text-enrichi-forum",
    ]
    get_avis(urls, elements)

if __name__ == "__main__":
    main()
