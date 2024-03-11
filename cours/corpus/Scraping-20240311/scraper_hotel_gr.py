# -*- coding: utf-8 -*-
# coding: utf-8
from bs4 import BeautifulSoup
import json
import requests
import re,csv
import time
# import encoding

'''
scrap('https://https://www.tripadvisor.com.gr/Hotels-g189415-Chania_Town_Chania_Prefecture_Crete-Hotels.html
'''
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
headers = { 'User-Agent' : user_agent }

ta_url = 'https://www.tripadvisor.com.gr/Hotels'

def scrap(base_url , location_url):
    activities = []
    csvfile = open('hotel_gr.csv', 'a+',encoding='utf8',newline='\n')  
    writer = csv.writer(csvfile)
    
    dl_page_src(base_url + location_url)

    with open('tripadvisor.html', encoding='utf-8') as page_src:
        source = page_src.read()

    soup = BeautifulSoup(source, 'html.parser')
    
    
    # get last element in the pagenation (i.e.: total number of pages)
    try:
        page_count = int(soup.select('.pagination a')[-1].text.strip())
        print("page count",  page_count )
        for page_no in range(page_count):
            # our formula to compute the next url to download:
            # [page_no * 30]
            # page 1: base_url + location_url
            # page 2: base_url + 'oa' + [page_no * 30] + '-' + location_url
            # etc ...
            ratinglist = []
            page_results = soup.select('.entry')
            for rating in soup.findAll(attrs={"class": "rating reviewItemInline"}):
                bubble_rating =  rating.find('span', class_='ui_bubble_rating')
                newstring= str(bubble_rating)
                a=""
                a=newstring.split("=\"")[1]
                ratinglist.append(int(a[0]))
            
         
            for result, rating in zip(page_results,ratinglist):
                title = result.select('.partial_entry')[0].text.strip()   
                activities = [ title, rating]
                writer.writerow(activities)
                # compute the url for the next page
                        
            next_page = base_url + 'or' + str((page_no + 1) * 10)+'-' + location_url + '#REVIEWS'

            time.sleep(15)
            soup=dl_page_src(next_page)
    except:
        print("in except")
        ratinglist = []
        page_results = soup.select('.entry')
        for rating in soup.findAll(attrs={"class": "rating reviewItemInline"}):
            bubble_rating =  rating.find('span', class_='ui_bubble_rating')
            newstring= str(bubble_rating)
            a=""
            a=newstring.split("=\"")[1]
            ratinglist.append(int(a[0]))
            
         
        for result, rating in zip(page_results,ratinglist):
            title = result.select('.partial_entry')[0].text.strip()   
            activities = [ title, rating]
            writer.writerow(activities)
                # compute the url for the next page
    '''
    with open('activities.json', 'a+', encoding='utf-8') as output:
        data =json.dumps(activities, indent=4,ensure_ascii=False)
        output.write(data)
    '''
    
        
def dl_page_src(url):
    print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    with open('tripadvisor.html', 'w', encoding='utf-8') as saved_page:
        saved_page.write(soup.prettify(encoding='utf-8').decode('utf-8'))
        return soup
        

if __name__ == '__main__':
    scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d265318-Reviews-','Kriti_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d593312-Reviews-','El_Greco_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d491123-Reviews-','Arkadi_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d660067-Reviews-','Hotel_Candia-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d253904-Reviews-','Halepa_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d228871-Reviews-','Kydon_The_Heart_City_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d3344042-Reviews-','Royal_Sun_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d287910-Reviews-','Civitel_Akali_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d6557824-Reviews-','Ambassadors_Residence_Boutique_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d8286727-Reviews-','Elia_Betolo_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d1453497-Reviews-','Hotel_Filoxenia-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d665568-Reviews-','Hotel_Tina-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d10220114-Reviews-','Domus_Renier_Boutique_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d6437631-Reviews-','La_Maison_Ottomane-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d316375-Reviews-','Avra_City_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d1466160-Reviews-','Hotel_Irida-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d662731-Reviews-','Hotel_Irene-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d664114-Reviews-','Nefeli_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d227375-Reviews-','Porto_Veneziano_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d228915-Reviews-','Samaria_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d618200-Reviews-','Hotel_Nostos-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d665562-Reviews-','Theofilos_City_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d250618-Reviews-','Casa_Delfino_Hotel_Spa-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d660033-Reviews-','Hotel_Belmondo-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d315206-Reviews-','Amalthia_Beach_Resort-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d665358-Reviews-','Hotel_Stellina_Village-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d676753-Reviews-','Ionas_Boutique_Hotel-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d568071-Reviews-','Corinna_Mare_Suites_Studios-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g189415-d660271-Reviews-','Casa_Veneta-Chania_Town_Chania_Prefecture_Crete.html')
# scrap('https://www.tripadvisor.com.gr/Hotel_Review-g1015384-d659260-Reviews-','Alexis_Hotel_Chania-Parigoria_Chania_Town_Chania_Prefecture_Crete.html')

