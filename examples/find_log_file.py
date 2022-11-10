import glob
import os
import time

searchedfile = glob.glob("*.txt")
files = sorted( searchedfile, key = lambda file: os.path.getctime(file))

for file in files:
 print("{} - {}".format(file, time.ctime(os.path.getctime(file))) )
