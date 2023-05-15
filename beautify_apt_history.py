
#!/usr/bin/python
#filename: beautify_apt_history.py
#description: parse file /var/apt/history.log and make it look pretty.

import re
import os
import time
import subprocess
import magic

debug=0
target_filename="/var/log/apt/history.log"

def use_magic_to_get_file_encoding(target_filename):
 try:
   blob = open(target_filename).read()
   m=magic.Magic(mime_encoding=True)
   myencoding = m.from_buffer(blob)
   print("Passed: encoding is '{}' on '{}'".format(myencoding,target_filename))
   return myencoding
 except:
  print("Failed when trying to determine the file encoding for our file '{}'".format(target_filename))

#verify if the file exists or exit
file_exists=os.path.exists(target_filename)
if file_exists == False:
 print("Failed: '{}' file not found.".format(target_filname))
 os._exit(os.EX_IOERR)
else:
 print("Passed: '{}' file exists.".format(target_filename))


#main variables
e=use_magic_to_get_file_encoding(target_filename)
data_from_file=[] #array of data elements from file
upgraded_items=[] #array of upgraded_itemsd items

try:
 myfile = open(target_filename, 'r', encoding=e)
 for line in myfile:
     data_from_file.append(line.strip())
 myfile.close()
except:
  print(f"error opening: target_filename")

if debug==1:
 print("=========================================")
 print("data from file")
 print("=========================================")
 for l in data_from_file:
   l=l.strip()
   if len(l) > 0:
    print(". '{}'".format(l))
 print("=========================================")



count=0
st_date=''
ed_date=''
for line in data_from_file:
  line=line.strip() #remove white space
  if re.search("^Start-Date:", line):
      st_date=line.split("Start-Date:")[1].strip()
  elif re.search("^Commandline:",line):
     cl=line.split(":")[1]
  elif re.search("^Requested-By:",line):
     rb=line.split(":")[1]
  elif re.search("^Upgrade:",line): #upgraded_itemsd items
     upgraded_items=line.split("Upgrade:")[1]
  elif re.search("^End-Date:",line):
      ed_date=line.split("End-Date:")[1].strip()
  else:
      a='nothing'

  my_start=st_date.split(' ')[0] #trimmed off hours/minutes
  my_end=ed_date.split(' ')[0] #trimmed off hours/minutes

  if my_start == my_end and len(my_start)>1:
     print()
     count=count+1
     if debug==1:
       print("st and ed are {}, {}".format(my_start,my_end))
     print("Update completed: {}".format(my_start))
     print("=============================================")

     newlist=upgraded_items.split(')')
     for line1 in newlist:
       line1=line1.replace(',','') #get rid of "," at beginning of the string
       if ( len(line1) > 0 ):
           line1=line1.split(" (")[0] #remove the ubuntu specific version info
           print("Updated '{}'".format(line1.strip()))
