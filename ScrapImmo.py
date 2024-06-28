import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from tqdm import tqdm



headers = { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }


def get_data (link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    infos= soup.find('script', type="text/javascript").text

    window_classified_removed= re.sub("window.classified =","", infos)
    remove_ponctuation = re.sub(";","", window_classified_removed)
    try:
        parsed = json.loads(remove_ponctuation)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error for the link: {link}\nError: {e}")
        return None
    parsed = json.loads(remove_ponctuation)

    return parsed

def get_postalCode(parsed):
    try:
        postal_code = parsed['property']["location"]["postalCode"]
        return postal_code
    except:
        return None

def get_type(parsed):
    
    try:
        type= parsed['property']['type']
        return type
    except:
        return None

def get_subtype(parsed):
    
    try:
        subtype= parsed['property']['subtype']
        return subtype
    except:
        return None
       


def get_price(parsed):
    try:
        price= parsed['price']['mainValue']
        return price
    except:
        return None 

def get_whatSale(parsed):
    try:
        SaleType= parsed['flags']['isPublicSale']
        if SaleType == True:
            typeofsale= "Public Sale"
            return typeofsale
        
        SaleType= parsed['flags']['isNotarySale']
        if SaleType == True:
            typeofsale= "Notary Sale"
            return typeofsale
        SaleType= parsed['flags']['isAnInteractiveSale']
        if SaleType == True:
            typeofsale= "Interactive Sale"
            return typeofsale
        
        SaleType = parsed['flags']['isNewlyBuilt'] 
        if SaleType == True:
            typeofsale= "Newly Built"
            return typeofsale 
        
        SaleType = parsed['flags']['isNewClassified'] 
        if SaleType == True:
            typeofsale= "New Classified"
            return typeofsale 

        SaleType = parsed['flags']['isNewPrice'] 
        if SaleType == True:
            typeofsale= "New Price"
            return typeofsale    
        
        SaleType = parsed['flags']['isUnderOption'] 
        if SaleType == True:
            typeofsale= "Under Option"
            return typeofsale      
    except:
        return None 


def get_nbrBedrooms(parsed):
    try:
        nbrBedrooms= parsed['property']['bedroomCount']
        return nbrBedrooms
    except:
        return None
    
def get_livingArea(parsed):
    try:
        livingArea= parsed['property']['netHabitableSurface']
        return livingArea     
    except:
        return None 

def is_KitchenEquiped(parsed):
    try:
        KitchenEquiped= parsed['property']['kitchen']['type']
        if KitchenEquiped == "":
            return None
        else:
            return KitchenEquiped
    except:
        return None 
    
def is_furnished(parsed):
    try:
        if  parsed['transaction']['sale']['isFurnished']:
            return True
        else:
            return False     
    except:
        return False 
     
def HasOpenFire(parsed):
    try:
        OpenFire= parsed['property']['fireplaceExists']
        if OpenFire == True:
            return OpenFire
        elif OpenFire == False:
            return OpenFire
    except:
        return False

def HasTerrace(parsed):
    try:
        Terrace= parsed['property']['hasTerrace']
        if Terrace == True:
            surface = parsed['property']['terraceSurface']
            return int(surface)
        else:
            return 0
    except:
        return 0

def HasGarden(parsed):
    try:
        Garden= parsed['property']['hasGarden']
        if Garden == True:
            surface = parsed['property']['gardenSurface']
            return int(surface)
        else:
            return 0
    except:
        return 0 

def get_plotSurface(parsed):
    try:
        plotSurface= parsed['property']['land']['surface']
        return plotSurface 
    except:
        return None 

def get_nbrFacades(parsed):
    try:
        Facades= parsed['property']['building']['facadeCount']
        return int(Facades)    
    except:
        return None 
             
def HasSwimPool(parsed):
    try:
        if parsed['property']['hasSwimmingPool']:
            return True
        else:
            return False
    except:
        return False  

def get_BuildingState(parsed):
    try:
        State= parsed['property']['building']['condition']
        return State     
    except:
        return None 
    
def get_yearConstruct(parsed):
    try:
        yearConstruct= parsed['property']['building']['constructionYear']
        return int(yearConstruct)  
    except:
        return None 

def is_inFloodZone(parsed):
    try:
        FloodZone= parsed['property']['constructionPermit']['floodZoneType']
        if FloodZone == "POSSIBLE_FLOOD_ZONE":
            return True
        if FloodZone == "NON_FLOOD_ZONE":
            return False   
    except:
        return None 


def get_allDatas(parsed):

    data={'postalCode':get_postalCode(parsed), 
          'type':get_type(parsed),
          'subType':get_subtype(parsed),
          'price':get_price(parsed),
          'SaleType':get_whatSale(parsed),
          'nbrBedrooms':get_nbrBedrooms(parsed),
          'livingArea': get_livingArea(parsed),
          'Kitchen':is_KitchenEquiped(parsed),
          'Furnished':is_furnished(parsed),
          'OpenFire':HasOpenFire(parsed),
          'Terrace':HasTerrace(parsed),
          'Garden':HasGarden(parsed),
          'plotSurface':get_plotSurface(parsed),
          'nbrFacades':get_nbrFacades(parsed),
          'SwimPool':HasSwimPool(parsed),
          'State':get_BuildingState(parsed),
          'yearConstruct':get_yearConstruct(parsed),
          'FloodZone':is_inFloodZone(parsed),}

    return data


def get_page_link(soup):
    links = []
    properties = soup.find_all('a', attrs={"class":"card__title-link"})
    for link in properties:
        href= link["href"]
        if href in links:
            continue
        elif 'new-real-estate-project-apartments' not in href and 'new-real-estate-project-houses' not in href:
                links.append(href)
    return links
    

def get_allpages(soup):
    all = []
    for i in range (1,334):
        links = get_page_link(soup)
        all.extend(links)
    return all


url = 'https://www.immoweb.be/en/search/house/for-rent?countries=BE&page=1&orderBy=relevance'
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')
pages=get_allpages(soup)
data= []
for page in tqdm(pages):
    parsed= get_data(page)
    if parsed is None:
        continue
    test=get_allDatas(parsed)
    data.append(test)
df = pd.DataFrame(data)
df.to_csv("immo_properties_rent.csv", index=False)


