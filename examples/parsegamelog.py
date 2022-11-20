
#filename:parse_game_log.py
#description: parse the game log and get useful info
import re
import os
import glob
import time
import subprocess

class ParseGameLog:
  # import glob
  # import os
  # import subprocess
  #import re

  def __init__(self,debug=0):
   self.debug=debug
   
  def readfile(self,myfilename):
   #import re
  #  import time
   counter=0
   myline=""
   print("Debug: read_file called") 
   try: 
    file = open (myfilename, 'r', encoding="utf-8")
    for line in file:
      counter=counter+1
      myline=line.strip()
      if re.search("^Listener:", myline):
        character=myline.split(":")[1].strip()
        print(f"* Got Character: '{character}'")
      elif re.search("Session Started:",myline):
        started=myline.split("Started:")[1].strip()
        print(f"* Got Start: '{started}'")
      elif re.search("^\[",myline):
        log_line_parsed=myline.replace(' (','|')#convert " (" to | 
        log_line_parsed=log_line_parsed.replace(') ','|')#convert  ") " to |
        gt,mtype,message=log_line_parsed.split("|")
        gt=gt.replace('[ ','').replace(' ]','') #remove both [ ] around text
        mydate,mytime=re.findall(r'\S+',gt)
        if self.debug==1:
          print(f"Debug: '{mydate}' '{mytime}' , '{mtype}', '{message}'")
      else:
         if self.debug==1:
          print(f"Junk ? => {myline}") 
   except:
    print(f"Error: problem opening or parsing {self.myfilename}")

   if file.closed is False:
    print(f"File close status is '{file.closed}'. Closing file.") if self.debug==1 else None
    file.close() #close file
    print("parsed.readfile end") if self.debug==1 else None

  def get_newest_game_file(self,gamelog):
    #  import subprocess
    #  import time
    #  import os
    #  import glob
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
        #print(f"\nLast File from list of {file_count} files: {file}")
        #print("{} - {}".format(file, time.ctime(os.path.getctime(file))) )
     return file #return last file

parse=ParseGameLog(debug=1)
myfilename=parse.get_newest_game_file('GameLogs')
print(myfilename)
parse.readfile(myfilename)
#parse.readfile()

