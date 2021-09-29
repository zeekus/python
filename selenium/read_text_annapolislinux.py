#!/usr/bin/python3
#read_text_from_annapolislinux.py

#headless chrome example
#requirements chromedriver

from bs4 import BeautifulSoup
import requests
import html5lib
import lxml
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(chrome_options=options)
source=driver.get('https://annapolislinux.org')
source_code=driver.page_source

soup = BeautifulSoup(source_code,'lxml')
#article_block = soup.findall('div',class_='post-title')

print(soup.get_text())
