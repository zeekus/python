#!/usr/bin/python3
#filename: re_example.py
#description: regular expression matching example

import re
sentence=("I like chicken.")
if re.search( "chicken", sentence):
    print ("We found a match.")
	