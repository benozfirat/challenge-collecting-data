# 🏠🏢 Immoweb Property Data Scraper

<p align="center">
  <img src="title.jpg" style="max-width: 35%; height: auto;">
</p>

## 📜 Description

<p align="center">
  <img src="title1.PNG" style="max-width: 15%; height: auto;">
</p>

- This project involves a web scraper that collects property data from Immoweb, a leading real estate website in Belgium.

- The scraper extracts detailed information about properties listed for sale, including their location, type, price, number of rooms, and additional features such as garden, terrace, swimming pool, and more.

- The data is then compiled into a CSV file for further analysis or use.

## 📦 Installation

- To run this project, you need to have Python installed on your machine. You also need the following Python libraries:

- 🌐 `requests`

- 🕸️ `beautifulsoup4`

- 🐼 `pandas`

- 🐍 `tqdm`

## 🛠️ Usage

### 1. 📥 Setup and Run the Scraper

- Save the Python script provided in this README to a file, ` immoweb_scraper.py.`

- Run the script to start scraping data from Immoweb:
  `python immoweb_scraper.py`

### 2. 📊 Collecting Data

The script will:

- Navigate through property listings on Immoweb.

- Extract data from each property page.

- Store the extracted data in a list.

- Convert the list to a pandas DataFrame.

- Save the DataFrame to a CSV file `immoweb_properties.csv`

### 3. 🔄 📝 Handling Missing Values

- The script will then read the CSV file, fill any missing values with None, and save the updated DataFrame back to the CSV file.

### 4. 📉 Viewing Data

- Finally, the script prints the contents of the DataFrame to the console.

## 🦄 Features

### 🖥️ Data Collection and Processing:

- Automated data extraction and processing from web pages.

- Analysis and transformation of JSON data.

### 📋 Data Points and Attributes:

- Detailed analysis of property listings.

- Extraction of data points such as property type, subtype, price, number of rooms, etc.

### 🧩 Detailed Features:

- Verification of kitchen equipment.

- Inquiry into whether the property is furnished.

- Verification of the presence of an open fire.

### 🌳 Property Area Features:

- Verification of the presence and surface area of balcony or terrace.

- Verification of garden area.

### 🌟Additional Features:

- Verification of the presence of a swimming pool.

- Inquiry into building condition and construction year.

- Verification of flood risk status.

## 🧑‍💻🎯 Project Components: Functions and Descriptions

- 🏠 `get_postalCode(parsed)`: Extracts the postal code.

- 🏡 `get_type(parsed)`: Extracts the property type.

- 🏘️ `get_subtype(parsed)`: Extracts the property subtype.

- 💰 `get_price(parsed)`: Extracts the price.

- 🛒 `get_whatSale(parsed)`: Determines the sale type (public sale, notary sale, interactive sale).

- 🛏️ `get_NbrRooms(parsed)`: Extracts the number of rooms.

- 📏 `get_livingArea(parsed)`: Extracts the living area.

- 🍽️ `is_KitchenEquiped(parsed)`: Checks if the kitchen is equipped.

- 🛋️ `is_furnished(parsed)`: Checks if the property is furnished.

- 🔥 `HasOpenFire(parsed)`: Checks if there is an open fire.

- 🏞️ `HasTerrace(parsed)`: Checks if there is a terrace and its surface.

- 🌳 `HasGarden(parsed)`: Checks if there is a garden and its surface.

- 🌄 `get_plotSurface(parsed)`: Extracts the plot surface area.

- 🏛️ `get_nbrFacades(parsed)`: Extracts the number of facades.

- 🏊‍♂️ `HasSwimPool(parsed)`: Checks if there is a swimming pool.

- 🏗️ `get_BuildingState(parsed)`: Extracts the building state or condition.

- 🏢 `get_yearConstruct(parsed)`: Extracts the year of construction.

- 🌊 `is_inFloodZone(parsed)`: Checks if the property is in a flood zone.

- 🛏️ `get_nbrBedrooms(parsed)`: Extracts the number of bedrooms.

- 📋 `get_allDatas(parsed)`: Collects all the extracted data points into a single dictionary.

- 🔍 `get_page_link(soup)`: Extracts links to individual property pages from the search results page.

- 📑 `get_allpages(soup)`: Collects links from all search result pages (assuming 333 pages).

## 🖼️ Visuals

<p align="center">
  <img src="2.jpg" style="max-width: 65%; height: auto;">
</p>

## 👥 Contributors

- 👨‍🦰 Ben Ozfirat

- 👩‍🦳 Ezgi Tandoğan

- 👱‍♂️ Christian Valéry

## 📅 Timeline

- `Day 1`: Project setup, library installation, and initial testing.

- `Day 2-3`: Developing and refining the web scraper.

- `Day 4`: Data extraction, DataFrame creation, and CSV file handling.

- `Day 5`: Documentation and final testing.

<p align="center">
  <img src="3.jpg" style="max-width: 55%; height: auto;">
</p>
