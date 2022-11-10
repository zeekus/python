#!/usr/bin/python
#filename: read_file.py
# Open a file: file

myfilename="moby_dick.txt"

try: 
 file = open (myfilename, 'r', encoding="utf-8")

 # Print it
 print(file.read())

 # Check whether file is closed
 print(file.closed)

 # Close file
 file.close()

 # Check whether file is closed
 print(file.closed)
except: 
  print(f"File '{myfilename}' appears to be missing")




