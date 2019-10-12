#!/usr/bin/env python3 
#filename: time_wizard.py
#description: converting time into CST from other timezones 
#author: Teddy Knab
#date: 12/Oct/ 2019
#version 1.0
#Licence: MIT
#Copyright <2019> <Teddy Knab>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from datetime import datetime
from datetime import timedelta
import argparse
import sys
from pytz import timezone

#import os #for timezone
#import sys

def timezone_select(string):
    zone=""
    string=string.upper()
    if (string == "PST" ):
        zone=timezone("America/Los_Angeles")
    elif (string =="MST"):   
        zone=timezone("America/Denver")
    elif (string =="CST"):   
        zone=timezone("America/Chicago")
    elif (string =="EST"):   
        zone= timezone('America/New_York')
    elif (string =='HST'):
        zone= timezone('Pacific/Honolulu')
    elif (string =="AST"):
        zone=timezone('America/Port_of_Spain')
    elif (string =="CHST"):
        zone=timezone("Pacific/Guam")
    else:
        #south_africa = timezone('Africa/Johannesburg')
        #sa_time = datetime.now(south_africa)
        print("error not configured for this time zone")
        sys.exit()

    return zone


def display_formated_time(start_time,end_time,time_delta,lc_tz,zab_cst):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    lt_s=lc_tz.localize(start_time)
    lt_e=lc_tz.localize(end_time)
    print(f"------------------------------------------------------")
    print(f"Local Start Time is   :", lt_s.strftime(fmt)) #local start
    print(f"Local End Time is     :", lt_e.strftime(fmt))   #local end 
                                                      
    c_s=lt_s.astimezone(zab_cst)#cst start
    c_e=lt_e.astimezone(zab_cst)#cst end
    print(f"Zabbix Start Time is  :", c_s.strftime(fmt))
    print(f"Maintenance window    : {time_delta}") #time delta
    print(f"Zabbix End Time is    :", c_e.strftime(fmt))


def dds_time_dde_time(s_yyear,s_mmon,s_dday,s_hhour,s_mmin,e_yyear,e_mmon,e_dday,e_hhour,e_mmin,tz):
    lc_tz=timezone_select(tz) 
    zab_cst=timezone_select("CST") 
    start_time= datetime(year=int(s_yyear), month=int(s_mmon), day=int(s_dday), hour=int(s_hhour), minute=int(s_mmin) )  #start time 9/19/2099:17:01
    end_time= datetime(year=int(e_yyear), month=int(e_mmon), day=int(e_dday), hour=int(e_hhour), minute=int(e_mmin) )    #end time 9/20/2099:18:01
    time_delta=(end_time-start_time)
    #print(f"start time is {start_time}")
    #print(f"end time is {end_time}")
    display_formated_time(start_time,end_time,time_delta,lc_tz,zab_cst)



def time_delta_converter(yyear,mmon,dday,hhour,mmin,fdays,fhrs,fmins,tz):
    lc_tz=timezone_select(tz) 
    zab_cst=timezone_select("CST") 
    start_time= datetime(year=int(yyear), month=int(mmon), day=int(dday), hour=int(hhour), minute=int(mmin) )  #start 9/30/19:5:05
    time_delta = timedelta(days=int(fdays),hours=int(fhrs),minutes=int(fmins))                                 #hours:mins
    delta_end = (start_time + time_delta)
    display_formated_time(start_time,delta_end,time_delta,lc_tz,zab_cst)

#######################
#Variables 
#######################
debug=1 #debug mode 1 for debugging

#######################
#Python Arg Parser Library
########################
parser = argparse.ArgumentParser(description='Future time converter')
parser.add_argument('--start','-s', type=str,help='The start time. - example -s 9/1/2099:09:30')
parser.add_argument('--end','-e',   type=str,help='The end time takes end time or hours:mins. example -e 9/2/2099:09:45 or 24:45 for a 24 hour 25 minute window')
parser.add_argument('--timezone','-tz',   type=str,help='The timezone for localtime.')
parser.add_argument('--version', '-v', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if debug==1:
    print(f"DEBUG 1 ARGS: {args}")

if args.timezone:
    if debug==1:
        print("DEBUG2: Characters in args.timezone: " + str(len(args.timezone)) )
        print("DEBUG3: RAW args.timezone: " + (args.timezone) )

    zone=args.timezone
else:
    print("--timezone missing")
    parser.parse_args(['--help'])

if args.start:
    if debug==1: 
        print("DEBUG4: characters in args.start: " + str(len(args.start)) )
        print("DEBUG5: RAW args.start: " + (args.start) )
    s_mydate,s_myhour,s_mymin=args.start.split(":") #split by :
    (mmon,dday,yyear)=s_mydate.split("/") #split start date
else:
    print("--start missing")
    parser.parse_args(['--help'])

if args.end:
    end_variables=args.end.split(":")
    if debug==1: 
        print("DEBUG6: characters in args.end: " + str(len(args.end)) )
        print("DEBUG7: RAW args.end: " + (args.end) )
    if (len(end_variables)==3):
        print("three variables passed to end date time end")
        #date field sometimes we are given the end date time
        (e_mydate,e_myhour,e_mymin)=args.end.split(":")
        (e_mmon,e_dday,e_yyear)=e_mydate.split("/") #split end date
        dds_time_dde_time(yyear,mmon,dday,s_myhour,s_mymin,e_yyear,e_mmon,e_dday,e_myhour,e_mymin,tz=zone)
    elif (len(end_variables)==2):
        print("two variables passed to end date time end")
        #hours from time given in --start field
        (e_hr,e_min)=args.end.split(":")
        (mmon,dday,yyear)=s_mydate.split("/")
        print(f"year: {yyear},month: {mmon},day: {dday},s hour:{s_myhour},s min: {s_mymin} e_hr:{e_hr},e_min: {e_min}")
        time_delta_converter(yyear,mmon,dday,s_myhour,s_mymin,fdays=0,fhrs=e_hr,fmins=e_min,tz=zone)
    else:
        print(f"Bad data provided please try again")
        parser.parse_args(['--help'])

else:
    print("--end missing")
    parser.parse_args(['--help'])
