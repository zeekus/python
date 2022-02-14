#!/usr/bin/python3
# Description This program demonstrates how to use Argv with python and caclulate dates in the future.
# filename: kill_harv_calculator.py
# date: 2/14/2022

#Sample run: python3 skill_harv_calculator.py 39.0 5277089
#This is the name of the program: skill_harv_calculator.py
#Argument List:  ['skill_harv_calculator.py', '39.0', '5277089']
#Argument elements:  3
#minutes left: 5716
#Fri, 18 Feb 2022 14:20:09

from datetime import datetime, timedelta
import sys

def help():
    print ("Help...")
    print ("use: type in the gain per minute and the current skills")
    string=(sys.argv[0])
    #string=''.join(map(str,list))
    print ("example: " + string + " 40.5 5000000")

def calculate_end_date(rate,target):
    minutes=0
    while float(target)<5500000:
        target=float(target)+float(rate)
        minutes=minutes+1
    
    return minutes    
    
print("This is the name of the program:", sys.argv[0])

print("Argument List: ",  str(sys.argv) )
print("Argument elements: ", len(sys.argv) )
if len(sys.argv) < 3 or sys.argv[1] == "-h":
   help()
   exit()

#mins left until target
minutes_left=calculate_end_date(sys.argv[1],sys.argv[2])

#get the date of completion
print("minutes left:", str(minutes_left))
now = datetime.now()
future_day = now + timedelta(minutes = minutes_left )
print(future_day.strftime('%a, %d %b %Y %H:%M:%S %Z'))


