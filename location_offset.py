#!/usr/bin/python3
#filename: location_offset.py
#description: random number with range using a step example 0-10 step 1
import random
x=random.randrange(0,10,1)
print(str(x))

def randomize_xy(x,y):
   xr=random.randrange(0,3,1)
   yr=random.randrange(0,3,1)
   #print(str(xr),str(yr))

   if yr == 2:
     y=y-1
   else:
    y=y+yr
   if xr == 2:
     x=x-xr
   else:
     x=x+xr

   return x,y

x=100
y=150
print("start location is : " + str(x) + "," + str(y))
x,y=randomize_xy(x,y)
print((str(x),str(y)))



