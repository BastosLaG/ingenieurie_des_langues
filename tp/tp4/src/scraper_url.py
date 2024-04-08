import requests
from bs4 import BeautifulSoup

debug = False
# potential_value = 10

def get_element(url, element):
    """
    Fonction pour récupérer les éléments spécifiés d'une page HTML.
    
    Args:
        url (str): L'URL de la page à récupérer.
        element (str): La classe CSS des éléments à extraire.
    
    Returns:
        list: Une liste des éléments récupérés.
    """
    response = requests.get(url)
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
        print("Erreur lors de la récupération de la page:", response.status_code)
        return None


def get_url_avis_valide():
    # URL de la page JV.com avec la sélection populaire
    url = "https://www.jeuxvideo.com/jeux/populaires/"
    valide_avis_urls = []  # Stocker tous les URL d'avis valides
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        game_links = soup.find_all(class_='gameTitleLink__196nPy')
        
        for link in game_links:
            game_url_parts = link['href'].split('/')  
            game_id = game_url_parts[-2]
            game_url = f"https://www.jeuxvideo.com/jeux/{game_id}/"
            if debug: print("URL du jeu : " + str(game_url))
            
            response_main = requests.get(game_url)
            
            if response_main.status_code == 200:
                soup = BeautifulSoup(response_main.text, 'html.parser')
                avis_links = soup.find_all(class_='gameCharacteristicsMain__reviewTitle')
                
                if avis_links:
                    for avis_link in avis_links:
                        if avis_link.name == 'a' and 'href' in avis_link.attrs:
                            avis_url = avis_link['href']
                            if avis_url[-6:] == '/avis/': 
                                valide_avis_url = f"https://www.jeuxvideo.com{avis_url}"
                                valide_avis_urls.append(f"{valide_avis_url}note/")  # Ajouter à la liste des URL d'avis valides
                    
                    if valide_avis_urls:
                        if debug: print("URLs d'avis valides : ", valide_avis_urls)
                    else:
                        if debug: print("Aucun lien d'avis valide trouvé pour ce jeu.")
                else:
                    if debug: print("Aucun lien d'avis trouvé pour ce jeu.")
            else:
                if debug: print("Erreur lors de la récupération de la page: ", response_main.status_code)
    else:
        if debug: print("Erreur lors de la récupération de la page : ", response.status_code)
    return valide_avis_urls



def get_all(pages_recheche, class_rechercher):
    all_avis_links = []
    for url in pages_recheche:
        all_avis_links.append(url)
        response = requests.get(url)   
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            pages_link = soup.find_all(class_=class_rechercher)
            if pages_link:
                for page in pages_link:
                    if page.name == 'a' and 'href' in page.attrs:
                        page_url = page['href']
                        if page_url[-6:] == '/avis/':
                            all_avis_link = f"https://www.jeuxvideo.com{page_url}"
                            all_avis_links.append(f"{all_avis_link}note/")  
            else:
                if debug: print("Aucun lien de page trouvé pour l'URL:", url)
        else:
            if debug: print("Erreur lors de la récupération de la page:", response.status_code, "pour l'URL:", url)
    return all_avis_links

# def get_potential_avis_page(pages_recheche):
#     all_avis_links = []
#     for url in pages_recheche:
#         all_avis_links.append(url)
#         for i in range(2, potential_value+1, 1):
#             temp_url = f'{url}?p={i}'
#             all_avis_links.append(temp_url)
#     return all_avis_links


def test_avis_pages(potential_avis_pages):
    tested_pages = set()
    valid_pages = []

    for page in potential_avis_pages:
        if page not in tested_pages:
            tested_pages.add(page) 
            try:
                if page not in valid_pages:
                    valid_pages.append(page)
            except Exception as e:
                print(f"Erreur lors du test de la page {page}: {str(e)}")
    return valid_pages


def main():
    if debug: print("Recherche pages de jeux...")
    valide_avis_urls = get_url_avis_valide()
    if debug: print("OK")
    for elem in valide_avis_urls:
        if debug: print(elem)

    if debug:print("Recherche toutes pages avis pour les jeux...")
    avis_urls = get_all(valide_avis_urls,'gameHeaderBanner__platformLink')
    if debug:print("OK")
    for elem in avis_urls:
        print(elem)


if __name__ == "__main__":
    # debug = True
    # potential_value = 10
    main()
