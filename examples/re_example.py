#!/usr/bin/python3
#filename: re_example.py
#description: regular expression matching example

import re
sentence=("I like chicken.")
match="chicken"

#note the shorter string needs to be first. 
if re.search( match, sentence):
  print (f"We found a match for '{match}' in '{sentence}'")
	
