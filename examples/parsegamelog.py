
#filename:parse_game_log.py
#description: parse the game log and get useful info

class ParseGameLog:
   import glob
   import os
   import subprocess

   def __init__(self, myfilename,debug=0):
     self.myfilename=myfilename
     self.debug=debug
     if debug==1:
       print(f"debug: {myfilename} debug status is {debug}")
   
   def readfile(self):
    import re
    import time
    counter=0
    myline=""
    print("read_file called")
    try: 
      file = open (self.myfilename, 'r', encoding="utf-8")
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



myfilename="example_game_log.txt"
parse=ParseGameLog(myfilename,1)
parse.readfile()

