#!/usr/bin/python
#filename: count_characters.py
#date: 08 Sept 2019 
#updated 8/29/22 to comply with python3 format
#description: a python program that counts characters in a string

import sys
print ("This is the name of the script: ", sys.argv[0])

print ("Number of arguments: ", len(sys.argv))

if ( len(sys.argv)  == 1 ):
  print ("No data found exiting...")
  print ("You need to type a line of characters. Try a name.\n .. use example: "  + sys.argv[0] + " 'Matt Smith'")
  sys.exit(0)
else:
  print ("The arguement you provides was: ", sys.argv[1])
  print ("...counting characters\n")

string = sys.argv[1]
count = 0
for c in string:
  count = count + 1

print ("Characters counted : " + str(count) + " in " + "'" + string + "'")
