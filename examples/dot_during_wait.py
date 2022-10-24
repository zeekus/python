#!/usr/bin/python3
#filename: dot_during_wait.py
#description: example of how to implement a flush with wait using sys.stdout.write. 
import sys
import time 
print ("Wait 10 seconds with dot feedback:")

print("example1")
for i in range(3):
  sys.stdout.write('.')
  sys.stdout.flush()
  time.sleep(.5)

print("example2")
for i in range(3):
    print (".", end='', flush=True)
    time.sleep(.5)




print ("")
