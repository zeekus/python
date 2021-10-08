#!/usr/bin/python3

from bs4 import BeautifulSoup
import html5lib
import requests

URL = "https://www.annapolislinux.org"
r=requests.get(URL)

soup = BeautifulSoup(r.content, 'html5lib')
print(soup.prettify())
