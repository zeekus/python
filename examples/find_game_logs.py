#filename: find_newest_game_log_file.py
#description: from an abstract search generate a list of all the text files and return the newest file.

import glob
import os
import time
import subprocess

def search_for_me(search): #returns newest file from on search.
  searchedfile=glob.glob(search)
  return sorted( searchedfile, key = lambda file: os.path.getmtime(file)) #mtime .getctime(file)) #changetime

def search_for_newest(mylist):
  return sorted( mylist, key = lambda file: os.path.getmtime(file)) #mtime

def find_latestfile():
  list_of_files = glob.glob('/path/to/folder/*') # * means all if need specific format then *.csv
  latest_file = max(list_of_files, key=os.path.getmtime)
  print(latest_file)

proc=subprocess.run(['find','/home','-iname','GameLogs'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
directories=[] #may have more than onesearchedfile
directories=proc.stdout.rstrip().split("\n")  #generates list - remove white space at end of line and split by whitespace if more than one line
list_of_files=[]
last=""
print(f"my dirs: '{directories}'")
for directory in directories:
  print(f"Exending list with '{directory}/*.txt' ")
  list_of_files.extend(glob.glob(directory + "/*.txt")) #append list

new=search_for_newest(list_of_files)
file_count=0
for file in new:
  file_count=file_count+1
  
print(f"\nLast File from list of {file_count} files: {file}")
print("{} - {}".format(file, time.ctime(os.path.getctime(file))) )