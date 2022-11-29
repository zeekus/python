
#filename:parse_game_log.py
#description: parse the game log and get useful info
import re
import os
import glob
import time
import subprocess

class ParseGameLog:
  def __init__(self,debug=0):
   self.debug=debug
   
  def readfile_getlast(myfilename,target):
   #description: a function to find a two target words in a string in a file
   #print(f"Info: read_file called with myfile:{myfilename},target:{target}")
   try:
    file = open (myfilename, 'r', encoding="utf-8")
    for myline in file:
      log_line_parsed=myline.strip().replace(' (','|')#convert " (" to | 
      log_line_parsed=log_line_parsed.replace(') ','|')#convert  ") " to |
      log_line_parsed=log_line_parsed.replace('[ ','').replace(' ]','') #remove both [ ] around tex
      result = re.search('(.+)'+target+'(.+)',log_line_parsed) #just get target
      if result:
        logtime,title,message=log_line_parsed.split("|") #parse by delimiter
        #print(f"HIT:{log_line_parsed}")
        #print(f"logtime:{logtime},title:{title},message:{message}")
    if file.closed is False:
      print(f"File close status is '{file.closed}'. Closing file.") if self.debug==1 else None
      file.close() #close file
      print("parsed.readfile end") if self.debug==1 else None
    return logtime,title,message #get last line with target
   except:
    print(f"Error: problem opening or parsing {self.myfilename}")


  def get_newest_game_file(self,gamelog):
     #proc=subprocess.run(['find','/home','-iname','GameLogs'], check=True, stdout=subprocess.PIPE, universal_newlines=True)
     proc=subprocess.run(['find','/home','-iname',gamelog], check=True, stdout=subprocess.PIPE, universal_newlines=True)
     directories=[] #may have more than onesearchedfile
     directories=proc.stdout.rstrip().split("\n")  #generates list - remove white space at end of line and split by whitespace if more than one line
     list_of_files=[]
     print(f"my dirs: '{directories}'")
     for directory in directories:
       print(f"Exending list with '{directory}/*.txt' ")
       list_of_files.extend(glob.glob(directory + "/*.txt")) #append list
       file_count=0
       sorted_list=sorted( list_of_files, key = lambda file: os.path.getmtime(file)) #sort list of files by mtime to get newest
       for file in sorted_list: 
        file_count=file_count+1
        if self.debug==1:
          print(f"\nLast File from list of {file_count} files: {file}")
          print("{} - {}".format(file, time.ctime(os.path.getctime(file))) )
     return file #return last file



