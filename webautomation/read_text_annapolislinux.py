#!/usr/bin/python3
#read_text_from_annapolislinux.py

#headless chrome example
#requirements chromedriver

#tested 29 Sept 29 2021

from bs4 import BeautifulSoup
#import requests
#import html5lib
import lxml
from selenium import webdriver

myoptions = webdriver.ChromeOptions()
myoptions.add_argument('--ignore-certificate-errors')
myoptions.add_argument('--incognito')
myoptions.add_argument('--headless')

driver = webdriver.Chrome(options=myoptions)
source=driver.get('https://annapolislinux.org')
html_source=driver.page_source

soup = BeautifulSoup(html_source,'lxml')

#article_block = soup.findall('div',class_='post-title')



#condensed text
print (soup.get_text("|", strip=True))

#text with html
#print (soup.prettify())


#inspect each string
#lines=(soup.get_text())
#for string in lines:
#  print(string)


soup = BeautifulSoup(html_source, 'html.parser')
for tag in soup.find_all('title'):
    print(repr((tag.sourceline, tag.sourcepos, tag.string)))
