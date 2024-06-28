import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from tqdm import tqdm

class ImmoWebScraper3000:
    def __init__(self,link,headers):

        self.link = link
        self.headers=headers

    def get_data (self,link):
        response = requests.get(link, headers=self.headers)
         # Use BeautifulSoup to parse the content of the response of the request.
        soup = BeautifulSoup(response.content, "html.parser")
        # The relevant property informations are content in a json-like javascript object.
        # Store the information as a string and clean it with some regex.
        infos= soup.find('script', type="text/javascript").text
        window_classified_removed= re.sub("window.classified =","", infos)
        remove_ponctuation = re.sub(";","", window_classified_removed)
        # Convert the result into a json object and try for error.
        try:
            parsed = json.loads(remove_ponctuation)
        except json.JSONDecodeError as e:
            print(f"JSON decoding error for the link: {link}\nError: {e}")
            return None
        return parsed
        
    def get_postalCode(self,parsed):
        """
        This method retrieves the zip code of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            postal_code = parsed['property']["location"]["postalCode"]
            return postal_code
        except:
            return None

    def get_type(self,parsed):
        """
        This method retrieves the type of the property from the json object.
        It returns None if this information is not available.
        """   
        try:
            type= parsed['property']['type']
            return type
        except:
            return None
            

    def get_subtype(self,parsed):
        """
        This method  retrieves the subtype of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            subtype= parsed['property']['subtype']
            return subtype
        except:
            return None
        


    def get_price(self,parsed):
        """
        This method  retrieves the price of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            price= parsed['price']['mainValue']
            return price
        except:
            return None 

    def get_whatSale(self,parsed):
        """
        This method  retrieves the type of the sale of the property from the json object.
        It returns None if this information is not available.
        """
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


    def get_nbrBedrooms(self,parsed):
        """
        This method  retrieves the number of bedrooms of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            nbrBedrooms= parsed['property']['bedroomCount']
            return nbrBedrooms
        except:
            return None
        
    def get_livingArea(self,parsed):
        """
        This method  retrieves the living area in m² of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            livingArea= parsed['property']['netHabitableSurface']
            return livingArea     
        except:
            return None 

    def is_KitchenEquiped(self,parsed):
        """
        This method  returns True if the kitchen of the property is equiped,
        False otherwise, and None if this information is not available.
        """
        try:
            KitchenEquiped= parsed['property']['kitchen']['type']
            if KitchenEquiped == "":
                return None
            else:
                return KitchenEquiped
        except:
            return None 
        
    def is_furnished(self,parsed):
        """
        This method  returns True if the kitchen of the property is furnished,
        False otherwise; and also False if this information is not available.
        """
        try:
            if  parsed['transaction']['sale']['isFurnished']:
                return True
            else:
                return False     
        except:
            return False 
        
    def HasOpenFire(self,parsed):
        """
        This method returns True if the property has an open fire,
        False otherwise; and also False if this information is not available.
        """
        try:
            OpenFire= parsed['property']['fireplaceExists']
            if OpenFire == True:
                return OpenFire
            elif OpenFire == False:
                return OpenFire
        except:
            return False

    def HasTerrace(self,parsed):
        """
        This method  retrieves the terrace area in m² of the property from the json object.
        It returns 0 if it has no terrace or if this information is not available.
        """
        try:
            Terrace= parsed['property']['hasTerrace']
            if Terrace == True:
                surface = parsed['property']['terraceSurface']
                return int(surface)
            else:
                return 0
        except:
            return 0

    def HasGarden(self,parsed):
        """
        This method  retrieves the garden area in m² of the property from the json object.
        It returns 0 if it has no garden or if this information is not available.
        """
        try:
            Garden= parsed['property']['hasGarden']
            if Garden == True:
                surface = parsed['property']['gardenSurface']
                return int(surface)
            else:
                return 0
        except:
            return 0 

    def get_plotSurface(self,parsed):
        """
        This method  retrieves the plot surface area in m² of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            plotSurface= parsed['property']['land']['surface']
            return plotSurface 
        except:
            return None 
    
    def get_nbrFacades(self,parsed):
        """
        This method  retrieves the number of facade of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            Facades= parsed['property']['building']['facadeCount']
            return int(Facades)    
        except:
            return None 
                
    def HasSwimPool(self,parsed):
        """
        This method  returns True if the property has a swimming pool,
        False otherwise; and also False if this information is not available.
        """
        try:
            if parsed['property']['hasSwimmingPool']:
                return True
            else:
                return False
        except:
            return False  

    def get_BuildingState(self,parsed):
        """
        This method  retrieves the building state of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            State= parsed['property']['building']['condition']
            return State     
        except:
            return None 
        
    def get_yearConstruct(self,parsed):
        """
        This method  retrieves the year of construction of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            yearConstruct= parsed['property']['building']['constructionYear']
            return int(yearConstruct)  
        except:
            return None 

    def is_inFloodZone(self,parsed):
        """
        This method  returns True if the property is in a flood zone, False otherwise.
        It returns None if this information is not available.
        """
        try:
            FloodZone= parsed['property']['constructionPermit']['floodZoneType']
            return FloodZone    
        except:
            return None 
        
    def get_allDatas(self,parsed):
        """
        For any url of a property on the immoweb, this method  returns a dictionary with all the relevant features of the property. 
        """
        data={'postalCode':self.get_postalCode(parsed), 
                'type':self.get_type(parsed),
                'subType':self.get_subtype(parsed),
                'price':self.get_price(parsed),
                'SaleType':self.get_whatSale(parsed),
                'nbrBedrooms':self.get_nbrBedrooms(parsed),
                'livingArea': self.get_livingArea(parsed),
                'Kitchen':self.is_KitchenEquiped(parsed),
                'Furnished':self.is_furnished(parsed),
                'OpenFire':self.HasOpenFire(parsed),
                'Terrace':self.HasTerrace(parsed),
                'Garden':self.HasGarden(parsed),
                'plotSurface':self.get_plotSurface(parsed),
                'nbrFacades':self.get_nbrFacades(parsed),
                'SwimPool':self.HasSwimPool(parsed),
                'State':self.get_BuildingState(parsed),
                'yearConstruct':self.get_yearConstruct(parsed),
                'FloodZone':self.is_inFloodZone(parsed),}
        return data


    def get_page_links(self,soup):
        """
        This method  return a list of all the urls of the properties of a page of the result of the search.
        """
        links = []
        properties = soup.find_all('a', attrs={"class":"card__title-link"})
        for link in properties:
            href= link["href"]
            if href in links:
                continue
            elif 'new-real-estate-project-apartments' not in href and 'new-real-estate-project-houses' not in href:
                    links.append(href)
        return links

    def get_allpages(self):
        """
        This method  loops through all the pages of the result of the search, and returns a list of alll the urls.
        """
        all = []
        for i in range (1,334):
            url = f"{self.link}&page={i}"
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            links = self.get_page_links(soup)
            all.extend(links)
        return all

    def scrape(self):
        """
        This fmethod  loops through the list of all urls and retrieves all the informations using the get_allDatas function.
        It returns a list of dictionaries. One dictionary for each property.
        """
        pages = self.get_allpages()
        data= []
        for page in tqdm(pages):
            parsed= self.get_data(page)
            if parsed is None:
                continue
            test=self.get_allDatas(parsed)
            data.append(test)
        return data

# Set an user-agent to make requests.
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
url= 'https://www.immoweb.be/en/search/house/for-rent?countries=BE&page=1&orderBy=relevance'

# Generate the list of all informations property 'for sale' and convert it into a dataframe.
scraper_3000= ImmoWebScraper3000(url,headers)
datas=scraper_3000.scrape()
df1 = pd.DataFrame(datas)

# Generate the list of all informations property 'to rent' and convert it into a dataframe.
url2= 'https://www.immoweb.be/en/search/house/for-rent?countries=BE&page=1&orderBy=relevance'
scraper_3000= ImmoWebScraper3000(url2,headers)
datas2=scraper_3000.scrape()
df2 = pd.DataFrame(datas2)

# Merge the two dataframes
df_merged = pd.concat([df1, df2], ignore_index=True)
# Convert the merged dataframe into a csv file.
df_merged.to_csv("immo_properties_final.csv", index=False)


print(df_merged)
