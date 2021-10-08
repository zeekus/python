#!/usr/bin/python
from bs4 import BeautifulSoup
import requests

#get all raw data from website
page = requests.get("https://forecast.weather.gov/MapClick.php?lat=38.9768&lon=-76.4901")

#get page HTML content
soup = BeautifulSoup(page.content, 'html.parser')

#get seven day forcast from HTML content
seven_day = soup.find(id="seven-day-forecast")

#put tomstone-container items from seven_day
forecast_items = seven_day.find_all(class_="tombstone-container")

#get forcast for tonight
tonight = forecast_items[0]
img=tonight.find("img")
desc=img['title']
print ("metadata - img['title']")
print(desc)
