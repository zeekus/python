
#filename:parse_game_log.py
#description: parse the game log and get useful info

import glob
import re
import os
import time
import subprocess

myfilename="example_game_log.txt"
counter=0
debug=0
fields=[]

try: 
 file = open (myfilename, 'r', encoding="utf-8")
 #with open(myfilename, 'r', encoding="utf-8") as file:
 for line in file:
   parsed_string=(line.strip())
   if re.search( "Listener:", line):
      character=line.rstrip().split(":")[1].lstrip()
      print(f"* Got Character: {character}")
   elif re.search("Session Started:",line):
      log_start_time=line.rstrip().split(":")[1].lstrip()
      print(f"* Got Session Start: {log_start_time}")
   elif re.search("^\[",line):
      log_line_parsed=line.rstrip().lstrip()
      counter=counter+1
      print(f"{counter}: {log_line_parsed}")
      log_line_parsed=log_line_parsed.replace(' (','|')#convert " (" to | 
      log_line_parsed=log_line_parsed.replace(') ','|')#convert  ") " to |
      gt,mtype,message=log_line_parsed.split("|")
      gt=gt.replace('[ ','').replace(' ]','') #remove both [ ] around text
      mydate=gt[0]
      mytime=gt[1]
      mydate,mytime=re.findall(r'\S+',gt)
      print(f"time unparsed '{gt}'")
      print(f"mytime is {mytime}")
      print(f"mydate is {mydate}")
      print(f"type of message:{mtype}")
      print(f"message:{message}")
      #print(f"time:{gt},type of message:{mtype},message:{message}")
   else:
      if debug==1:
        print(f"Junk ? => {line.rstrip().lstrip()}")


   #parsed_string=(parsed_line.lstrip())
   #print(parsed_string)
 # Print it
 #print(file.read())
 # Check whether file is closed
 if file.closed is False:
  print(f"File close status is '{file.closed}'. Closing.")
  # Close file
  file.close()


except: 
    print (f"Error: we were not able to open {myfilename}")
