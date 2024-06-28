import numpy as np
import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
from requests import Session
import re


def property_infomation(url: str, session: Session) -> dict:
    """
    For any url of a property on the immoweb, this fonction returns a dictionary with all the relevant features of the property. 
    """
    # Set an user-agent to make a request.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36'}
    response = requests.get(url, headers=headers)
    # Use BeautifulSoup to parse the content of the response of the request.
    soup = BeautifulSoup(response.content, "html.parser")
    # The relevant property informations are content in a json-like javascript object.
    # Store the information as a string and clean it with some regex.
    infos = soup.find('script', type="text/javascript").text
    window_classified_removed = re.sub("window.classified =", "", infos)
    remove_ponctuation = re.sub(";", "", window_classified_removed)
    # Convert the result into a json object.
    parsed = json.loads(remove_ponctuation)

    def get_postalCode(parsed):
        """
        This function retrieves the zip code of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            postal_code = parsed['property']["location"]["postalCode"]
            return postal_code
        except:
            return None

    def get_type(parsed):
        """
        This function retrieves the type of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            type_property = parsed['property']['type']
            return type_property
        except:
            return None

    def get_subtype(parsed):
        """
        This function retrieves the subtype of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            subtype = parsed['property']['subtype']
            return subtype
        except:
            return None

    def get_price(parsed):
        """
        This function retrieves the price of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            price = parsed['price']['mainValue']
            return int(price)
        except:
            return None

    def get_whatSale(parsed):
        """
        This function retrieves the type of the sale of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            SaleType = parsed['flags']['isPublicSale']
            if SaleType == True:
                typeofsale = "Public Sale"
                return typeofsale

            SaleType = parsed['flags']['isNotarySale']
            if SaleType == True:
                typeofsale = "Notary Sale"
                return typeofsale
            SaleType = parsed['flags']['isAnInteractiveSale']
            if SaleType == True:
                typeofsale = "Interactive Sale"
                return typeofsale

            SaleType = parsed['flags']['isNewlyBuilt']
            if SaleType == True:
                typeofsale = "Newly Built"
                return typeofsale

            SaleType = parsed['flags']['isNewClassified']
            if SaleType == True:
                typeofsale = "New Classified"
                return typeofsale

            SaleType = parsed['flags']['isNewPrice']
            if SaleType == True:
                typeofsale = "New Price"
                return typeofsale

            SaleType = parsed['flags']['isUnderOption']
            if SaleType == True:
                typeofsale = "Under Option"
                return typeofsale
        except:
            return None

    def get_nbrBedrooms(parsed):
        """
        This function retrieves the number of bedrooms of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            nbrBedrooms = parsed['property']['bedroomCount']
            return int(nbrBedrooms)
        except:
            return None

    def get_livingArea(parsed):
        """
        This function retrieves the living area in m² of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            livingArea = parsed['property']['netHabitableSurface']
            return int(livingArea)
        except:
            return None

    def is_KitchenEquiped(parsed):
        """
        This function returns True if the kitchen of the property is equiped,
        False otherwise, and None if this information is not available.
        """
        try:
            KitchenEquiped = parsed['property']['kitchen']['type']
            if KitchenEquiped == "":
                return None
            else:
                return KitchenEquiped
        except:
            return None

    def is_furnished(parsed):
        """
        This function returns True if the kitchen of the property is furnished,
        False otherwise; and also False if this information is not available.
        """
        try:
            furnished = parsed['transaction']['sale']['isFurnished']
            if furnished == True:
                return furnished
            elif furnished == False:
                return furnished
        except:
            return False

    def HasOpenFire(parsed):
        """
        This function returns True if the property has an open fire,
        False otherwise; and also False if this information is not available.
        """
        try:
            OpenFire = parsed['property']['fireplaceExists']
            if OpenFire == True:
                return OpenFire
            elif OpenFire == False:
                return OpenFire
        except:
            return False

    def HasTerrace(parsed):
        """
        This function retrieves the terrace area in m² of the property from the json object.
        It returns 0 if it has no terrace or if this information is not available.
        """
        try:
            Terrace = parsed['property']['hasTerrace']
            if Terrace == True:
                surface = parsed['property']['terraceSurface']
                return int(surface)
            else:
                return 0
        except:
            return 0

    def HasGarden(parsed):
        """
        This function retrieves the garden area in m² of the property from the json object.
        It returns 0 if it has no garden or if this information is not available.
        """
        try:
            Garden = parsed['property']['hasGarden']
            if Garden == True:
                surface = parsed['property']['gardenSurface']
                return int(surface)
            else:
                return 0
        except:
            return 0

    def get_plotSurface(parsed):
        """
        This function retrieves the plot surface area in m² of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            plotSurface = parsed['property']['land']['surface']
            return int(plotSurface)
        except:
            return None

    def get_nbrFacades(parsed):
        """
        This function retrieves the number of facade of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            Facades = parsed['property']['building']['facadeCount']
            return int(Facades)
        except:
            return None

    def HasSwimPool(parsed):
        """
        This function returns True if the property has a swimming pool,
        False otherwise; and also False if this information is not available.
        """
        try:
            if parsed['property']['hasSwimmingPool']:
                return True
            else:
                return False
        except:
            return False

    def get_BuildingState(parsed):
        """
        This function retrieves the building type of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            State = parsed['property']['building']['condition']
            return State
        except:
            return None

    def get_yearConstruct(parsed):
        """
        This function retrieves the year of construction of the property from the json object.
        It returns None if this information is not available.
        """
        try:
            yearConstruct = parsed['property']['building']['constructionYear']
            return int(yearConstruct)
        except:
            return None

    def is_inFloodZone(parsed):
        """
        This function returns True if the property is in a flood zone, False otherwise.
        It returns None if this information is not available.
        """
        try:
            FloodZone = parsed['property']['constructionPermit']['floodZoneType']
            if FloodZone == 'NON_FLOOD_ZONE':
                return False
            if FloodZone == 'POSSIBLE_FLOOD_ZONE':
                return True
        except:
            return None

    return {
        "Locality": get_postalCode(parsed),
        "Type of property": get_type(parsed),
        "Subtype of property": get_subtype(parsed),
        "Price": get_price(parsed),
        "Type of sale": get_whatSale(parsed),
        "Number of bedrooms": get_nbrBedrooms(parsed),
        "Living Area (m²)": get_livingArea(parsed),
        "Fully equipped kitchen": is_KitchenEquiped(parsed),
        "Furnished": is_furnished(parsed),
        "Open fire": HasOpenFire(parsed),
        "Terrace Area (m²)": HasTerrace(parsed),
        "Garden Area (m²)": HasGarden(parsed),
        "Surface of the plot (m²)": get_plotSurface(parsed),
        "Number of facades": get_nbrFacades(parsed),
        "Swimming pool": HasSwimPool(parsed),
        "State of the building": get_BuildingState(parsed),
        "Construction Year": get_yearConstruct(parsed),
        "Flood Zone": is_inFloodZone(parsed)
    }


def real_estate_urls(url: str, session: Session) -> list:
    """
    Some results of the search pages are real estate projects with links of the individual properties of the project.
    This function allows to get the urls of these individual properties.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return [item.get("href") for item in soup.find_all('a', attrs={'class': 'classified-with-plan__list-item classified__list-item-link'})]


def search_page_urls(url: str, session: Session = Session()) -> list:
    """
    This function gets all the urls of the properties of a search page.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.9999.99 Safari/537.36'}
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls_list = [item.get("href") for item in soup.find_all(
        'a', attrs={'class': 'card__title-link'})]
    real_estate_list = [
        url for url in urls_list if 'new-real-estate-project-apartments' in url]
    urls_list = [
        url for url in urls_list if not 'new-real-estate-project-apartments' in url]
    with Session() as session:
        for elem in real_estate_list:
            urls_list.extend(real_estate_urls(elem, session))

    return urls_list


def session_loop_request():
    """
    This function loops through all the pages of the result of the search.
    It returs a list of dictionaries. Each dictionary containing a property's informations.
    """
    url_start = 'https://www.immoweb.be/en/search/house-and-apartment/for-sale?countries=BE&isALifeAnnuitySale=false&page='
    url_end = '&orderBy=relevance'
    infos_list = []
    # Create shared session for all of the requests.
    with Session() as session:
        # The search returns 333 pages. Query the 333 pages.
        for i in range(1, 334):
            for url in search_page_urls(url_start + str(i) + url_end, session):
                try:
                    property_infomation(url, session)
                    infos_list.append(property_infomation(url, session))
                except:
                    pass
    return infos_list

# Create the list of all properties informations and store it.
data = session_loop_request()

# Convert the list into a dataframe.
df = pd.DataFrame(data)

# Remove all the duplicates.
df_2 = df.drop_duplicates()

# Convert the dataframe into a csv file
df_2.to_csv('immoweb_properties.csv', index=False)