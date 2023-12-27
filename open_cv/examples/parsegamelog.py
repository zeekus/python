
#filename:parse_game_log.py
#description: parse the game log and get useful info
import re
import os
import glob
import time
import subprocess

class ParseGameLog:
  """
    A class for processing information from the game logs.

    This class has two class methods: get_newest_gamefile, load_image_data_from_json.

    Attributes:
        game_file (str): The file path holding the lastest game log.
        target (str): A message to use for searching for searching the game log.
        gamelog (str): The directory path to the game log.
        myfilename (str): full path to the game log.

    Returns:
      Either logtime,message or None
      Logtime - holds system time in UTC in which log was written.
      message - can be None or a valid entry.
  """
  def __init__(self,debug=0):
   self.debug=debug

  def get_newest_game_file(self,gamelog='*ame*ogs*'):
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
   
  def readfile_getlast(self,myfilename,target):
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
    else:
      logtime="";message="NONE" # jump not found in file
    file.close() if file.closed is False else None
    return logtime,message #get last line with time/target
   except:
    print(f"Error: problem opening or parsing {myfilename}")  

