#!/usr/bin/python3
#filename: timeoff_audit.py
#description: cat a text file with data to script and add up the hours
#example data file:
#                   8 hours: 1/17: Holiday
#                   8 hours: 2/21: Holiday
#                   8 hours: 2/22: UTO 
#                   8 hours: 4/7: UTO 
#                   1.5 hours: 4/13: UTO
#                   1 hours: 4/20: sick 
#                   2 hours: 4/28: sick 
#
import sys,re
#########################
#three types of time off
#########################
holiday=0.0
sick=0.0
vacation=0.0
for line in sys.stdin:
    line=line.rstrip() #remove white space at end of line
    hours,taken,type=line.split(':') #spit line in to strings
    hours = hours.strip() # remove white space around hours
    print(f'{hours},{type}') 
    hours=hours.split(" ")[0] #get number of hours from string
    print(f'2 {hours},{type}') 
    if re.search('UTO', type):
        vacation=vacation+float(hours)
        print(f"hours are uto {hours}")
    if re.search('Holiday', type):
        holiday=holiday+float(hours)
    if re.search('sick',type):
        sick=sick+float(hours)

    # if 'Exit' == line.rstrip():
    #     break
    #print(f'Processing Message from sys.stdin *****{line}*****')
remaining_vacation=200-(vacation+sick+holiday)
print("Processing complete...")
print (f'sick hours         : {sick} hours')
print (f'vacation hours     : {vacation} hours')
print (f'holiday hours      : {holiday} hours')
print (f'remaining time off : {remaining_vacation} hours')