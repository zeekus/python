#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import html5lib
import lxml
import selenium

URL = "https://www.annapolislinux.org"
r=requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())
