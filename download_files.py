#!/usr/bin/python3.3
#filename: download_files.py
#description: download files from a list
#source: https://stackoverflow.com/questions/3173372/download-files-from-a-list-if-not-already-downloaded
import os.path
import urllib.request

links = open('links.txt', 'r')
for link in links:
    link = link.strip()
    name = link.rsplit('/', 1)[-1]
    #this downloads in the location you start the run from
    filename = os.path.join('./', name)

    if not os.path.isfile(filename):
        print('Downloading: ' + filename)
        try:
            urllib.request.urlretrieve(link, filename)
        except Exception as inst:
            print(inst)
            print('  Encountered unknown error. Continuing.')