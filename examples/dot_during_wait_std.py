#!/bin/python3
#filename:  dot_during_wait_std.py
#description: standard waits in python in conjunction with stdout writes require a flush
import time 
dc=1
print ("Wait 10 seconds with dot feedback:")

for i in range(10):
  print ('.', end='', flush=True)
  time.sleep(1)
  dc=dc+1

print ("")
