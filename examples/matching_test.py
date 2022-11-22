#filename: matching_test.py
#description: a function to find a two target words in a string in a file

import re
import sys
from time import sleep

def readfile(myfilename,gametime,target):
   #description: a function to find a two target words in a string in a file
   print("Info: read_file called")
   try:
    file = open (myfilename, 'r', encoding="utf-8")
    for myline in file:
      log_line_parsed=myline.strip().replace(' (','|')#convert " (" to | 
      log_line_parsed=log_line_parsed.replace(') ','|')#convert  ") " to |
      log_line_parsed=log_line_parsed.replace('[ ','').replace(' ]','') #remove both [ ] around tex
      #result = re.search('(.+)'+target+'(.+)',log_line_parsed) #just get target
      result = re.search('(^)'+gametime+'(.+)'+target+'(.+)',log_line_parsed) #get gametime and target
      #result = re.search('(^)'+gametime+'(.+)',log_line_parsed)
      #result = re.search('(.+)'+gametime+'(.+)'+target+'(.+)',log_line_parsed)
      if result:
        logtime,title,message=log_line_parsed.split("|") #parse by delimiter
        print(f"HIT:{log_line_parsed}")
        print(f"logtime:{logtime},title:{title},message:{message}")

   except:
     print(f"Warning: unable to open file.")


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
    return logtime,title,message #get last line with target

   except:
     print(f"Warning: unable to open file.")

myfilename="example_game_log.txt"
gametime="2022.11.19 15:29:04" 
logtime,title,message=readfile_getlast(myfilename,"Jumping")
print(f"Waiting for jump message:", end='')
while True:
  logtime1,title1,message1=readfile_getlast(myfilename,"Jumping")
  if logtime==logtime1 and message==message1:
    sleep(1)
    print (".",end='',flush=True)
  else:
    print ("\nWe jumped.")
    logtime=logtime1;message=message1
    sys.exit()
    
