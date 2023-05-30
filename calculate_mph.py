#!/usr/bin/python
#filename: calculate_mph.py
#description: calculate the average speed with two strings passed on the command line

def calculate_mph(distance: float, time_minutes: float) -> float:
    time_hours = time_minutes / 60
    speed_mph = distance / time_hours
    return round(speed_mph,2)

#def is_float(s):
#    try: 
#       float(s)
#       return True
#   except ValueError:
#       return False


import sys

if "--help" in sys.argv:
    print("This program checks if a string is a float.")
    print(f"Usage: python {sys.argv[0]} <minutes> <distance>")
    print(f"Example: python {sys.argv[0]} 29 1.6")
else:
   if len(sys.argv) !=3:
       print(f"Error: Please provide two strings or type {sys.argv[0]} --help for an example")
   else: 
    minutes =  float(sys.argv[1]) #convert string to float
    distance = float(sys.argv[2]) #covert string to float
    speed=calculate_mph(distance,minutes)
    print(f"Your {speed} was MPH for a distance of {distance} miles in {minutes} minutes.")
