#!/usr/bin/python3
#filename: check_site.py
#description: checks sites to see if they are down using Beautiful soup. 

from bs4 import BeautifulSoup
import requests
import re

mysite="example.net"


def check_site(URL):
  page = requests.get(str(URL))
  soup = BeautifulSoup(page.content, 'html.parser')
  title=soup.find('title') #get title in html format
  if re.search('[5|4]0[0-9]',title.text):
    print("site is down")
  else:
    print (f"site up --- {title.text}") #render text no HTML

sites=['bitbucket','confluence','jira']

for site in sites:
  myurl=(f"https://{site}.{mysite}")
  check_site(myurl)
