#!/usr/bin/python3
#filename: monitor_outbound_netowork.py
#description: monitor the outbound connection.

import subprocess
import sys
import re
import datetime

destination="google.com"

def get_ip_of_target_hop(destination,hops=3):
  last_line=""
  traceroute_cmd=("traceroute -m %s %s| awk {'print $2'}" % (hops,destination))  #get the ip
  proc = subprocess.Popen(traceroute_cmd, shell=True,stdout=subprocess.PIPE)
  traceroute = proc.stdout.readlines()
  for line in traceroute:
      #print(line)
      last_line=line.decode("utf-8").rstrip()

  return last_line

def ping_target(ip,packets=3):
  ping_cmd=("ping -c %s %s" % (packets,ip)) #ping ip
  proc = subprocess.Popen(ping_cmd, shell=True,stdout=subprocess.PIPE)
  ping = proc.stdout.readlines()
  regex= re.compile('.*packets trans.*',re.IGNORECASE)
  for line in ping:
    #print(line.decode("utf-8").rstrip())
    if regex.match(line.decode("utf-8").rstrip()):
      return line.decode("utf-8").rstrip()

def write_line_to_log(logfile,input_line):
  f=open(logfile,'a')
  f.write(input_line + "\n")
  f.close
  

my_ip=get_ip_of_target_hop(destination) #get the target to ping
print ("target ip is '%s'" % my_ip)
output=ping_target(my_ip) #ping output summary
t=datetime.datetime.now()
mytime = (t.strftime("%a %x %X")) # logging style 
mylog_date=(t.strftime("%m-%d-%y")) # filename style
myline = ("%s | %s" % (mytime,output) ) #log entry
print(myline)
log_filename=("/var/tmp/net_monitor_%s.log" % mylog_date) #log file
write_line_to_log(log_filename,myline) #write to log file 




