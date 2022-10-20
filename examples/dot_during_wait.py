#!/usr/bin/python3
#filename: dot_during_wait.py
#description: example of how to implement a flush with wait using sys.stdout.write. 
import sys
import time 
dc=1
print ("Wait 10 seconds with dot feedback:")

for i in range(10):
  sys.stdout.write('.')
  sys.stdout.flush()
  time.sleep(1)
  dc=dc+1

print ("")
