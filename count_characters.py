#!/usr/bin/python
#filename: count_characters.py
#date: 08 Sept 2019 
#updated 8/29/22 to comply with python3 format
#description: a python program that counts characters in a string
#use: python3 count_characters.py 'John Doe'

import sys
print ("This is the name of the script: ", sys.argv[0])


if ( len(sys.argv)  == 1 ):
  print ("No data found exiting...")
  print ("You need to type a line of characters. Try a name.\n .. use example: "  + sys.argv[0] + " 'John Doe'")
  sys.exit(0)
elif  ( len(sys.argv)  == 2 ):
  print ("The arguement you provides was: ", sys.argv[1])
  print ("...counting characters\n")
else:
  print ("Number of arguments: ", len(sys.argv), " is invalid.")
  print ("...invalid input\nexiting\n")
  sys.exit(1)

string = sys.argv[1]
count = 0
for c in string:
  count = count + 1

print ("Characters counted : " + str(count) + " in " + "'" + string + "'")
